---
id: computing-software.firmware-embedded-development.zephyr.shell-custom-commands
name: shell-custom-commands
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-logging, zephyr-shell, shell-cmd-register, shell-static-subcmd-set-create, shell-backend, shell-print, built-in-shell-commands, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Add a Zephyr shell with custom commands and subcommands for bring-up and field diagnostics, use the built-in device/sensor/i2c/gpio commands, and lock it down for production."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/shell/index.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/shell/shell.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/shell/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/shell/backends/Kconfig.backends
  - https://docs.zephyrproject.org/latest/services/shell/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr shell and custom commands

**Goal:** an interactive console for poking hardware, reading state and changing settings,
using Zephyr's shell subsystem rather than a home-made parser.

## Enable
```
CONFIG_SHELL=y
CONFIG_SHELL_BACKEND_SERIAL=y        # or SHELL_BACKEND_RTT, or a network backend (telnet, ssh, websocket, mqtt)
CONFIG_DEVICE_SHELL=y                # `device list`
CONFIG_I2C=y
CONFIG_I2C_SHELL=y                   # `i2c scan <bus>`
CONFIG_GPIO=y
CONFIG_GPIO_SHELL=y
CONFIG_SENSOR=y
CONFIG_SENSOR_SHELL=y
CONFIG_KERNEL_SHELL=y                # `kernel thread list`, `kernel thread stacks`, `kernel uptime`
```
Other documented groups: `CONFIG_FLASH_SHELL`, `CONFIG_FILE_SYSTEM_SHELL`, `CONFIG_ADC_SHELL` (each needs its
subsystem enabled). Built-ins cover much of board bring-up: scan buses, read sensors, toggle pins, list threads
with stack usage. Run `help` on the target for the exact subcommands of your release.

## Custom commands
```c
#include <zephyr/shell/shell.h>

static int cmd_motor_speed(const struct shell *sh, size_t argc, char **argv) {
    char *end;
    long rpm = strtol(argv[1], &end, 10);
    if (*end || rpm < 0 || rpm > 6000) {
        shell_error(sh, "rpm must be 0..6000");
        return -EINVAL;
    }
    motor_set_rpm(rpm);
    shell_print(sh, "speed set to %ld rpm", rpm);
    return 0;
}
static int cmd_motor_status(const struct shell *sh, size_t argc, char **argv) {
    shell_print(sh, "rpm=%d temp=%d", motor_rpm(), motor_temp());
    return 0;
}
SHELL_STATIC_SUBCMD_SET_CREATE(motor_cmds,
    SHELL_CMD_ARG(speed, NULL, "Set speed <rpm>", cmd_motor_speed, 2, 0),  /* 2 mandatory incl. name */
    SHELL_CMD(status, NULL, "Show status", cmd_motor_status),
    SHELL_SUBCMD_SET_END);
SHELL_CMD_REGISTER(motor, &motor_cmds, "Motor control", NULL);
```
Argument counts are checked by the shell: with the wrong number of arguments it prints an error message
and does not call the handler. Tab completion and help come with the command tree.
Handler return values: 0 success, 1 help printed and command not executed, `-EINVAL` argument validation
failed, `-ENOEXEC` command not executed.

## Practices
- Each shell instance runs in its own thread (`CONFIG_SHELL_STACK_SIZE` sets its stack): keep handlers
  short and hand long work to a work queue.
- Use the handler return codes above for failures.
- Keep a `diag` command group that prints everything support needs in one go.

## Production
- Remove or restrict: `CONFIG_SHELL=n` in release, or keep a minimal set and expose the backend only
  on a debug connector. `CONFIG_SHELL_START_OBSCURED` echoes `*` instead of typed characters (meant for login
  prompts); it is not authentication by itself.
- Shell + logging on the same UART: `CONFIG_SHELL_LOG_BACKEND` (on by default when logging is enabled,
  not in minimal log mode) routes log output through the shell so it does not corrupt the prompt.

## Verify
- [ ] `motor speed 9999` rejected with a clear error; `help motor` lists subcommands.
- [ ] Release build excludes the shell or limits it to a protected interface.

## Checked

Checked 2026-10-26 against the Zephyr shell guide and sources on main: `SHELL_CMD_ARG` /
`SHELL_STATIC_SUBCMD_SET_CREATE` / `SHELL_CMD_REGISTER` argument semantics, handler return codes from
`include/zephyr/shell/shell.h`, backend Kconfig names (serial, RTT, telnet, ssh, websocket, mqtt), `DEVICE_SHELL`,
`I2C_SHELL`, `GPIO_SHELL`, `SENSOR_SHELL`, `KERNEL_SHELL`, `FLASH_SHELL`, `FILE_SYSTEM_SHELL`, `ADC_SHELL`,
`SHELL_STACK_SIZE` (thread per instance), `SHELL_LOG_BACKEND`, `SHELL_START_OBSCURED`. Fixed `kernel threads`/`kernel stacks`
to the documented `kernel thread ...` forms. Removed the Bluetooth NUS backend option and `CONFIG_SHELL_LOGIN`, which
do not appear in the shell Kconfig, and the device-specific command examples.

Method: documentation only; no commands were run.
