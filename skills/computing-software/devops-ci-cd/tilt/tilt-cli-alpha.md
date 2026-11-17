---
id: computing-software.devops-ci-cd.tilt.tilt-cli-alpha
name: tilt-cli-alpha
category: computing-software
field: devops-ci-cd
product: tilt
tags: [cli-alpha]
level: advanced
status: docs-checked
description: "Use the unstable tilt alpha subcommands: get, shell, tiltfile-result, tree-view and updog."
sources:
  - "https://docs.tilt.dev/cli/tilt_alpha.html"
  - "https://docs.tilt.dev/cli/tilt_alpha_get.html"
  - "https://docs.tilt.dev/cli/tilt_alpha_shell.html"
  - "https://docs.tilt.dev/cli/tilt_alpha_tiltfile-result.html"
  - "https://docs.tilt.dev/cli/tilt_alpha_tree-view.html"
  - "https://docs.tilt.dev/cli/tilt_alpha_updog.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tilt alpha commands

Goal: use Tilt's unstable, advanced commands. They are for advanced users only and their APIs may change frequently. Subcommands that contact Tilt take `--host` (default `localhost`) and `--port` (default 10350).

## tilt alpha get

```
tilt alpha get TYPE [NAME | -l label]
```

Displays one or many resources. Flags include `-o, --output` (json, yaml, name, jsonpath, custom-columns, wide and others), `-l, --selector`, `--field-selector`, `-w, --watch`, `--watch-only`, `--sort-by` (a JSONPath expression), `--show-labels`, `-L, --label-columns`, `--no-headers`, `--ignore-not-found`.

## tilt alpha shell

```
tilt alpha shell [<resource-name>]
```

Finds the Kubernetes Pod in the resource and opens an interactive shell. It tries, in order: kubectl shell; `kubectl exec -it <pod> -- bash`; `kubectl exec -it <pod> -- sh`. Currently only works on MacOS and Linux. `-c, --container` names the container (only required with more than one).

## tilt alpha tiltfile-result

Executes the Tiltfile and prints data about execution, by default as JSON (unstable API).

- Exit code 0: success, data on stdout.
- Exit code 1: failure in setup, printing results, etc.
- Exit code 5: error evaluating the Tiltfile (syntax error, illegal operation, etc.).

Flags: `-f, --file` (default "Tiltfile"), `-b, --builtin-timings` (print timings of builtin calls instead), `--dur-threshold` (with builtin timings, only calls at least this long), `--context` (Kubernetes context override), `-v` to print execution logs on stderr.

## tilt alpha tree-view

```
tilt alpha tree-view
tilt alpha tree-view --blockers
```

Shows resources as a tree by their `resource_deps`; resources with no dependencies are roots. `--blockers` shows only blocked resources and their root blockers. `--dedupe` shows multi-parent subtrees once, annotated with `[also depends on: ...]`.

## tilt alpha updog

```
tilt alpha updog -f config.yaml
```

Demo app that starts a blank-slate Tilt using only the new Tilt API, applies the config, and streams logs until ctrl-c. It does not execute the Tiltfile. `--port-forwards=false` disables all port-forwards.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/cli/tilt_alpha.html, https://docs.tilt.dev/cli/tilt_alpha_get.html, https://docs.tilt.dev/cli/tilt_alpha_shell.html, https://docs.tilt.dev/cli/tilt_alpha_tiltfile-result.html, https://docs.tilt.dev/cli/tilt_alpha_tree-view.html, https://docs.tilt.dev/cli/tilt_alpha_updog.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Added the five tilt alpha subcommand pages to sources (all resolve) and read them.

Method: documentation only; no commands were run.
