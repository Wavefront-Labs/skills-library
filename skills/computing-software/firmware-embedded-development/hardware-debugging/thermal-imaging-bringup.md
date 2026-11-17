---
id: computing-software.firmware-embedded-development.hardware-debugging.thermal-imaging-bringup
name: thermal-imaging-bringup
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [thermal-imaging, thermal-camera, short-circuit-finding, hot-spot, emissivity, power-dissipation, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Use a thermal camera in bring-up: find shorts by current-limited injection, spot parts heated by firmware mistakes, emissivity pitfalls, heat vs firmware state."
sources:
  - https://en.wikipedia.org/wiki/Thermography
  - https://www.fluke.com/en-us/learn/blog/thermal-imaging/how-to-use-a-thermal-camera-for-electrical-inspections
  - https://www.analog.com/en/resources/technical-articles/thermal-characterization-of-ic-packages.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thermal imaging during bring-up

A thermal camera (FLIR, InfiRay/Hikmicro, Seek; phone add-ons work) shows in seconds which part is
dissipating power. Pair it with a current-limited bench supply.

## Finding a short
1. Rail shorted (supply goes into current limit). Set the limit to a safe value (start ~0.5 A),
   voltage to at most the rail's nominal.
2. Inject into the shorted rail and watch the image. The shorted capacitor, solder bridge or dead
   IC lights up first. Raise current slowly; ceramic caps get very hot at 1-2 A.
3. Nothing visible: try a lower voltage with higher current (the short may be low resistance) or
   inject into a different point.

## Firmware-caused heat
- **GPIO contention:** an output driving against another output or a shorted net; the MCU or the
  other driver shows a hot spot after the pin is configured. Reset the MCU: it cools, configure:
  it heats.
- **Regulator in dropout or overloaded** because firmware enabled loads together (radio + motor).
- **LED/heater/motor drivers** left at 100% duty by a stuck PWM.
- **Back-powering:** an I/O drives a powered-down chip that warms through its ESD diodes.
- **Peripheral not entering sleep:** a sensor or PHY still warm when the system should idle.
Correlate by toggling firmware states with a shell command while watching the image.

## Measurement pitfalls
- Emissivity: shiny metal (shields, bare copper, tin leads) reflects and reads cold/wrong. Apply
  Kapton or matt black tape/paint (e ~0.95) for absolute readings.
- Spatial resolution: a cheap 80x60 sensor cannot resolve a 0402 part at 30 cm; use a macro lens
  or get closer.
- Thermal time constants: small parts heat in seconds, large ones in minutes; wait for steady
  state before comparing.
- Read package temperature, then estimate junction temperature: Tj = Tcase + P x theta_JC
  (or psi_JT from the datasheet).

## Verify
- [ ] Short found and confirmed by removing the hot component and measuring resistance.
- [ ] Steady-state temperatures of regulators and MCU recorded at worst-case firmware load.
