---
id: computing-software.firmware-embedded-development.zephyr.shell-subcommands-and-dynamic-commands
name: shell-subcommands-and-dynamic-commands
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [shell-subcommands, shell-dynamic-cmd-create, shell-cmd-arg, shell-subcmd-add, dictionary-commands, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build multi-level Zephyr shell command trees: static subcommand sets, argument counts, runtime dynamic commands, SHELL_SUBCMD_ADD from other files, and dictionary commands."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/shell/index.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/shell/shell.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/shell/Kconfig
  - https://docs.zephyrproject.org/latest/services/shell/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shell subcommands and dynamic commands

## Static tree with argument checking
```c
#include <zephyr/shell/shell.h>

static int cmd_led_on(const struct shell *sh, size_t argc, char **argv)
{
    int idx = atoi(argv[1]);
    shell_print(sh, "LED %d on", idx);
    return 0;
}

static int cmd_led_set(const struct shell *sh, size_t argc, char **argv)
{
    /* argv[1] = index, argv[2] = brightness */
    return 0;
}

SHELL_STATIC_SUBCMD_SET_CREATE(sub_led,
    SHELL_CMD_ARG(on,  NULL, "Turn LED on: led on <idx>", cmd_led_on, 2, 0),
    SHELL_CMD_ARG(set, NULL, "led set <idx> <0-255>",    cmd_led_set, 3, 0),
    SHELL_SUBCMD_SET_END
);
SHELL_CMD_REGISTER(led, &sub_led, "LED control", NULL);
```
`SHELL_CMD_ARG(name, subcmds, help, handler, mandatory, optional)`: `mandatory` counts the
command itself, so `2` means one required argument. With the wrong number of arguments the shell prints an
error message and does not call the handler, so handlers can index `argv` up to the mandatory count.

## Dynamic commands (completion from runtime data)
```c
static void dev_name_get(size_t idx, struct shell_static_entry *entry)
{
    const struct device *dev = nth_ready_device(idx);   /* your enumerator */
    entry->syntax  = dev ? dev->name : NULL;            /* syntax must be NULL when there are no more entries */
    entry->handler = NULL;
    entry->help    = "device";
    entry->subcmd  = NULL;
}
SHELL_DYNAMIC_CMD_CREATE(dsub_dev, dev_name_get);

SHELL_STATIC_SUBCMD_SET_CREATE(sub_sensor,
    SHELL_CMD_ARG(read, &dsub_dev, "sensor read <device>", cmd_sensor_read, 2, 0),
    SHELL_SUBCMD_SET_END);
```
Tab completion now lists current device names.

## Extending a command from another file
```c
/* in led.c */
SHELL_SUBCMD_SET_CREATE(app_cmds, (app));          /* section-based set */
SHELL_CMD_REGISTER(app, &app_cmds, "Application", NULL);

/* in radio.c */
SHELL_SUBCMD_ADD((app), radio, NULL, "Radio cmds", cmd_radio, 1, 0);
```
Modules contribute subcommands without a central table.

## Dictionary commands (value lookup)
```c
static int cmd_gain(const struct shell *sh, size_t argc, char **argv, void *data)
{
    set_gain((int)(intptr_t)data);
    return 0;
}
SHELL_SUBCMD_DICT_SET_CREATE(sub_gain, cmd_gain,
    (low, 1, "x1"), (mid, 4, "x4"), (high, 16, "x16"));
SHELL_CMD_REGISTER(gain, &sub_gain, "Set gain", NULL);
```

## Tips
- `shell_print`, `shell_warn`, `shell_error`, `shell_hexdump` for output.
- Handler return values: 0 success, 1 help printed and command not executed, `-EINVAL` argument validation
  failed, `-ENOEXEC` command not executed.
- Each shell instance has its own thread; size `CONFIG_SHELL_STACK_SIZE` for the deepest handler.
- `CONFIG_SHELL_GETOPT=y` creates a per-instance, thread-safe getopt state for `-x` style options.

## Verify
- [ ] Wrong argument counts produce help, not crashes.
- [ ] Tab completion lists dynamic entries.

## Checked

Checked 2026-10-26 against the Zephyr shell guide and `include/zephyr/shell/shell.h` on main: `SHELL_CMD_ARG`
mandatory count includes the command name and a wrong count prints an error without calling the handler (the skill
said it returns `-EINVAL`; fixed); dynamic entries must set `syntax` to NULL when no more are available; the
`SHELL_SUBCMD_SET_CREATE((parent))` plus `SHELL_SUBCMD_ADD` pattern, `SHELL_SUBCMD_DICT_SET_CREATE` triplet form and handler
signature with a data pointer, the handler return codes, `CONFIG_SHELL_STACK_SIZE` and `CONFIG_SHELL_GETOPT` Kconfig
symbols.

Method: documentation only; no commands were run.
