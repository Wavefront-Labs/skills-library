---
id: computing-software.software-engineering.erlang.application-callback
name: application-callback
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-otp-more, application-callback]
level: practitioner
status: docs-checked
description: "OTP application behaviour: start/2 returning the top supervisor pid, stop/1, prep_stop and application:ensure_all_started."
sources:
  - https://www.erlang.org/doc/apps/kernel/application.html
  - https://www.erlang.org/doc/apps/kernel/app.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application callback module
**Goal:** start and stop an OTP application correctly.

```erlang
-module(myapp_app).
-behaviour(application).
-export([start/2, stop/1]).
start(_Type, _Args) -> myapp_sup:start_link().
stop(_State) -> ok.
```
- `start/2` starts the processes of the application; for a supervision tree that means starting the top supervisor. It must return `{ok, Pid}` or `{ok, Pid, State}` (or `{error, Reason}`), where `Pid` is the top supervisor; `State` defaults to `[]`. `StartArgs` come from the `mod` key of the application resource file.
- `application:ensure_all_started(myapp)` starts the not-yet-started dependencies of the application (and optional ones that are available), then the application itself, returning `{ok, Started}`.
- Optional callbacks: `prep_stop/1`, `start_phase/3`, `config_change/3`.
- On `application:stop/1` the application master calls `prep_stop/1` if defined, then tells the top supervisor to shut down; `stop/1` is then called to clean up and its return value is ignored. `stop/1` gets the value returned by `prep_stop/1`, else the `State` from `start/2`.
- `config_change/3` is called after a code replacement if configuration parameters changed.

## Self-check
Run `application:ensure_all_started(myapp)` then `application:which_applications()`.

## Checked
Method: docs-checked 2026-11-09 against the Erlang kernel `application` reference page (callbacks, ensure_all_started, stop) and the `app` resource file page (mod key). Dropped the blocking-start gotcha and the reverse-order shutdown wording, which neither page states.
