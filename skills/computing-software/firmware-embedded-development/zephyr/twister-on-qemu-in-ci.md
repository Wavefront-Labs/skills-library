---
id: computing-software.firmware-embedded-development.zephyr.twister-on-qemu-in-ci
name: twister-on-qemu-in-ci
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [qemu-testing, twister-ci, qemu-cortex-m3, zephyr-ci-container, twister-shards, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run Zephyr twister test suites on QEMU and native_sim in CI: emulated platforms, the zephyr CI container, sharding with --subset, retries, and reports."
sources:
  - https://docs.zephyrproject.org/latest/develop/twister/index.html
  - https://github.com/zephyrproject-rtos/docker-image
  - https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/qemu
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/pylib/twister/twisterlib/environment.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Twister on QEMU in CI

## Platforms that run without hardware
| Platform | Arch | Notes |
|---|---|---|
| `native_sim` (and `native_sim/native/64`) | host | runs as a host process; Address Sanitizer via `CONFIG_ASAN` |
| `qemu_cortex_m3`, `qemu_cortex_m0` | Arm Cortex-M | |
| `mps2/an385`, `mps2/an521/cpu0` | Arm Cortex-M (QEMU `mps2` machines) | |
| `qemu_x86`, `qemu_x86_64` | x86 | |
| `qemu_riscv32`, `qemu_riscv64` | RISC-V | |
| `qemu_cortex_a53` | ARM64 | |

The Zephyr SDK ships host tools including a custom QEMU. Board directories exist under `boards/qemu`
and `boards/arm/mps2` in the Zephyr tree; check the board's `.yaml` for the exact identifier and
supported toolchains in your release.

## GitHub Actions example
```yaml
jobs:
  twister:
    runs-on: ubuntu-24.04
    container: ghcr.io/zephyrproject-rtos/ci:<tag>      # pin a tag (see Zephyr's own workflows)
    strategy:
      matrix: { subset: [1, 2, 3, 4] }
    steps:
      - uses: actions/checkout@v4
        with: { path: app }
      - run: |
          west init -l app && west update -o=--depth=1 -n
          west zephyr-export
      - run: |
          ./zephyr/scripts/twister -T app/tests \
            -p native_sim -p qemu_cortex_m3 \
            --subset ${{ matrix.subset }}/4 \
            --inline-logs --retry-failed 2 -j $(nproc) \
            --outdir twister-out
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: twister-${{ matrix.subset }}, path: "twister-out/*.xml\ntwister-out/twister.json" }
```

## Useful flags
- `--subset N/M`: deterministic sharding across jobs.
- `--integration`: only `integration_platforms` from each testcase.yaml (fast PR runs).
- `--retry-failed 2`: absorb occasional emulator timing flakes; investigate repeats.
- `--inline-logs`: print failing logs into CI output.
- `--timeout-multiplier 2`: slow runners.
- `-c` / `--clobber-output` controls cleaning of the output directory; `--only-failed` re-runs
  failures from a previous run.
- Reports in the output directory: `twister.json`, `testplan.json`, `twister.xml` (JUnit
  summary), `twister_report.xml` (JUnit, all test cases) and a per-suite JUnit report.

## Writing QEMU-friendly tests
- Avoid tight real-time assertions. `CONFIG_QEMU_ICOUNT` gives deterministic guest time (it
  defaults to `y` unless networking or Bluetooth is enabled); otherwise use generous tolerances.
- Hardware-specific tests: `platform_allow`/`depends_on` features so twister filters them out of
  emulators.
- Use emulated buses and drivers (for example the `zephyr,i2c-emul-controller` devicetree
  binding) on `native_sim`. `--emulation-only` restricts a run to emulation platforms.

## Verify
- [ ] PR pipeline runs the `--integration` subset; nightly runs the full matrix.
- [ ] JUnit XML published so failures show per test in the CI UI.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed twister options --subset (-B), --integration (-G), --inline-logs, --retry-failed, --timeout-multiplier, --only-failed, --emulation-only, --clobber-output (twisterlib/environment.py), the report file list (twister page), board directories for the QEMU and mps2 platforms, CONFIG_QEMU_ICOUNT default (boards/Kconfig), and the i2c emulator binding. Wrong in the draft: -M is --runtime-artifact-cleanup, not --clobber-output. Replaced the unverifiable pinned CI image tag with a placeholder and removed unsupported platform notes.
Method: documentation only; no commands were run.
