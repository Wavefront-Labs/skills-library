---
id: computing-software.devops-ci-cd.tilt.tilt-tiltfile-config
name: tilt-tiltfile-config
category: computing-software
field: devops-ci-cd
product: tilt
tags: [tiltfile-config, tilt, tiltfile, config]
level: practitioner
status: docs-checked
description: "Expose user options in a Tiltfile with config.define_*, tilt_config.json and tilt args, including enabled-resource patterns."
sources:
  - "https://docs.tilt.dev/tiltfile_config.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tiltfile config

Goal: let users choose options (which services run, which to edit) without learning the Tiltfile.

## Ways users set options

- Flags and args on the command: `tilt up -- --key value`.
- A `tilt_config.json` next to the Tiltfile, one JSON dict such as `{"to-edit": ["b", "c"]}`. Changes re-execute the Tiltfile. Command-line args win over the file, even if the file changes later.
- At runtime: `tilt args -- --key value2`; `tilt args --clear` resets to a bare `tilt up`.

## Defining settings

```python
config.define_string_list("to-run", args=True)
config.define_string_list("to-edit")
cfg = config.parse()
config.set_enabled_resources(cfg.get('to-run', []))
```

Flag types: `config.define_string_list("foo")` (`-- --foo bar --foo baz`), `config.define_string("foo")` (`-- --foo bar`), `config.define_bool("foo")` (`-- --foo` or `--foo=False`).

At most one option may take positional args (`args=True`); then `tilt up -- bar baz` yields `['bar', 'baz']`.

Without `config.parse`, Tilt treats non-empty args as the resources to run. Equivalent Tiltfile:

```python
config.define_string_list("args", args=True)
cfg = config.parse()
config.set_enabled_resources(cfg.get('args', []))
```

## Patterns

- Groups: map names such as `consumer` to resource lists in a dict, expand each arg, then call `config.set_enabled_resources(resources)`.
- Edit only some services: call `docker_build('a', './a')` only when `'a'` is in `cfg.get('to-edit', [])`; an image in YAML with no build keeps its existing tag.
- Start with nothing running: `config.clear_enabled_resources()`. Then use `tilt enable a b`, `tilt enable --only a b`, `tilt enable --all`, `tilt disable a b`, `tilt disable --all`.
- UI grouping: pass `labels="frontend"` or a list to `k8s_resource`, `local_resource` or `dc_resource`; the UI groups by label alphabetically, and a resource with several labels appears in each group.

`tilt down a b d` deletes only those services.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Tiltfile Config page in full (Setting Options, all five examples, The Config File, Changing args at runtime, Comparison to Default Behavior, Flag types, Positional Arguments). Confirmed `tilt_config.json` behaviour and precedence, `tilt args` and `--clear`, the three flag types, the at-most-one positional option rule, the default-behaviour Tiltfile, `config.clear_enabled_resources()`, the enable and disable commands, and label grouping. Nothing removed. 

Method: documentation only; no commands were run.
