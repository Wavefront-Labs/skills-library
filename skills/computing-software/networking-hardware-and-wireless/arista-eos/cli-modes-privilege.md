---
id: computing-software.networking-hardware-and-wireless.arista-eos.cli-modes-privilege
name: cli-modes-privilege
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, cli-modes, privilege-levels, enable-mode, exec-modes]
level: practitioner
status: draft
description: "Navigate EOS user exec, privileged exec and global configuration modes, with help, abbreviations and pipes."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EOS CLI modes and privilege levels
Goal: move between EOS CLI modes and filter output efficiently.

```
switch> enable
switch# configure terminal
switch(config)# interface ethernet 1
switch(config-if-Et1)# exit
switch(config)# end
switch# show running-config | section bgp
switch# show interfaces status | include connected
switch# show running-config | grep -i ntp
switch# show version | json
```

- User exec (`>`) is limited; `enable` goes to privileged exec (`#`); `configure` enters global config. `enable` can require a password via `enable secret`.
- The CLI is IOS-like but is a Linux system underneath: `bash` drops to a shell; `show ... | json` returns JSON for any show command.
- Context help uses `?`; commands can be abbreviated (`sh run`).
- `show running-config | diff` is not supported, so use `show session-config diffs` inside config sessions.

Gotcha: `show running-config` is the live config; `show startup-config` is what loads on boot. Changes are lost after reload unless saved with `write memory` (or `copy running-config startup-config`).

## Verify
- `show version` and `show running-config | section interface` return expected output; after `write memory` startup and running match.
