---
id: computing-software.firmware-embedded-development.device-driver-development.linux-pwm-subsystem
name: linux-pwm-subsystem
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-pwm, linux-driver-subsystem, pwm-chip, pwm-state, sysfs-pwm, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use and implement Linux PWM: consumers with devm_pwm_get and pwm_apply_might_sleep, provider drivers with the .apply/.get_state ops, DT pwms cells, and sysfs testing."
sources:
  - https://docs.kernel.org/driver-api/pwm.html
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/pwm/pwm.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PWM subsystem

## Consumer side
```dts
backlight { compatible = "pwm-backlight"; pwms = <&pwm1 0 50000 0>; /* chan, period ns, flags (PWM_POLARITY_INVERTED) */
            brightness-levels = <0 4 8 16 32 64 128 255>; default-brightness-level = <6>; };
fan { compatible = "pwm-fan"; pwms = <&pwm2 1 40000 0>; };
```
Prefer generic consumers (`pwm-backlight`, `pwm-fan`, `pwm-leds`, `pwm-beeper`, `pwm-ir-tx`).
In a custom driver:
```c
struct pwm_device *pwm = devm_pwm_get(dev, NULL);
struct pwm_state st;
pwm_init_state(pwm, &st);                 /* period/polarity from DT */
pwm_set_relative_duty_cycle(&st, 30, 100);
st.enabled = true;
ret = pwm_apply_might_sleep(pwm, &st);    /* pwm_apply_atomic() is the variant usable from atomic context */
```
Atomic state application changes period, duty and polarity together, avoiding glitches from
separate calls (`pwm_config` + `pwm_enable` are legacy).

## Provider side (PWM controller driver)
```c
static int acme_pwm_apply(struct pwm_chip *chip, struct pwm_device *pwm, const struct pwm_state *st) {
    if (st->polarity != PWM_POLARITY_NORMAL) return -EINVAL;
    if (!st->enabled) { acme_disable(chip, pwm->hwpwm); return 0; }
    u64 cycles = mul_u64_u64_div_u64(clk_rate, st->period, NSEC_PER_SEC);  /* round down */
    ...
}
static const struct pwm_ops acme_pwm_ops = { .apply = acme_pwm_apply, .get_state = acme_pwm_get_state };
chip = devm_pwmchip_alloc(dev, npwm, sizeof(*priv));
chip->ops = &acme_pwm_ops;
ret = devm_pwmchip_add(dev, chip);
```
Newer providers can instead implement the waveform ops (`round_waveform_tohw`,
`round_waveform_fromhw`, `read_waveform`, `write_waveform`) listed in `struct pwm_ops`.
Values are usually rounded **down** to the nearest achievable value (core.c), and `.get_state`
lets the kernel read the bootloader's configuration to avoid glitches (pwm.rst).
`CONFIG_PWM_DEBUG` enables additional checks of the low-level driver callbacks.

## Sysfs testing
```sh
echo 0 > /sys/class/pwm/pwmchip0/export
echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/period        # ns
echo 250000  > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable
cat /sys/kernel/debug/pwm
```

## Verify
- [ ] Scope confirms period/duty for several settings, including 0% and 100%.
- [ ] `CONFIG_PWM_DEBUG` reports no rounding/state warnings.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/driver-api/pwm.rst and include/linux/pwm.h: pwm_apply_might_sleep, pwm_apply_atomic (usable from atomic context), pwm_init_state, pwm_set_relative_duty_cycle, devm_pwmchip_alloc, devm_pwmchip_add, struct pwm_ops with .apply, .get_state and the waveform ops, and that .get_state exists so drivers avoid glitches. Confirmed in drivers/pwm/core.c: waveform values are usually rounded down to the nearest possible value. Confirmed in drivers/pwm/Kconfig: PWM_DEBUG enables additional checks for low-level driver authors. Removed the unconfirmed version gates (6.8, 6.9) and the "PWM maintainers" rule list. The mul_u64_u64_div_u64 provider snippet is illustrative and was not checked.

Method: documentation only; no commands were run.
