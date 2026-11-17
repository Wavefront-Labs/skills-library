---
id: creative-arts.design-for-form-and-experience.prototyping.prototyping-with-arduino-and-physical-computing
name: prototyping-with-arduino-and-physical-computing
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [arduino-prototype, physical-computing, arduino, microcontroller-prototype, sensor-prototype, interactive-hardware]
level: practitioner
status: draft
description: "Prototype interactive hardware with Arduino: choose parts, wire a button and LED, read sensors, add outputs, power safely and plan the move to a product design."
sources:
  - "Arduino documentation (arduino.cc)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Physical computing prototypes with Arduino

Arduino boards are microcontrollers with a simple IDE, widely used to prototype interactions with buttons, sensors, lights, motors and displays. Instruction details vary by board; check the documentation for yours.

## Starter workflow
1. **Pick a board** (for example an Uno for learning; a board with built-in wireless for connected prototypes), a breadboard, jumper wires, USB cable.
2. **Install the IDE** and select the right board and port.
3. **Test with a button and an LED:**
```cpp
const int BTN = 2, LED = 13;
void setup() { pinMode(BTN, INPUT_PULLUP); pinMode(LED, OUTPUT); }
void loop() { digitalWrite(LED, digitalRead(BTN) == LOW ? HIGH : LOW); }
```
With `INPUT_PULLUP` the pin reads LOW when the button (wired between the pin and ground) is pressed. Use a resistor (a few hundred ohms) in series with an external LED.
4. **Read an analogue sensor** (a light or distance sensor, potentiometer) with `analogRead()` and print to the Serial Monitor.
5. **Add outputs:** LEDs, a servo (use the Servo library), a buzzer, or a small display.
6. **Map** sensor values to outputs with `map()` and smooth noisy readings by averaging.
7. **Enclose it** (cardboard or a printed shell) and test with real users (see `...prototyping.running-a-prototype-walkthrough-test`).

## Safety and gotchas
- Power motors and long LED strips from a separate supply (with a common ground); do not draw heavy current through the board's pins.
- Do not connect mains voltage; use certified modules and get expert help for anything beyond low voltage.
- Debounce buttons; keep wiring tidy so a loose jumper does not look like a design problem.
- Prototype code and wiring are not production design.

## Verify
- [ ] The button test works before adding anything else.
- [ ] Power for motors is separate and grounds are shared.
- [ ] A sensor-to-output mapping is documented.
