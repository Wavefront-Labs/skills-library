---
id: computing-software.firmware-embedded-development.esp-idf.adc-oneshot-continuous-and-calibration
name: adc-oneshot-continuous-and-calibration
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, esp-adc-calibration, adc-oneshot, adc-continuous, adc-cali-curve-fitting, attenuation, adc2-wifi-conflict, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Read analog voltages accurately on ESP32 chips with the v5 ADC oneshot and continuous drivers plus eFuse-based calibration schemes, attenuation choice and noise handling."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/adc/adc_oneshot.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/adc/adc_calibration.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/adc/adc_continuous.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADC oneshot, continuous and calibration

Raw ESP32 ADC readings are nonlinear and vary chip to chip. Always convert through a
calibration scheme; never scale `raw * 3.3 / 4095`.

## Oneshot read with calibration
```c
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali_scheme.h"

static adc_oneshot_unit_handle_t adc1;
static adc_cali_handle_t cali;

void adc_init(void)
{
    adc_oneshot_unit_init_cfg_t uc = { .unit_id = ADC_UNIT_1 };
    ESP_ERROR_CHECK(adc_oneshot_new_unit(&uc, &adc1));
    adc_oneshot_chan_cfg_t cc = { .atten = ADC_ATTEN_DB_12, .bitwidth = ADC_BITWIDTH_DEFAULT };
    ESP_ERROR_CHECK(adc_oneshot_config_channel(adc1, ADC_CHANNEL_6, &cc));

#if ADC_CALI_SCHEME_CURVE_FITTING_SUPPORTED          /* C3, S3, C6, H2, C5, P4 */
    adc_cali_curve_fitting_config_t k = { .unit_id = ADC_UNIT_1, .chan = ADC_CHANNEL_6,
        .atten = ADC_ATTEN_DB_12, .bitwidth = ADC_BITWIDTH_DEFAULT };
    ESP_ERROR_CHECK(adc_cali_create_scheme_curve_fitting(&k, &cali));
#elif ADC_CALI_SCHEME_LINE_FITTING_SUPPORTED         /* ESP32, S2, C2 */
    adc_cali_line_fitting_config_t k = { .unit_id = ADC_UNIT_1,
        .atten = ADC_ATTEN_DB_12, .bitwidth = ADC_BITWIDTH_DEFAULT };
    ESP_ERROR_CHECK(adc_cali_create_scheme_line_fitting(&k, &cali));
#endif
}

int read_mv(void)
{
    int raw, mv, sum = 0;
    for (int i = 0; i < 16; i++) { adc_oneshot_read(adc1, ADC_CHANNEL_6, &raw); sum += raw; }
    adc_cali_raw_to_voltage(cali, sum / 16, &mv);     /* average raw, then convert */
    return mv;
}
```
Calibration creation fails with `ESP_ERR_NOT_SUPPORTED` on early chips without eFuse
calibration data; handle it (fall back with a warning, or reject the unit in production test).

## Attenuation and range
`ADC_ATTEN_DB_0/2_5/6/12`. Usable input ranges are chip-specific; read the attenuation table
for your target in the ADC docs (on ESP32-C2, for instance, calibration is only supported at
`ADC_ATTEN_DB_0` and `ADC_ATTEN_DB_12`, with inputs above 950 mV and 2800 mV unsupported
respectively). Pick the lowest attenuation that covers your signal.

## Continuous (DMA) mode
For sampling at kHz rates:
```c
adc_continuous_handle_cfg_t hc = { .max_store_buf_size = 1024, .conv_frame_size = 256 };
adc_continuous_new_handle(&hc, &h);
/* adc_continuous_config with pattern list + sample_freq_hz, then adc_continuous_start,
   read frames with adc_continuous_read(h, buf, len, &got, timeout) and parse
   adc_digi_output_data_t entries (format differs per chip: TYPE1 vs TYPE2) */
```
A given ADC unit can work in either oneshot or continuous mode at any one time (on chips with ADC DMA).

## Chip gotchas
- ADC2 is shared with Wi-Fi on ESP32, ESP32-S2 and ESP32-S3; the driver arbitrates between them, so prefer ADC1 pins when Wi-Fi is active. On ESP32-C3, ADC2 oneshot is not supported (unstable results, see the errata).
- The ADC is noise-sensitive: add a bypass capacitor (for example 100 nF ceramic) at the input pad and multisample.
- On ESP32, oneshot reads make the hardware RNG less random while they run.

## Verify
- [ ] Compare against a calibrated DMM at 3+ points across the range; error within your budget.
- [ ] Calibration-scheme creation result checked and logged at boot.
- [ ] No ADC2 channel used on ESP32 or ESP32-C3 unless you have read the ADC2 limits for your chip.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed: calibration scheme choice per chip (line fitting on ESP32, S2, C2; curve fitting on C3, S3, C6, H2, C5, P4), ESP_ERR_NOT_SUPPORTED on missing eFuse data, ADC2/Wi-Fi arbitration and C3 ADC2 limit, one mode per unit, noise capacitor advice. Removed unconfirmed range, impedance and DB_11 rename claims. Wrong: ADC2 was said to be unavailable with Wi-Fi on ESP32; the driver arbitrates.
Method: documentation only; no commands were run.
