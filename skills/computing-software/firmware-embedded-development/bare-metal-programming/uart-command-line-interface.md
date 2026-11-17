---
id: computing-software.firmware-embedded-development.bare-metal-programming.uart-command-line-interface
name: uart-command-line-interface
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [uart-cli, superloop, debug-shell, command-table, line-editing, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Add a small debug/production CLI over UART to bare-metal firmware: non-blocking line input, a static command table, argc/argv handlers, and locking it down in release builds."
sources:
  - https://github.com/memfault/interrupt/blob/master/_posts/2020-06-09-firmware-shell.md
  - https://github.com/marcinbor85/microshell
  - https://docs.zephyrproject.org/latest/services/shell/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UART command line interface

A serial shell gives a structured way to query a device's configuration and state and to send commands during
bring-up, factory test and debugging (the Memfault Interrupt article's motivation).

## Structure
Each command is a handler taking `int argc, char *argv[]`, registered in a table of name, handler and help
string, with a `help` command that lists them; `argc` counts the strings in `argv`, and `argv[0]` is the
command name.
```c
typedef int (*cli_fn)(int argc, char *argv[]);
typedef struct { const char *name; cli_fn fn; const char *help; } cli_cmd_t;

static const cli_cmd_t s_cmds[] = {
    { "help",   cmd_help,   "list commands" },
    { "reboot", cmd_reboot, "reset the MCU" },
};
```
Check `argc` in each handler (the article's `kv_write` example rejects the wrong argument count). Zephyr's
shell gathers root commands registered with `SHELL_CMD_REGISTER` in a dedicated, alphabetically sorted memory
section, which is how modules register commands without a central list.

## Non-blocking input
Both MicroShell and the Zephyr shell are built around not blocking: MicroShell is serviced by one
non-blocking call (`ush_service`) in the main loop, with non-blocking read and write callbacks that should be
implemented as FIFOs, no dynamic allocation and no static variables so several shells can coexist.
Feed your own CLI the same way: poll a UART RX FIFO from the main loop, echo characters, handle backspace,
and execute on end of line. Completion, history and arrow-key editing are optional extras that cost code
space; MicroShell (VT100, Tab completion) and Zephyr's shell (history, Tab completion) provide them
ready-made.

## Output for humans and machines
- The article advises one consistent result format for every command, such as `> OK` or `> FAIL,<code>`.
- CSV works for tabular output; use base64 or hex encoding for binary buffers.
- Factory and automated test scripts parse this output, so command arguments, behaviour and output must not
  change between builds. Unit-test the exact output and run those tests in CI, and mark stable commands with
  comments.

## Production considerations
- Command implementations are heavy in strings and formatting and optimise poorly, so developer-only commands
  are usually the first removed. The article wraps them in `#if !PRODUCTION_BUILD` and keeps only what
  automated tests need.
- Secure or remove the serial shell before shipping. The article lists password verification (weak: visible
  with `strings` on the firmware unless obfuscated, and still weak), a knock pattern, signing an "UNLOCK"
  phrase with the device key, and shipping different firmware without the shell.
- Keep output non-blocking so a long `help` does not stall the main loop.
- Zephyr can also expose the shell over RTT, telnet, USB CDC ACM or Bluetooth LE (NUS) backends, not only
  UART.

## Verify
- [ ] Typing fast, pasting long lines, and sending binary junk never hangs or overflows.
- [ ] Main-loop latency is unaffected while the CLI prints.
- [ ] Release build: CLI absent or locked.

## Checked
Checked 2026-11-09 against the Memfault Interrupt "firmware shell" article, the MicroShell README and the
Zephyr shell documentation (searched for and read the command registration, backend, feature, formatted
output, production and security sections). Removed: the exact line-editor C code and `strtoul` parsing advice
(the author's own illustration, not in the sources), the "about 8 arguments" limit, the `section(".cli_cmds")`
and `KEEP` recipe, and the picocom and PuTTY terminal settings.
Method: docs-checked 2026-11-09 against the Memfault article, MicroShell README and Zephyr shell docs.
