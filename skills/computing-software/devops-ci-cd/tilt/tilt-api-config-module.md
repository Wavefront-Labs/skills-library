---
id: computing-software.devops-ci-cd.tilt.tilt-api-config-module
name: tilt-api-config-module
category: computing-software
field: devops-ci-cd
product: tilt
tags: [api-config-module]
level: practitioner
status: docs-checked
description: "Tiltfile config module: define_string, define_string_list, define_bool, parse, set_enabled_resources, clear_enabled_resources and the tilt_subcommand and path values."
sources:
  - "https://docs.tilt.dev/api.html#api.config"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The Tiltfile config module

Goal: let users pass named settings to a Tiltfile (`tilt up -- --foo bar`) and choose which resources run.

## Values

- `config.tilt_subcommand`: the sub-command Tilt was invoked with, excluding extra args. `tilt down` gives "down"; `tilt up frontend backend` gives "up"; `tilt alpha tiltfile-result` gives "alpha tiltfile-result".
- `config.main_path`: absolute path of the main Tiltfile.
- `config.main_dir`: absolute directory of the main Tiltfile; often used to locate vendored code and caches.

## Defining settings

`define_string_list(name, args=False, usage="")`, `define_string(...)` and `define_bool(...)` each define a setting that appears under key `name` in the dict returned by `parse()`.

- `args=False`: set by name. For a string named "foo", `tilt up -- --foo bar` gives "bar"; for a list, it gives `["bar"]`; for a bool, `tilt up -- --foo` gives True.
- `args=True`: set by unnamed positional args. `tilt up -- 1 2 3` gives `["1" "2" "3"]` for a list; `tilt up -- 1` gives "1" for a string. For a bool this is unlikely to be what you want.
- `usage`: description printed when arg parsing fails.

A bool is False via `tilt up -- --foo=False` or a default:

```
config.define_bool('foo')
cfg = config.parse()
do_stuff = cfg.get('foo', False)
```

## parse()

Loads settings from tilt_config.json, overlays Tiltfile command-line args, validates them against the definitions, and returns a dict. Settings defined but not specified are absent, so use `cfg.get('foo', ["hello"])` for a default.

By default Tilt reads command-line args as resource names. Once a Tiltfile calls `parse()`, that is suppressed; if you still need resource selection, call `set_enabled_resources`.

## Enabling resources

- `config.set_enabled_resources(resources)`: only run the named resources; takes precedence over the command-line default. An empty list runs all resources.
- `config.clear_enabled_resources()`: disable all resources, so the user enables the ones they want once Tilt is running.

See the Tiltfile config documentation (tiltfile_config.html) for examples.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/api.html#api.config (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
