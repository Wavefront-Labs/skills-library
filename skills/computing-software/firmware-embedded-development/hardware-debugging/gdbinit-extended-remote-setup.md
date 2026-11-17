---
id: computing-software.firmware-embedded-development.hardware-debugging.gdbinit-extended-remote-setup
name: gdbinit-extended-remote-setup
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [gdbinit-setup, gdbinit, extended-remote, target-remote, auto-load-safe-path, arm-none-eabi-gdb, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Set up a project .gdbinit for embedded targets: extended-remote vs remote, auto-load safe-path, user-defined macros and monitor commands."
sources:
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Connecting.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Auto_002dloading-safe-path.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Define.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project .gdbinit and extended-remote

## remote vs extended-remote
GDB supports `target remote` and `target extended-remote`; many remote targets support only `target remote`, so check
what your debug server offers.
- `target remote`: when the program exits or you detach, GDB disconnects. `run` and `attach` are not supported.
- `target extended-remote`: after exit or detach GDB stays connected, so you can rerun, attach, or use `monitor`
  commands. `run` is supported (it uses `set remote exec-file`), as is `attach`.
- Both take the same arguments: a serial device, a Unix socket, `host:port` (TCP, or `udp:host:port`), or
  `| command`. Omit the host for a local server but keep the colon, for example `target remote :1234`.
- Specify the program with `file` (or as the first GDB argument). It should be an unstripped copy matching what runs on
  the target; mismatched files give confusing results.
- `detach` releases the program (in remote mode GDB can then connect elsewhere); `disconnect` closes the connection and
  generally does not resume the target. `monitor cmd` sends a command straight to the server's monitor.

## A project file
```gdb
# <project>/.gdbinit
target extended-remote localhost:3333

define reload
  monitor reset halt
end
document reload
Reset and halt the target through the debug server's monitor.
end
```
`define commandname ... end` creates a user command (arguments are `$arg0` ... `$argN`, count in `$argc`);
`document commandname ... end` gives it `help` text. `save user filename` writes all user-defined commands to a script
that `source` can read back. Monitor command names (such as `reset halt`) belong to your debug server, so take them
from its documentation.

## Auto-load security
GDB does not automatically load files from untrusted locations. The setting `auto-load safe-path` lists trusted
directories (and their subdirectories); a project file outside them is declined with a warning containing
`auto-loading has been declined`. Add your workspace from your home init file:
```gdb
add-auto-load-safe-path ~/work
```
- `set auto-load safe-path /` disables the protection, which the manual says is meant for trusted sources only. Do not
  use it where cloned repositories might be untrusted.
- For one session: `gdb -iex "set auto-load safe-path <dir>" ...`. `set auto-load no` forbids auto-loading.
- Use `show auto-load safe-path` to see the list; entries are separated by `:` on Unix and `;` on Windows.

## Verify
- [ ] Opening GDB on the ELF in the project directory connects without an auto-load warning.
- [ ] `reload` (or your own macro) works and `help reload` shows its text.

## Checked
Method: docs-checked 2026-11-09 against the GDB manual pages Connecting to a Remote Target, Security restriction for auto-loading and User-defined Commands (all read in full). Removed unconfirmed claims: which probes support extended-remote, history and pretty-print settings, hook-quit and hookpost-load, batch/CI invocation and exit-status versions, "already connected" gotcha.
