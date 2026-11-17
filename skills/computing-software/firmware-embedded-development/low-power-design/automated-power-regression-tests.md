---
id: computing-software.firmware-embedded-development.low-power-design.automated-power-regression-tests
name: automated-power-regression-tests
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [power-regression-test, hil-power, ppk2-api, joulescope-api, otii-scripting, ci-power-gate, low-power, firmware-embedded-development]
level: advanced
status: draft
description: "Gate firmware changes on measured power in CI: a HIL rig with a scriptable profiler (PPK2, Joulescope, Otii), test scenarios, limits with tolerance, and trend tracking."
sources:
  - https://github.com/IRNAS/ppk2-api-python
  - https://joulescope.readthedocs.io/en/latest/
  - https://github.com/qoitech/otii-tcp-client-python
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated power regression tests

A one-line change (debug UART left on, sensor not put to sleep) can triple sleep current. Catch it
on the pull request, not in the field.

## Rig
- Scriptable profiler supplying the DUT: Nordic PPK2 (`ppk2-api` Python), Joulescope (`joulescope`
  / `pyjoulescope_driver`), Qoitech Otii (TCP API, Otii Automation Toolbox), or a SMU.
- Probe for flashing that can be electrically disconnected (USB relay/hub with per-port power
  switching such as `uhubctl`, or a relay board on SWD lines).
- Optional GPIO marker from DUT to profiler digital input to align phases.

## Test flow
```python
from ppk2_api.ppk2_api import PPK2_API
ppk = PPK2_API(PPK2_API.list_devices()[0][0])
ppk.get_modifiers(); ppk.use_source_meter(); ppk.set_source_voltage(3000)
flash_firmware(); disconnect_probe()
ppk.toggle_DUT_power("ON"); time.sleep(5)          # boot, settle
ppk.start_measuring(); samples = []
t_end = time.time() + 60
while time.time() < t_end:
    data = ppk.get_data()
    if data: samples += ppk.get_samples(data)[0]   # microamps
    time.sleep(0.01)
ppk.stop_measuring()
avg = sum(samples) / len(samples)
assert avg < LIMIT_UA * 1.10, f"avg {avg:.1f} uA over limit"
```
Scenarios: deep-sleep floor, idle connected (BLE connection interval), periodic job (sensor + TX),
boot energy. Store raw captures as CI artefacts for comparison.

## Limits
- Baseline per scenario per hardware revision; tolerance 5-15% depending on noise.
- Use median or long averages; single samples are noisy.
- Temperature changes leakage; keep the rig in a stable environment or log temperature.

## Trend tracking
Push results to a time-series (CSV in repo, InfluxDB, CI dashboard) keyed by commit. Slow creep
(2% per release) is invisible to a fixed limit but obvious in a trend.

## Gotchas
- The DUT must be fully power-cycled after flashing (debug domain stays powered otherwise).
- USB-connected profilers on a CI host: pin devices by serial, handle reconnects.
- Radio scenarios vary with RF environment; use a shielded box or a fixed central/gateway.

## Verify
- [ ] A deliberately injected regression (UART left enabled) fails the CI job.
- [ ] Repeat runs of the same build agree within the tolerance.
