---
id: computing-software.firmware-embedded-development.arduino.arduino-library-api-style
name: arduino-library-api-style
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-api-style, library-design, begin-method, stream-print-inheritance, camelcase-api, wire-instance, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Design Arduino libraries the Arduino way: begin()/end(), camelCase verbs, inheriting Stream/Print, passing TwoWire/SPIClass instances, non-blocking calls, safe defaults."
sources:
  - https://github.com/arduino/docs-content/blob/main/content/learn/08.contributions/01.arduino-library-style-guide/arduino-library-style-guide.md
  - https://github.com/arduino/ArduinoCore-API/blob/master/api/Print.h
  - https://github.com/arduino/ArduinoCore-API/blob/master/api/Stream.h
  - https://github.com/arduino/reference-en/blob/master/Language/Functions/Communication/SPI/beginTransaction.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arduino API style for libraries

The Arduino style guide favours APIs a beginner can read aloud. Follow it so your library feels
native and works across cores.

## Shape of the class
```cpp
class Bme {
public:
  explicit Bme(TwoWire &wire = Wire, uint8_t address = 0x76);
  bool begin();                      // init hardware; return false on failure, never hang
  void end();
  float readTemperature();           // verbs: read/write/set/get/is/available
  bool  isConnected();
  void  setSampling(Sampling s);
private:
  TwoWire &_wire; uint8_t _addr;
};
```
- Use `begin()` to initialise a library instance and `end()` to stop it (style guide). Practice: keep
  hardware access out of the constructor so global objects are safe, and return `bool` (or an error
  code) from `begin()` so sketches can report "sensor not found".
- Accept bus instances (`TwoWire&`, `SPIClass&`, `Stream&`) by reference with defaults (`Wire`, `SPI`);
  the style guide asks for any `Stream` object to be accepted rather than hard-coding `Serial`.
- Name functions in camelCase with clear everyday words and avoid pointers in the public API
  (style guide); document the unit of returned values.

## Streams and printing
- Libraries that provide byte-stream communication should inherit `Stream` (`available()`, `read()`,
  `peek()`, `write()`), so the print and parse functions work; buffer incoming data so `read()` does not wait.
- Output-only devices (displays) can inherit `Print` and implement `write(uint8_t)`, optionally
  overriding the buffer overload.

## Behaviour rules
- Practice: no unbounded waits; poll with timeouts based on `millis()` and expose non-blocking variants
  (`startMeasurement()` / `isReady()` / `getResult()`).
- Practice: do not call `Serial.begin()` or print from inside the library unless the user passes a debug `Stream`.
- Practice: keep RAM use small and let users override buffer sizes.
- Practice: document any change to shared bus settings (for example `Wire.setClock`), and wrap SPI access
  in `SPI.beginTransaction(SPISettings(...))` / `endTransaction()`.
- Check `ARDUINO_ARCH_*` macros only where needed and list supported `architectures` in
  `library.properties`.

## Examples and docs
Ship examples that compile on every listed architecture (CI with `arduino/compile-sketches`), a
`keywords.txt`, and a README showing wiring and the minimal sketch.

## Verify
- [ ] A global instance works on every listed architecture (no hardware access before `begin`).
- [ ] Library examples pass `arduino-lint --library-manager update`.

## Checked

Date: 2026-10-25. Documentation release: Arduino library style guide (docs-content main) and ArduinoCore-API master.

Confirmed from the style guide: use `begin()` to initialise a library instance and `end()` to stop it; camelCase function names; `read()`/`write()` verbs; use `Stream` and `Print` for byte streams, and inherit `Stream` for byte-stream libraries; let the user pass any `Stream` object by reference rather than hard-coding `Serial`; avoid requiring pointers in the API; `Client` and `Server` as the basis for network libraries. From ArduinoCore-API: `Print` requires `write(uint8_t)` and offers a buffer overload; `Stream` adds `available()`, `read()`, `peek()` and the parse functions. The remaining guidance below is engineering practice, not a quotation of the style guide, and contains no version-specific claims; `SPI.beginTransaction` is documented in the Arduino language reference.

Method: documentation only; no commands were run.
