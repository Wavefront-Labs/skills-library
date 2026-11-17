---
id: computing-software.systems-network-administration.apache-guacamole.clipboard-and-terminal-display
name: clipboard-and-terminal-display
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, disable-copy, disable-paste, clipboard-control, color-scheme, font-name, font-size, scrollback, terminal-type, backspace, stdin-pipe]
level: practitioner
status: docs-checked
description: "Control clipboard direction and terminal appearance in Guacamole SSH, telnet and Kubernetes: disable-copy/paste, color-scheme, font, scrollback, backspace, STDIN."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
  - https://guacamole.apache.org/doc/gug/guacamole-native.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clipboard and terminal settings

Clipboard (all protocols):
- `disable-copy=true`: block remote-to-browser copy (default allowed)
- `disable-paste=true`: block browser-to-remote paste (default allowed)

Terminal behaviour:
- `backspace`: default ASCII 127 (Delete)
- `terminal-type`: default `linux`

Terminal display:
| Parameter | Default |
|---|---|
| `color-scheme` | `gray-black` (gray text on black) |
| `font-name` | `monospace` |
| `font-size` | 12 points |
| `scrollback` | 1000 rows |

Terminal input from JavaScript: open a pipe stream named `STDIN` with `Guacamole.Client.createPipeStream()`.

Tips:
- Terminal protocols need fonts installed on the Guacamole server (not the client); missing fonts log `Unable to get font "monospace"` in syslog (apache-guacamole.build-guacamole-server).
- If backspace shows `^?` or `^H` instead of erasing, adjust `backspace` (default 127).
- `color-scheme` is a semicolon-separated list such as `foreground: rgb:00/00/ff; background: rgb:ff/ff/ff`; the legacy names `black-white`, `gray-black`, `green-black` and `white-black` are still accepted.

Verify: a connection with `font-size=16` and `scrollback=5000` shows larger text and longer history.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages configuring-guacamole and guacamole-native: disable-copy and disable-paste meanings and defaults (all protocols), backspace default 127 and the ^? or ^H symptom, terminal-type default linux, color-scheme default gray on black and its format, font-name, font-size and scrollback defaults, terminal emulator used by SSH, telnet and Kubernetes, the STDIN pipe via createPipeStream, and the missing-font syslog message. Changed: removed the exfiltration advice and file-transfer remark, which the page does not make; added the colour-scheme format and the fonts-on-server note.

Method: documentation only; no commands were run.
