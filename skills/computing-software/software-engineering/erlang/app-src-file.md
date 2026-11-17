---
id: computing-software.software-engineering.erlang.app-src-file
name: app-src-file
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-application, app-src-file]
level: practitioner
status: docs-checked
description: "Erlang application resource file: description, vsn, applications, mod, env, registered, modules, included_applications, rebar3 .app.src."
sources:
  - https://www.erlang.org/doc/apps/kernel/app.html
  - https://rebar3.org/docs/basic_usage/
  - https://rebar3.org/docs/deployment/releases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The .app.src resource file
**Goal:** write an .app.src that rebar3 turns into a valid .app.

```erlang
{application, myapp,
 [{description, "My service"},
  {vsn, "0.1.0"},                  % rebar3 also accepts git, semver, {cmd, ...}, {file, ...}
  {registered, [myapp_sup]},
  {mod, {myapp_app, []}},
  {applications, [kernel, stdlib, sasl, crypto, ssl]},
  {env, [{port, 8080}]},
  {modules, []}]}.
```
- The runtime file is `Application.app` in the application's `ebin` directory; it holds a single Erlang term, the application specification. For a rebar3 project the source is `src/myapp.app.src`.
- The application controller treats all keys as optional. The `systools` functions (start scripts, releases) require `description`, `vsn`, `modules`, `registered` and `applications`.
- `applications` lists every application that must be started before this one (all applications depend on at least kernel and stdlib). `optional_applications` lists optional ones; to have an optional dependency started first when present, list it in both.
- `registered` lists registered process names; `systools` uses it to detect name clashes between applications.
- `env` parameters are read with `application:get_env/1,2` and can be overridden by a config file or command-line flags.
- `included_applications`: the application controller loads them but does not start them; the top supervisor of an included application must be started by a supervisor of this one.
- `mod` is needed for an application implemented as a supervision tree; omit it for a library application with no processes (like STDLIB).
- With rebar3 `vsn` of `git` or `semver` uses the latest git tag.

## Gotchas
- Forgetting to add a dependency to `applications` in the `.app.src` is a common mistake; relx warns about calls to functions not included in the release.
- `{vsn, git}` needs a reachable tag; a shallow CI clone may not have one.

## Self-check
Run `rebar3 compile` and inspect the generated `.app` file under `_build`.

## Checked
Method: docs-checked 2026-11-09 against the Erlang kernel `app` reference page, the rebar3 Basic Usage page (.app.src template, vsn options) and rebar3 Releases page (relx undefined-function check). Dropped the `licenses` and `links` keys, the claim that rebar3 fills in `modules`, and the claim that a missing dependency fails with `undef` only in a release.
