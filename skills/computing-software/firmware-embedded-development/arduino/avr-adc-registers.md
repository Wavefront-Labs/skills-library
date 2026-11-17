---
id: computing-software.firmware-embedded-development.arduino.avr-adc-registers
name: avr-adc-registers
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [avr-adc, admux, adcsra, adc-prescaler, free-running-adc, adc-noise-reduction, vcc-measurement, avr, arduino, firmware-embedded-development]
level: advanced
status: draft
description: "Drive the ATmega328P ADC directly: ADMUX reference and channel, ADCSRA prescaler, auto-trigger modes, ADC interrupt, noise-reduction sleep, and Vcc via the 1.1 V bandgap."
sources:
  - https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf
  - https://ww1.microchip.com/downloads/en/Appnotes/AVR120-Characterization-and-Calibration-of-the-ADC-on-an-AVR-DS00002558A.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AVR ADC registers

## Registers (ATmega328P)
- `ADMUX`: REFS1:0 (00 AREF, 01 AVcc, 11 internal 1.1 V), ADLAR (left-adjust for 8-bit reads),
  MUX3:0 (channel 0-7, 8 = temperature sensor, 14 = 1.1 V bandgap, 15 = GND).
- `ADCSRA`: ADEN, ADSC (start), ADATE (auto trigger), ADIF, ADIE, ADPS2:0 (prescaler).
- `ADCSRB`: ADTS2:0 trigger source (000 free running, Timer1 compare B, Timer0 overflow, etc.).
- `DIDR0`: disable digital input buffers on analog pins (less power and noise).

## Clock
ADC clock must be 50-200 kHz for 10-bit accuracy. At 16 MHz: prescaler 128 -> 125 kHz -> 13 cycles
per conversion ~ 104 us (~9.6 kS/s). Prescaler 16 (1 MHz) gives ~77 kS/s with ~8-bit effective
accuracy, often acceptable.

## Single conversion
```cpp
uint16_t adcRead(uint8_t ch) {
  ADMUX = _BV(REFS0) | (ch & 0x0F);                // AVcc reference
  ADCSRA = _BV(ADEN) | _BV(ADPS2) | _BV(ADPS1) | _BV(ADPS0);
  ADCSRA |= _BV(ADSC); while (ADCSRA & _BV(ADSC)) {}
  return ADC;                                       // reads ADCL then ADCH correctly
}
```

## Timer-triggered sampling with interrupt
```cpp
volatile uint16_t buf[256]; volatile uint8_t idx;
void startSampling() {             // Timer1 compare B at 8 kHz triggers ADC
  ADMUX = _BV(REFS0) | 0; DIDR0 = _BV(ADC0D);
  ADCSRB = _BV(ADTS2) | _BV(ADTS0);                 // Timer1 compare match B
  ADCSRA = _BV(ADEN) | _BV(ADATE) | _BV(ADIE) | _BV(ADPS2) | _BV(ADPS1);  // /64 = 250 kHz
  TCCR1A = 0; TCCR1B = _BV(WGM12) | _BV(CS11);      // CTC, /8 -> 2 MHz
  OCR1A = 249; OCR1B = 249;                         // 8 kHz
  TIMSK1 = 0;
}
ISR(ADC_vect) { buf[idx++] = ADC; TIFR1 = _BV(OCF1B); }   // clear OCF1B so the next match retriggers
```

## Measuring Vcc with the bandgap
Select AVcc as reference and the 1.1 V bandgap as input; `Vcc = 1.1 * 1023 / reading`. Wait ~1 ms
after switching MUX for the bandgap to settle, discard the first conversion. Calibrate the bandgap
per chip (it is 1.0-1.2 V): measure Vcc with a DMM once and store the constant in EEPROM.

## Noise reduction
- `set_sleep_mode(SLEEP_MODE_ADC)` with ADIE set: the CPU sleeps during conversion, removing digital
  noise; wakes on ADC complete.
- 100 nF on AREF, LC filter on AVcc (datasheet recommends 10 uH + 100 nF), source impedance
  <= 10 kOhm.

## Verify
- [ ] Sampling rate measured (toggle a pin in ADC_vect) equals the timer setting.
- [ ] Vcc reading agrees with a DMM within 1% after calibration.
