---
id: computing-software.software-engineering.erlang.ports
name: ports
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-native, ports]
level: practitioner
status: draft
description: "Erlang ports: open_port spawn_executable, messages, exit_status, packet framing and os:cmd trade-offs."
sources:
  - https://www.erlang.org/doc/apps/erts/
  - https://www.erlang.org/doc/apps/erl_interface/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ports and external programs
**Goal:** drive an external program safely.

```erlang
Port = open_port({spawn_executable, "/usr/bin/sort"},
                 [binary, exit_status, use_stdio, {args, ["-r"]}, {line, 1024}]),
port_command(Port, <<"a\nb\n">>),
receive {Port, {data, {eol, Line}}} -> Line;
        {Port, {exit_status, Code}} -> {exit, Code}
after 5000 -> port_close(Port), timeout end.
```
- Port messages: `{Port, {data, D}}`, `{Port, {exit_status, N}}`, `{'EXIT', Port, Reason}` when trapping exits.
- The owner process is linked; if it dies the port closes. Closing stdin signals EOF to the program, which is how it should exit.
- `{packet, 4}` frames messages with a 4-byte length for binary protocols.
- `os:cmd/1` runs through a shell, blocks, returns stdout as a string; avoid with user input (shell injection).

## Gotchas
- External programs may keep running if they ignore EOF on stdin.
- Pass arguments with `{args, List}`; do not build shell strings.

## Self-check
Run a program with exit_status and handle both data and exit messages.
