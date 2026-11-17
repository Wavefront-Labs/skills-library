---
id: computing-software.digital-forensics-incident-response.volatility.console-command-history-from-memory
name: console-command-history-from-memory
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [consoles-plugin, memory-artefacts, volatility3, cmdline-plugin, dfir]
level: practitioner
status: docs-checked
description: "Recover typed console commands and output from memory with windows.cmdscan/consoles (conhost), plus PowerShell history and command line context."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.html", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Console command history from memory

**Goal:** attackers type commands into cmd.exe and PowerShell. Console history buffers in
`conhost.exe` memory keep those commands - and sometimes their output - even when nothing was logged to disk.

## Volatility 3
```bash
vol -f mem.raw windows.cmdline                     # command line of every process (how cmd/powershell were launched)
vol -f mem.raw windows.cmdscan                     # COMMAND_HISTORY structures: typed commands per console
vol -f mem.raw windows.consoles                    # CONSOLE_INFORMATION: history plus screen buffer (output)
vol -f mem.raw windows.pstree                      # find conhost.exe and its client processes
```
- `consoles` output can include the screen buffer, so command output the attacker viewed may be recoverable.
- Map each conhost to its client process (cmd.exe/powershell.exe PID) via pstree/handles.
- If your Volatility 3 build lacks these plugins, check its plugin list (they are in the current documentation); Volatility 2 has equivalents that need the right profile.

## Fallback
- Extract strings with offsets from the image and map the offsets to processes with the `windows.strings` plugin.
- PowerShell: also check the on-disk PSReadLine history file and script block logging; in memory, string or YARA search the powershell.exe process.

## Gotchas
- History buffers are limited in size; old commands roll off.
- Commands run non-interactively do not appear in console history; use cmdline and process creation instead.

## Verify
Recovered commands are tied to a process, user (windows.getsids) and approximate time (process create time).

## Checked
2026-11-01. Confirmed in the Volatility 3 windows plugin index: `windows.cmdline`, `windows.cmdscan`, `windows.consoles`, `windows.getsids`, `windows.strings` and `windows.pstree` exist. Removed: the version in which cmdscan and consoles were ported, default buffer sizes, the PSReadLine path, event ID 4104, and the `strings`/grep recipe, none confirmed by the fetched docs. The plugin descriptions are the author's, consistent with the plugin names.
Method: documentation only; no commands were run.
