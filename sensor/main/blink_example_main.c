#include <stdio.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "esp_random.h"

#define TAG "temp_sim"

void app_main(void)
{
    srand((unsigned)esp_random());

    while (1) {
        float temp = 20.0f + (rand() % 1500) / 100.0f; // 20.00 to 35.00

        ESP_LOGI(TAG, "Temperature: %.2f C", temp);

        vTaskDelay(pdMS_TO_TICKS(1000)); 
    }
}
