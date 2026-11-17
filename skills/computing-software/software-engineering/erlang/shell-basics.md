---
id: computing-software.software-engineering.erlang.shell-basics
name: shell-basics
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-shell, shell-basics]
level: intro
status: draft
description: "Erlang shell usage: bindings, f(), c(), l(), rr(), v(), history, user switch command, remsh and quitting."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The Erlang shell
**Goal:** work fluently in `erl`.

```
1> c(mymod).               % compile and load
2> l(mymod).               % reload after external rebuild
3> rr("include/rec.hrl").  % load records for printing
4> f(X).                   % forget a binding; f() forgets all
5> v(-1).                  % previous result
6> h(lists, map, 2).       % docs when doc chunks are available
```
- `rebar3 shell` loads your app and deps (and starts the app unless configured otherwise).
- `Ctrl+G` opens the user switch command menu (`h` help, `j` jobs, `r` remote shell, `q` quit); `q().` or `init:stop().` quit cleanly.
- Start a remote shell on a running node: `erl -remsh node@host -sname me -setcookie <cookie>`.
- `+pc unicode` or `io:setopts([{encoding, unicode}])` for wide characters.

## Gotchas
- Funs defined in the shell cannot be shipped across nodes if the shell session ends.
- Killing a remsh with `Ctrl+C` twice (`a`bort) may stop the remote node if you used `q()` there; use `Ctrl+G` then `q`.

## Self-check
Define a module, `c/1` it, change it, `l/1` it, and call the new version.
