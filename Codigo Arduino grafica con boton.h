#include <lvgl.h>
#include <TFT_eSPI.h>

static const uint16_t screenWidth = 240;
static const uint16_t screenHeight = 320;

static lv_disp_draw_buf_t draw_buf;
static lv_color_t *buf1;
static lv_color_t *buf2;

TFT_eSPI tft = TFT_eSPI();

#if LV_USE_LOG != 0
void my_print(const char * buf) {
    Serial.printf(buf);
    Serial.flush();
}
#endif

// Variables globales
lv_obj_t * chart;     // Gráfica
lv_obj_t * btn;       // Botón
lv_obj_t * scrollable_panel; // Panel desplazable
bool showing_chart = false;

// Función callback para el botón
static void btn_event_cb(lv_event_t * e) {
    lv_event_code_t code = lv_event_get_code(e);
    if(code == LV_EVENT_CLICKED) {
        showing_chart = !showing_chart;
        
        if(showing_chart) {
            // Mostrar gráfica, ocultar panel
            lv_obj_clear_flag(chart, LV_OBJ_FLAG_HIDDEN);
            lv_obj_add_flag(scrollable_panel, LV_OBJ_FLAG_HIDDEN);
            lv_label_set_text(lv_obj_get_child(btn, 0), "Ver Panel");
        } else {
            // Mostrar panel, ocultar gráfica
            lv_obj_add_flag(chart, LV_OBJ_FLAG_HIDDEN);
            lv_obj_clear_flag(scrollable_panel, LV_OBJ_FLAG_HIDDEN);
            lv_label_set_text(lv_obj_get_child(btn, 0), "Ver Grafica");
        }
    }
}

void create_chart() {
    /* Crear gráfica (inicialmente oculta) */
    chart = lv_chart_create(lv_scr_act());
    lv_obj_set_size(chart, 200, 150);
    lv_obj_align(chart, LV_ALIGN_CENTER, 0, 40);
    lv_chart_set_type(chart, LV_CHART_TYPE_LINE);
    lv_chart_set_range(chart, LV_CHART_AXIS_PRIMARY_Y, 0, 100);
    lv_chart_set_point_count(chart, 10);
    
    /* Agregar dos series de datos */
    lv_chart_series_t * ser1 = lv_chart_add_series(chart, lv_palette_main(LV_PALETTE_RED), LV_CHART_AXIS_PRIMARY_Y);
    lv_chart_series_t * ser2 = lv_chart_add_series(chart, lv_palette_main(LV_PALETTE_BLUE), LV_CHART_AXIS_PRIMARY_Y);
    
    for(int i = 0; i < 10; i++) {
        lv_chart_set_next_value(chart, ser1, random(20, 80));
        lv_chart_set_next_value(chart, ser2, random(10, 90));
    }
    
    /* Estilo */
    lv_obj_set_style_bg_color(chart, lv_palette_lighten(LV_PALETTE_GREY, 1), 0);
    lv_obj_set_style_border_width(chart, 1, 0);
    lv_obj_set_style_radius(chart, 5, 0);
    
    /* Ocultar inicialmente */
    lv_obj_add_flag(chart, LV_OBJ_FLAG_HIDDEN);
}

void create_scrollable_panel() {
    // Crear un panel con scroll
    scrollable_panel = lv_obj_create(lv_scr_act());
    lv_obj_set_size(scrollable_panel, 220, 200);
    lv_obj_align(scrollable_panel, LV_ALIGN_CENTER, 0, 40);
    lv_obj_set_style_bg_color(scrollable_panel, lv_palette_lighten(LV_PALETTE_GREY, 1), 0);
    lv_obj_set_style_radius(scrollable_panel, 5, 0);
    
    // Habilitar scroll
    lv_obj_set_style_pad_all(scrollable_panel, 10, 0);
    lv_obj_set_scrollbar_mode(scrollable_panel, LV_SCROLLBAR_MODE_ACTIVE);
    lv_obj_set_scroll_dir(scrollable_panel, LV_DIR_VER); // Solo scroll vertical
    
    // Contenido del panel (varios elementos para necesitar scroll)
    for (int i = 0; i < 5; i++) {
        // Crear un grupo para cada fila
        lv_obj_t * item_group = lv_obj_create(scrollable_panel);
        lv_obj_set_size(item_group, 200, 80);
        lv_obj_align(item_group, LV_ALIGN_TOP_MID, 0, i * 90);
        lv_obj_set_style_bg_color(item_group, lv_palette_lighten(LV_PALETTE_BLUE, 1 + i), 0);
        lv_obj_set_style_radius(item_group, 5, 0);
        lv_obj_clear_flag(item_group, LV_OBJ_FLAG_SCROLLABLE); // Este contenedor no tiene scroll
        
        // Título
        lv_obj_t * title = lv_label_create(item_group);
        lv_label_set_text_fmt(title, "Elemento %d", i + 1);
        lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 5);
        lv_obj_set_style_text_color(title, lv_color_white(), 0);
        
        // Crear un indicador de valor
        lv_obj_t * slider = lv_slider_create(item_group);
        lv_obj_set_width(slider, 180);
        lv_obj_align(slider, LV_ALIGN_CENTER, 0, 5);
        lv_slider_set_value(slider, random(0, 100), LV_ANIM_OFF);
        
        // Valor
        lv_obj_t * value = lv_label_create(item_group);
        lv_label_set_text_fmt(value, "Valor: %d", (int)lv_slider_get_value(slider));
        lv_obj_align(value, LV_ALIGN_BOTTOM_MID, 0, -5);
        lv_obj_set_style_text_color(value, lv_color_white(), 0);
    }
}

