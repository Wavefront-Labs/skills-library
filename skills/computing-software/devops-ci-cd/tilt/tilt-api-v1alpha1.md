---
id: computing-software.devops-ci-cd.tilt.tilt-api-v1alpha1
name: tilt-api-v1alpha1
category: computing-software
field: devops-ci-cd
product: tilt
tags: [api-v1alpha1]
level: sme
status: docs-checked
description: "Tiltfile v1alpha1 module: constructors for Tilt API objects such as cmd, file_watch, kubernetes_apply, ui_button, probes and selectors."
sources:
  - "https://docs.tilt.dev/api.html#api.v1alpha1"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# v1alpha1 API objects

Goal: create Tilt API objects directly from a Tiltfile. Top-level constructors each take `name`, plus `labels` (grouping) and `annotations` (attached data), both dicts of strings.

## Object constructors

- `cmd(name, args, dir, env, readiness_probe, restart_on, start_on, disable_source)`: a process on the host machine. `args` must have length at least 1; `env` is a list like `["KEY1=VALUE1"]` layered on Tilt's environment. On exit, Tilt makes a best-effort attempt to kill spawned descendants. `restart_on` triggers a graceful shutdown then restart (killed abruptly if it does not exit in time); `start_on` is the same, but the command does not run until its start_on is satisfied.
- `config_map(name, data)`: unstructured data other controllers can read and write. Keys: alphanumerics, `-`, `_`, `.`.
- `file_watch(name, watched_paths, ignores, disable_source)`: `watched_paths` cannot be empty; `ignores` is a list of `ignore_def(base_path, patterns)` (dockerignore-style patterns).
- `kubernetes_apply(name, yaml, image_maps, image_locators, timeout, ..., cmd, restart_on)`: exactly one of `yaml` or `cmd` (a `kubernetes_apply_cmd(args, dir, env)`) must be given. It redeploys the entire YAML if any image map resolves to a new image. Default timeout is 30s.
- `kubernetes_discovery(name, watches, extra_selectors, ...)`: `watches` are `kubernetes_watch_ref(uid, namespace, name)`; namespace is required.
- `ui_button(name, location, text, icon_name, icon_svg, disabled, requires_confirmation, inputs)`: `icon_svg` takes precedence over `icon_name`. `location` is `ui_component_location(component_id, component_type)`. Inputs are `ui_input_spec(name, label, text, bool, hidden)` using `ui_text_input_spec`, `ui_bool_input_spec` or `ui_hidden_input_spec`.
- `extension(name, repo_name, repo_path, args)` and `extension_repo(name, url, ref)`: URLs may be https git repos or file: locations.

## Helper types

- `restart_on_spec(file_watches, ui_buttons)`, `start_on_spec(ui_buttons)`, `disable_source(config_map=config_map_disable_source(name, key))`.
- Probes: `probe(handler, initial_delay_seconds, timeout_seconds, period_seconds, success_threshold, failure_threshold)` with `handler(exec, http_get, tcp_socket)`; `exec_action(command)` is not run in a shell and exit 0 means healthy.
- Selectors: `label_selector`, `label_selector_requirement` (operators In, NotIn, Exists, DoesNotExist), `object_selector` (regexps), `forward(local_port, container_port, host)`.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/api.html#api.v1alpha1 (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
