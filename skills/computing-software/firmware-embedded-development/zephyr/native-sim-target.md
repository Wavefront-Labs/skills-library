---
id: computing-software.firmware-embedded-development.zephyr.native-sim-target
name: native-sim-target
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [twister, native-sim, host-build, posix-arch, asan, simulated-flash, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build and run Zephyr apps as Linux executables with native_sim: command-line options, pty UARTs, simulated flash, networking and BLE, debugging with gdb, ASan and Valgrind."
sources:
  - https://docs.zephyrproject.org/latest/boards/native/native_sim/doc/index.html
  - https://docs.zephyrproject.org/latest/develop/test/twister.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/flash/flash_simulator.c
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/serial/uart_native_pty.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# native_sim target

`native_sim` compiles Zephyr plus your app into a normal Linux executable. The kernel,
threads, timers and many drivers run unmodified, so most logic can be developed and tested
without hardware. It is the evolution of `native_posix`, which is no longer in the Zephyr tree.

## Build and run
```bash
west build -b native_sim app            # 32-bit (ILP32) binary: needs multilib or a 32-bit userspace
west build -b native_sim/native/64 app  # 64-bit (LP64) variant, for hosts that cannot run 32-bit binaries
west build -t run                        # or: ./build/zephyr/zephyr.exe
./build/zephyr/zephyr.exe --help         # all simulator options
./build/zephyr/zephyr.exe --seed=1234    # seed for the random number generator
```
It builds a Linux executable for the host (typically x86); run it in a Linux environment. The
kernel keeps running in the idle loop after `main()` returns, so stop it with Ctrl+C, call
`nsi_exit(status)` under `#ifdef CONFIG_ARCH_POSIX`, or use ztest, which exits after the tests.

## Time
By default simulated time runs decoupled from host time, as fast as the host allows, so a test that
sleeps for an hour finishes in seconds. `--rt` slows it to real time (needed when interacting with
external programs; `--no-rt` is the opposite and `CONFIG_NATIVE_SIM_SLOWDOWN_TO_REAL_TIME` sets the
default); `--rt-ratio=2` makes simulated time run at twice real time.

## Peripherals
- **Console/log** to stdout by default.
- **UART**: the PTY driver (`UART_NATIVE_PTY`) creates a pseudo-terminal or uses stdin/stdout.
  `--attach_uart` / `--attach_uart_cmd=<cmd>` attach a terminal to every PTY UART (e.g. for the
  shell); per-instance forms are prefixed with the device name (the manual's example is
  `--uart_attach_uart_cmd`, with `%s` replaced by the PTY path). A TTY driver (`UART_NATIVE_TTY`)
  talks to host serial ports.
- **Flash**: the flash simulator keeps its content in a file (default `flash.bin` in the working
  directory, `--flash=<path>` to change it, `--flash_erase` to erase at start, `--flash_rm` to
  delete it at exit) so NVS/LittleFS/settings persist between runs.
- **GPIO/I2C/SPI**: emulators (see driver-emulators-for-testing).
- **Networking**: TAP interface via `CONFIG_ETH_NATIVE_TAP` (Linux hosts only; set up with Zephyr's
  `net-tools`), or `CONFIG_NET_NATIVE_OFFLOADED_SOCKETS` to use host sockets directly.
- **Bluetooth**: HCI over a real controller with `CONFIG_BT_USERCHAN` (`--bt-dev=hci0`, needs
  root; a TCP HCI server can be given as `--bt-dev=<ip>:<port>`), or fully simulated with
  BabbleSim boards (`nrf52_bsim`, `nrf5340bsim`).

## Debugging
It's a host process: use `gdb ./build/zephyr/zephyr.exe` directly, with breakpoints in
threads, no probe needed.
```
CONFIG_ASAN=y        # AddressSanitizer: out-of-bounds, use-after-free
CONFIG_UBSAN=y       # undefined behaviour
```
The manual says the executable can also be run with `valgrind`. For gcov coverage see the
"coverage reports using the POSIX architecture" section of the Zephyr documentation.

## Limits
- Not cycle-accurate: no timing validation, no ISR latency, no real cache/MPU behaviour.
- Architecture-specific code (inline asm, CMSIS register access) must be stubbed or
  excluded with `#ifdef CONFIG_ARCH_POSIX`.
- Different `sizeof(long)` and pointer size on the 64-bit variant can hide or expose bugs;
  CI on both variants is cheap.

## Verify
- [ ] App/unit tests run on native_sim in CI via twister.
- [ ] Flash-backed features tested across simulated reboots with `--flash` files.
- [ ] ASan build runs the test suite clean.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in the native_sim page and driver sources: ILP32 `native_sim` versus LP64 `native_sim/native/64` and the multilib/32-bit-userspace requirement; `--help`, `--seed`, `--rt`, `--no-rt`, `--rt-ratio`, CONFIG_NATIVE_SIM_SLOWDOWN_TO_REAL_TIME; the process does not exit after main and `nsi_exit()` under CONFIG_ARCH_POSIX; UART_NATIVE_PTY and UART_NATIVE_TTY with `--attach_uart`, `--attach_uart_cmd` and per-instance prefixed options; flash simulator `flash.bin` default, `--flash`, `--flash_erase`, `--flash_rm`; ETH_NATIVE_TAP (Linux only), NET_NATIVE_OFFLOADED_SOCKETS, BT_USERCHAN and `--bt-dev`; CONFIG_ASAN and CONFIG_UBSAN; valgrind mention; `nrf52_bsim` and `nrf5340bsim` boards; native_posix is gone from the tree.
Removed: the `--stop_at` option and the Windows/macOS/WSL2 statement, which the manual does not document; the `--uart_stdinout` option name was replaced with the documented option names.

Method: documentation only; no commands were run.
