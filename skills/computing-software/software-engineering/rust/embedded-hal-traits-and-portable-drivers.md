---
id: computing-software.software-engineering.rust.embedded-hal-traits-and-portable-drivers
name: embedded-hal-traits-and-portable-drivers
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-embedded-nostd, rust-embedded-hal, embedded-hal, drivers, spi, i2c, gpio, hal]
level: advanced
status: docs-checked
description: "Write hardware-independent peripheral drivers against embedded-hal traits (digital, I2C, SPI, delay) and test them on the host with embedded-hal-mock."
sources:
  - https://docs.rs/embedded-hal
  - https://docs.rust-embedded.org/book/
  - https://docs.rs/embedded-hal-mock
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# embedded-hal traits and portable drivers

**Goal:** one sensor driver that works across microcontroller HALs and embedded Linux.

The `embedded-hal` crate holds only blocking traits, in the modules `delay`, `digital`, `i2c`, `pwm` and `spi`. Other execution models live in companion crates: `embedded-hal-async` (async/await) and `embedded-hal-nb` (polling with the `nb` crate). `embedded-hal-bus` provides utilities for sharing SPI and I2C buses. There are no serial traits in `embedded-hal`: use `embedded-io` (byte streams, `no_std` compatible); `embedded-can` covers CAN.

The documented design goals shape how to write a driver: a driver is a library crate generic over the HAL traits, so it supports any target platform (Cortex-M, AVR, embedded Linux, etc.); the HAL erases device-specific details (no registers or magic values in the API); trait methods are fallible, so a driver should surface the HAL error type; and initialisation and pin-conflict configuration are out of scope for the HAL.

Skeleton:

```rust
pub struct Sensor<I2C> { i2c: I2C, addr: u8 }
impl<I2C: embedded_hal::i2c::I2c> Sensor<I2C> {
    pub fn new(i2c: I2C, addr: u8) -> Self { Self { i2c, addr } }
    pub fn release(self) -> I2C { self.i2c }       // give the bus back
    // read/write methods return Result<_, I2C::Error>
}
```

Guidelines: take the bus by value (so users can wrap it with the `embedded-hal-bus` sharing utilities), expose `release()`, keep errors generic over the bus error, accept delays from the caller rather than owning timing, document datasheet units, and keep the crate `no_std`. Add the `embedded-hal` keyword to your crate before publishing so users can find it.

Host testing: `embedded-hal-mock` provides mock implementations of the traits that never touch hardware, so drivers can be tested in CI. Define a list of expected transactions, instantiate the mock with it, run the code, and call `.done()` at the end to assert all expectations were met. Mocks contain an `Arc` and can be cloned, so keep a clone to call `.done()` after handing the original to the driver. Enable the `eh1` feature to mock embedded-hal 1.x (the default is 0.x support only on this page's description; check the feature table for your version).

## Gotchas
- embedded-hal 0.x and 1.x are different trait sets; target one version and make sure the mock crate's feature matches.
- Sensor endianness, sign extension and timing are the usual driver bugs; unit-test them against datasheet examples.

## Verify
Write a mock test with one expected write/read transaction and assert the decoded value matches the datasheet example, then compare against a reference instrument on hardware.

## Checked
Read the docs.rs embedded-hal crate page (modules, companion crates, no serial traits, design goals, keyword advice) and the embedded-hal-mock crate page (transaction expectations, `.done()`, cloneable mocks, `eh0`/`eh1` features). The embedded book landing page was fetched but not used for claims. Removed because not confirmed: the 1.0 release date, specific trait names (InputPin, OutputPin, SpiDevice, SpiBus, DelayNs), `I2cMock`, the TMP102 register arithmetic, `shared-bus`, and the `embedded-hal-compat` shim.

Method: docs-checked 2026-11-09 against docs.rs embedded-hal and embedded-hal-mock crate pages.