void create_button() {
    /* Crear botón */
    btn = lv_btn_create(lv_scr_act());
    lv_obj_set_size(btn, 150, 40);
    lv_obj_align(btn, LV_ALIGN_TOP_MID, 0, 15);
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED, NULL);
    
    /* Añadir etiqueta al botón */
    lv_obj_t * btn_label = lv_label_create(btn);
    lv_label_set_text(btn_label, "Ver Gráfica");
    lv_obj_center(btn_label);
    
    /* Estilo del botón */
    lv_obj_set_style_bg_color(btn, lv_palette_main(LV_PALETTE_BLUE), 0);
    lv_obj_set_style_text_color(btn, lv_color_white(), 0);
    lv_obj_set_style_radius(btn, 10, 0);
}

void setup_ui() {
    create_button();
    create_chart();
    create_scrollable_panel();
}

void my_disp_flush(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p) {
    uint32_t w = area->x2 - area->x1 + 1;
    uint32_t h = area->y2 - area->y1 + 1;
    
    tft.startWrite();
    tft.setAddrWindow(area->x1, area->y1, w, h);
    tft.pushPixelsDMA((uint16_t *)color_p, w * h);
    tft.endWrite();
    
    lv_disp_flush_ready(disp);
}

void my_touchpad_read(lv_indev_drv_t * indev_driver, lv_indev_data_t * data) {
    uint16_t touchX, touchY;
    bool touched = tft.getTouch(&touchX, &touchY, 600);

    if(!touched) {
        data->state = LV_INDEV_STATE_REL;
    } else {
        data->state = LV_INDEV_STATE_PR;
        data->point.x = touchX;
        data->point.y = touchY;
    }
}

void setup() {
    Serial.begin(115200);
    lv_init();

#if LV_USE_LOG != 0
    lv_log_register_print_cb(my_print);
#endif

    pinMode(27, OUTPUT);
    digitalWrite(27, LOW);
    tft.begin();
    tft.setRotation(0);
    tft.initDMA();
    digitalWrite(27, HIGH);
    
    uint16_t calData[5] = {405, 3238, 287, 3292, 2};
    tft.setTouch(calData);

    buf1 = (lv_color_t *)heap_caps_malloc(sizeof(lv_color_t) * screenWidth * 40, MALLOC_CAP_DMA);
    buf2 = (lv_color_t *)heap_caps_malloc(sizeof(lv_color_t) * screenWidth * 40, MALLOC_CAP_DMA);
    lv_disp_draw_buf_init(&draw_buf, buf1, buf2, screenWidth * 40);

    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.hor_res = screenWidth;
    disp_drv.ver_res = screenHeight;
    disp_drv.flush_cb = my_disp_flush;
    disp_drv.draw_buf = &draw_buf;
    lv_disp_drv_register(&disp_drv);

    static lv_indev_drv_t indev_drv;
    lv_indev_drv_init(&indev_drv);
    indev_drv.type = LV_INDEV_TYPE_POINTER;
    indev_drv.read_cb = my_touchpad_read;
    lv_indev_drv_register(&indev_drv);

    setup_ui();
    Serial.println("Setup done");
}

void loop() {
    lv_timer_handler();
    delay(5);
}