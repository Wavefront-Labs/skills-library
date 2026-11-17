---
id: computing-software.firmware-embedded-development.device-driver-development.i2c-sensor-driver-from-datasheet
name: i2c-sensor-driver-from-datasheet
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [i2c, iic, twi, smbus, sensor-driver, device-driver, datasheet, register-map, who-am-i, 7-bit-address, 8-bit-address, repeated-start, endianness, twos-complement, pull-up-resistors, clock-stretching, bus-recovery, sda-stuck-low, hal-abstraction, dependency-injection, logic-analyzer, imu, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write a portable I2C sensor driver from a datasheet: address formats, register reads with repeated start, WHO_AM_I checks, endian/two's-complement conversion, stuck-bus recovery."
sources:
  - https://www.nxp.com/docs/en/user-guide/UM10204.pdf
  - https://www.ti.com/lit/an/slva704/slva704.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# I2C sensor driver from a datasheet: portable, testable, bus-safe

**Goal:** turn a sensor datasheet into a small driver that works on any MCU, proves it is
talking to the right chip, converts raw registers to correct physical units, and recovers when
the bus hangs.

## 1. Read the datasheet in this order
1. **Electrical / I2C section:** supported speeds (UM10204: Standard 100 kHz, Fast 400 kHz,
   Fast-mode Plus 1 MHz), the address and the pin that selects it, whether the part stretches the
   clock, max bus capacitance.
2. **Register map:** ID register (`WHO_AM_I`) and its expected value, config registers and reset
   values, data registers and their byte order, auto-increment rules for burst reads.
3. **Power-up sequence:** time after power-on before the first access, soft-reset command and
   delay after it, measurement time per mode.
4. **Data format and scale:** signed or unsigned, bits used, LSB per unit at each range setting.

## 2. Addresses: 7-bit vs 8-bit
An I2C target address is 7 bits, followed by an eighth bit R/W (0 = write, 1 = read) in the first
byte after START (UM10204 section 3.1.10). So the byte on the wire is `(addr << 1) | R/W`.
Datasheets sometimes print the 8-bit write address (for example 0xD0 for a 0x68 device), and
driver APIs differ on which form they expect; check your HAL's documentation. A wrong shift shows
up as a NACK on the address byte. Two groups of eight addresses (0000 XXX and 1111 XXX) are
reserved (UM10204 Table 4), so a scanner only needs to probe 0x08 to 0x77.

## 3. The register read: write pointer, repeated start, read
The combined format (UM10204 section 3.1.10) changes direction within one transfer by repeating
START and the target address with the R/W bit reversed, and UM10204 gives serial memory access as
its example: write the internal location first, then repeat START and read. For a register read:
START, addr+W, register, **repeated START**, addr+R, N bytes, STOP. The controller-receiver
acknowledges every byte except the last, and sends a NACK just before the STOP or repeated START.
Use the combined transfer your HAL provides rather than a STOP between the two halves; whether a
given part tolerates a STOP there is a datasheet question. UM10204 note 2 leaves auto-increment
behaviour to the device designer, so confirm in the datasheet that a burst read advances the
register pointer.

## 4. A HAL-agnostic interface
```c
typedef struct {
    int  (*write_read)(void *ctx, uint8_t addr7, const uint8_t *w, size_t wn, uint8_t *r, size_t rn);
    void (*delay_ms)(void *ctx, uint32_t ms);
    void *ctx;
    uint8_t addr7;
} sens_t;

int sens_read_regs(sens_t *d, uint8_t reg, uint8_t *buf, size_t n) {
    return d->write_read(d->ctx, d->addr7, &reg, 1, buf, n);
}
int sens_init(sens_t *d) {
    uint8_t id;
    if (sens_read_regs(d, REG_WHO_AM_I, &id, 1)) return -EIO;
    if (id != WHO_AM_I_VALUE) return -ENODEV;       // wrong chip or wrong address
    /* soft reset, wait datasheet time, write config, read it back */
    return 0;
}
```
The platform supplies `write_read`; the driver never includes a vendor header, so the
conversions can be unit-tested on a host with a fake bus. Return an error code from every call
and never ignore a NACK. UM10204 section 3.1.6 lists why a NACK happens: no device at that
address, a device busy with a real-time function, data it does not understand, or a receiver that
cannot take more bytes.

## 5. Converting raw data
```c
int16_t raw = (int16_t)((uint16_t)buf[0] << 8 | buf[1]);  // big-endian, signed 16-bit
float g = raw / 16384.0f;                                 // only if the datasheet says 16384 LSB/g
```
- Take byte order and the LSB-per-unit scale from the datasheet for each register and range
  setting; never assume them.
- Assemble in `uint16_t`, then cast to `int16_t`, so a signed `char` is not sign-extended.
- Values narrower than the register (12 or 20 bits) need sign extension of the top used bit.
- If the datasheet defines calibration coefficients, read them once at init and apply its
  compensation formula with the integer widths it specifies.

## 6. Bus problems
- **Pull-ups:** SDA and SCL are open-drain, so external pull-ups are required. See
  `i2c-pull-up-resistor-sizing` for the UM10204 rise-time and sink-current limits.
- **Clock stretching:** a target may hold SCL low to make the controller wait (UM10204 3.1.9), but
  most targets cannot, since they have no SCL driver. If your sensor does stretch, make sure the
  controller peripheral supports it.
- **Stuck bus:** if SCL is stuck low, UM10204 3.1.16 prefers the hardware reset input of the
  devices, otherwise cycling power. If SDA is stuck low, the controller should send nine clock
  pulses, and the device holding the bus should release it within those nine clocks; if it does
  not, use hardware reset or cycle power. Implement the nine pulses by switching SCL to a GPIO,
  then reinitialise the I2C peripheral.
- Put a logic analyser with an I2C decoder on the bus during bring-up; it separates "NACK" from
  "wrong data" quickly.

## Verify
- [ ] Scanner finds the device at the expected 7-bit address; the driver uses the address form your HAL expects.
- [ ] `sens_init` returns `-ENODEV` when the address is deliberately wrong.
- [ ] Host unit tests cover sign and endianness conversion with known raw bytes (0xFF 0xFF gives -1).
- [ ] Readings at rest match physics (about 1 g on the vertical axis, plausible room temperature).
- [ ] With SDA held low, the nine-clock recovery restores communication.
- [ ] Logic-analyser capture shows a repeated start, not a STOP, between register write and read.

## Checked
2026-11-09. Read: NXP UM10204 Rev 7.0 (sections 3.1.6 NACK causes, 3.1.9 clock stretching,
3.1.10 address and R/W bit, combined format and its notes, Table 4 reserved addresses, 3.1.16 bus
clear) and the TI SLVA704 text on the ACK/NACK clock period. Removed: STM32 HAL, Linux and Zephyr
function names and shift behaviour, the claim that some parts reset their pointer or lose the
FIFO on a STOP, latch-on-first-byte behaviour, endianness generalisations about vendors, internal
pull-up values and the 2.2 to 10 kOhm range, Raspberry Pi stretching errata, the 20-bit
shift-based sign extension snippets, the PlatformIO cross-reference, and the docs.kernel.org
source (index page only, not used).
Method: docs-checked 2026-11-09 against UM10204 Rev 7.0 and TI SLVA704.
