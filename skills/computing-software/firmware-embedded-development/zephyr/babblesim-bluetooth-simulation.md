---
id: computing-software.firmware-embedded-development.zephyr.babblesim-bluetooth-simulation
name: babblesim-bluetooth-simulation
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [babblesim, bsim, nrf52-bsim, phy-simulation, bluetooth-ci-testing, zephyr, firmware-embedded-development]
level: sme
status: docs-checked
description: "Simulate multi-device Bluetooth LE systems with BabbleSim and the nrf52_bsim/nrf5340bsim boards: setup, building devices, running a simulation, and CI tests."
sources:
  - https://docs.zephyrproject.org/latest/develop/test/bsim.html
  - https://babblesim.github.io/
  - https://docs.zephyrproject.org/latest/boards/native/nrf_bsim/doc/nrf52_bsim.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BabbleSim

BabbleSim simulates the radio medium between devices; the `nrf52_bsim` / `nrf5340bsim` boards
run the real Zephyr BLE stack and the real nRF link-layer controller on the host, with models of
nRF peripherals. Multiple device executables talk through a simulated PHY, in simulated time, so
tests are fast and deterministic.

## Setup
```bash
west config manifest.group-filter -- +babblesim
west update
cd ${ZEPHYR_BASE}/../tools/bsim
make everything -j 8
export BSIM_OUT_PATH=${ZEPHYR_BASE}/../tools/bsim
export BSIM_COMPONENTS_PATH=${BSIM_OUT_PATH}/components/
```
The bsim boards build Linux executables and need the host 32-bit C library (see the POSIX
architecture dependencies in the Zephyr docs).

## Build two devices
```bash
west build -b nrf52_bsim -d build_periph samples/bluetooth/peripheral_hr
west build -b nrf52_bsim -d build_central samples/bluetooth/central_hr
cp build_periph/zephyr/zephyr.exe  $BSIM_OUT_PATH/bin/bs_nrf52_periph
cp build_central/zephyr/zephyr.exe $BSIM_OUT_PATH/bin/bs_nrf52_central
```

## Run a simulation
```bash
cd $BSIM_OUT_PATH/bin
./bs_nrf52_periph  -s=hr_sim -d=0 &
./bs_nrf52_central -s=hr_sim -d=1 &
./bs_2G4_phy_v1    -s=hr_sim -D=2 -sim_length=20e6     # 2 devices, 20 s simulated
```
`-s` is the simulation id (shared), `-d` the device number, `-D` the device count and
`-sim_length` the length in microseconds. Devices and the Phy accept many more switches; run
them with `-help`.

## Tests in tree
Zephyr's `tests/bsim/` folder holds self-checking test applications that report pass or fail
through the `bs_tests` system, each with a shell script in `tests_scripts/` that launches the
devices and the Phy and returns 0 on success. Run them with twister and the bsim harness
(`twister -p nrf52_bsim/native -T tests/bsim/bluetooth/host/adv/chain/ --fixture bsim_multi_test`),
or with the legacy `tests/bsim/compile.sh` and `tests/bsim/run_parallel.sh` scripts. Use them
as templates for product tests.

## When to use
- CI for BLE application logic and multi-device interactions without radios.
- Reproducing timing-dependent bugs deterministically (same seed, same result).
- Not for RF performance: the Phy is a simulation, and the bsim boards model specific SoCs
  (nrf52_bsim, nrf5340bsim, nrf54l15bsim).

## Verify
- [ ] Two-device simulation completes with the expected PASS from each device.
- [ ] CI job caches the BabbleSim build and runs bsim tests per PR.

## Checked

Checked 2026-10-25 against the Zephyr documentation source (main, latest release v4.4.2): doc/develop/test/bsim.rst and boards/native/nrf_bsim/doc/nrf52_bsim.rst.
Confirmed: `west config manifest.group-filter -- +babblesim`, `west update`, `make everything -j 8`; `BSIM_OUT_PATH`/`BSIM_COMPONENTS_PATH`; the 32-bit host C library requirement; the device and Phy switches `-s`, `-d`, `-D`, `-sim_length`; `bs_2G4_phy_v1`; the `bs_tests` system, `tests/bsim/`, `--fixture bsim_multi_test`, and the legacy `compile.sh`/`run_parallel.sh` scripts.

Method: documentation only; no commands were run.
