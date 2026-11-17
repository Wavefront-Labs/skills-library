---
id: engineering-technology.invention-prototyping.arduino-prototyping.microcontroller-breadboard-prototyping
name: microcontroller-breadboard-prototyping
category: engineering-technology
field: invention-prototyping
product: arduino-prototyping
tags: [invention-prototyping, arduino-prototyping, arduino, arduino-uno, atmega328p, raspberry-pi, esp32, breadboard, gpio, level-shifting, logic-level, 3v3, 5v, flyback-diode, freewheeling-diode, mosfet, motor-driver, tb6612fng, drv8833, relay, servo, i2c, pull-up, arduino-cli, serial-monitor, demonstrator, maker, physical-computing, sensor-integration]
level: practitioner
status: draft
description: "Build a working Arduino/Raspberry Pi demonstrator: pin current limits, 3.3V/5V level shifting, flyback diodes, motor drivers, arduino-cli build/upload and bring-up tests."
sources: ["Horowitz & Hill, The Art of Electronics (3rd ed.)", "Microchip ATmega328P datasheet (electrical characteristics)", "Raspberry Pi documentation: GPIO and hardware", "Arduino CLI documentation", "Monk, Programming Arduino: Getting Started with Sketches"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Microcontroller breadboard prototyping — a demonstrator that works on the day

**Goal:** wire sensors and actuators to an Arduino or Raspberry Pi so the demonstrator
works on the bench and in the meeting, without cooking a pin or a board.

## 1. Pick the controller by the job
| Need | Choose | Note |
|---|---|---|
| Hard real-time I/O, 5 V parts, instant boot | Arduino Uno/Nano (ATmega328P) | 5 V logic, 10-bit ADC |
| Wi-Fi/BLE, more RAM, 3.3 V sensors | ESP32 / Arduino Nano ESP32 | 3.3 V logic, **not 5 V tolerant** |
| Camera, Linux, Python, UI, networking | Raspberry Pi | 3.3 V GPIO, no ADC, needs clean shutdown |

Common split: Pi for UI, a microcontroller over USB serial for timing-critical I/O.

## 2. Respect the electrical limits (the rules that kill boards)
- **ATmega328P pins:** absolute max 40 mA per pin, design for ≤20 mA; about 200 mA total
  through the chip's VCC/GND pins. An LED gets a resistor: R = (5 V − 2 V) / 0.01 A ≈ 300 Ω,
  so use 330 Ω.
- **Raspberry Pi GPIO:** 3.3 V, never 5 V on an input. Commonly quoted ~16 mA per pin,
  ~50 mA total (unconfirmed; design for a few mA).
- **Other boards differ** (Uno R4, ARM boards are much lower): read that board's datasheet.
- A pin **switches** a load; it never **powers** a motor, relay coil, solenoid or LED strip.

## 3. Level shifting 3.3 V ↔ 5 V
- **5 V output → 3.3 V input:** resistor divider, e.g. 1 kΩ series + 2 kΩ to ground
  (5 V × 2/3 ≈ 3.3 V). Too slow for fast SPI.
- **3.3 V output → 5 V input:** a 5 V AVR reads high above ~0.6 × VCC = 3.0 V, so 3.3 V
  usually works but with little margin. For reliability (and for WS2812 LED data,
  which wants ~0.7 × VCC) use a 74AHCT125 / 74HCT-family buffer powered from 5 V.
- **I²C (bidirectional, open-drain):** BSS138 MOSFET shifter boards or a dedicated
  I²C translator IC. Pull-ups ~4.7 kΩ to each side's own rail for short buses.

## 4. Driving loads
- **Inductive loads (relay coil, solenoid, single-direction motor on a transistor):** a
  **flyback diode** across the load, cathode to the + supply. 1N4148 for small relays, 1N4007
  or a Schottky such as 1N5819 for bigger coils and motors. Without it the turn-off spike
  kills the transistor or resets the MCU.
- **Low-side MOSFET:** pick a *logic-level* part that is fully on at your gate voltage (check
  R_DS(on) is specified at V_GS = 2.5–4.5 V, not only at 10 V). Add a 100–220 Ω gate resistor
  and a 10 kΩ gate-to-ground pull-down so the load stays off during reset and upload.
- **DC motors, both directions:** TB6612FNG or DRV8833-class H-bridges; the old L298N
  drops ~2 V and runs hot.
- **Servos:** separate 5–6 V supply sized for stall current (often ≥1 A each) and a
  470–1000 µF capacitor across the servo rail.
- **Common ground** between every supply and the controller, always.

## 5. Build and upload from the command line (arduino-cli)
```bash
arduino-cli config init
arduino-cli core update-index
arduino-cli core install arduino:avr          # ESP32: add its board-manager URL first
arduino-cli board list                        # find the port, e.g. /dev/ttyACM0 or COM3
arduino-cli lib install "Servo"
arduino-cli compile --fqbn arduino:avr:uno MySketch
arduino-cli upload  -p <PORT> --fqbn arduino:avr:uno MySketch
arduino-cli monitor -p <PORT> -c baudrate=115200
```
Record core and library versions next to the sketch so the build is reproducible.

## 6. Bring-up order
1. Power only, controller unplugged: meter each rail.
2. Controller alone: blink plus a serial "hello".
3. Add one peripheral at a time with its own test sketch (I²C scanner for I²C parts).
4. Integrate; replace `delay()` with `millis()`-based timing so inputs stay responsive.

## Gotchas
- Power rails on full-length breadboards are often split in the middle — bridge them.
- Floating inputs read random values: use `INPUT_PULLUP` and switch to ground.
- USB power (~500 mA) browns out when a motor starts; the symptom is random resets.
- Pins 0/1 on the Uno are the USB serial line — wiring to them breaks upload.
- Jumper wires loosen in transport: move demos to stripboard or a screw-terminal shield.
- Pi SD cards corrupt when power is yanked — shut down properly.

## Verify
- [ ] Every pin's current is under its datasheet limit with margin.
- [ ] No 5 V signal reaches a 3.3 V-only input (checked with a meter, not assumed).
- [ ] Every inductive load has a correctly oriented flyback diode or a driver with one built in.
- [ ] A clean compile and upload with arduino-cli works from a fresh checkout.
- [ ] The demo survives 30 minutes powered and a gentle shake test without a reset.
