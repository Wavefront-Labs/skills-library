---
id: computing-software.firmware-embedded-development.esp-idf.gpio-isr-service
name: gpio-isr-service
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, gpio-isr-service, gpio-install-isr-service, gpio-isr-handler-add, gpio-glitch-filter, strapping-pins, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Handle ESP32 GPIO interrupts with the per-pin ISR service: configuration, IRAM-safe handlers, deferring to a task, debouncing, and chip-specific pin restrictions."
sources:
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_gpio/include/driver/gpio.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/gpio.rst
  - https://github.com/espressif/esp-idf/blob/master/examples/peripherals/gpio/generic_gpio/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPIO ISR service

## Pattern
```c
#include "driver/gpio.h"
#define BTN_GPIO GPIO_NUM_4
static QueueHandle_t gpio_evt_q;

static void IRAM_ATTR btn_isr(void *arg)
{
    uint32_t pin = (uint32_t)arg;
    BaseType_t woken = pdFALSE;
    xQueueSendFromISR(gpio_evt_q, &pin, &woken);
    if (woken) portYIELD_FROM_ISR();
}

void buttons_init(void)
{
    gpio_config_t io = {
        .pin_bit_mask = 1ULL << BTN_GPIO,
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .intr_type = GPIO_INTR_NEGEDGE,
    };
    ESP_ERROR_CHECK(gpio_config(&io));
    gpio_evt_q = xQueueCreate(10, sizeof(uint32_t));
    ESP_ERROR_CHECK(gpio_install_isr_service(ESP_INTR_FLAG_IRAM));   /* once per app */
    ESP_ERROR_CHECK(gpio_isr_handler_add(BTN_GPIO, btn_isr, (void *)BTN_GPIO));
}
```
A task receives from `gpio_evt_q` and does the work (logging, I2C, debouncing).

## Service vs single handler
- `gpio_install_isr_service` + `gpio_isr_handler_add`: one dispatcher, per-pin handlers. Use this.
- `gpio_isr_register`: one raw handler for all pins, you decode status yourself. Can't be mixed
  with the service.

## IRAM rules
With `ESP_INTR_FLAG_IRAM`, the ISR can run while flash cache is disabled (during NVS/OTA
writes), so it and everything it touches must be in IRAM/DRAM: `IRAM_ATTR` on the handler and
only internal-memory code and data. Without the flag the handler need not be `IRAM_ATTR`
and the interrupt is held off while the cache is disabled. See iram-attr-and-cache-disabled-code.

## Debouncing
Mechanical buttons bounce for 1-20 ms, giving bursts of interrupts.
- Hardware: RC filter, or the GPIO glitch filters on chips that have them
  (`gpio_new_pin_glitch_filter`, `gpio_new_flex_glitch_filter`).
- Software: in the task, ignore events within N ms of the last accepted one, or disable the pin
  interrupt (`gpio_intr_disable`) and re-enable it from an `esp_timer` after the bounce window.

## Pin restrictions (check your chip's datasheet)
- ESP32: GPIO34-39 are input-only with **no internal pull-ups/downs** (stated in `gpio.h`).
- Strapping pins and the pins used by flash/PSRAM differ per chip: take both lists from the
  datasheet and the module documentation, and avoid external pulls that conflict with boot values.
- Wake from light sleep: `gpio_wakeup_enable(pin, GPIO_INTR_LOW_LEVEL)` + `esp_sleep_enable_gpio_wakeup()`.

## Verify
- [ ] Interrupt still delivered during heavy flash writes (if IRAM flag used) and nothing crashes.
- [ ] Bounce test: 100 presses produce 100 events.
- [ ] No strapping pin has an external pull that conflicts with its boot value.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed in gpio.h: gpio_install_isr_service(intr_alloc_flags) (returns an error if already installed), gpio_isr_handler_add, handlers need IRAM_ATTR only when ESP_INTR_FLAG_IRAM is passed, gpio_isr_register is incompatible with the service, gpio_wakeup_enable / esp_sleep_enable_gpio_wakeup, glitch filter constructors, ESP32 GPIO34-39 input-only without pull resistors. Removed unconfirmed claims: service core affinity, ESP_DRAM_LOGE advice, glitch-filter chip list, strapping and flash pin lists, level-interrupt re-fire advice.
Method: documentation only; no commands were run.
