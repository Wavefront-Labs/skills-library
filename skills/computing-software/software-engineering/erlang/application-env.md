---
id: computing-software.software-engineering.erlang.application-env
name: application-env
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-application, application-env]
level: practitioner
status: docs-checked
description: "Erlang application environment: get_env/2,3, set_env with the persistent option, get_all_env and the env key in the .app file."
sources:
  - https://www.erlang.org/doc/apps/kernel/application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application environment and set_env
**Goal:** read configuration the OTP way.

```erlang
Port = application:get_env(myapp, port, 8080),
{ok, V} = application:get_env(myapp, secret),
application:set_env(myapp, port, 9090),
application:set_env(myapp, port, 9090, [{persistent, true}]).
```
- The application specification has an `env` key, a list of `{Par, Val}` pairs. `application:get_all_env(App)` returns all parameters of an application.
- `application:get_env/2` returns `{ok, Val}` or `undefined`; it returns `undefined` if the application is not loaded, the parameter does not exist, or the calling process does not belong to any application. `get_env/3` returns the given default when the parameter does not exist.
- `set_env` with `{persistent, true}` guarantees the value is not overridden by the one in the application resource file on load, so it sticks after load and on application reload.

## Self-check
Set a parameter in the `.app` file `env`, override it with `set_env`, and check what `get_env` returns before and after reloading the application.

## Checked

2026-11-03. Confirmed in the `application` module page: `env` spec key, `get_env/2,3`, `get_all_env/1`, `set_env/3,4`, `persistent` option. Removed: the precedence order between `.app`, `sys.config` and command-line parameters, the command-line value typing claim, and the compile-time-read and restart gotchas (not covered by this page).
Method: documentation only; no commands were run.
