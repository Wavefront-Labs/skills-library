---
id: computing-software.devops-ci-cd.dagger.cli-running-functions
name: cli-running-functions
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, cli, dagger-call, dagger-query, dagger-run, verbosity, interactive-debug]
level: practitioner
status: docs-checked
description: "Run Dagger functions and API queries from the CLI with dagger call, core, functions, query and run, and tune output with the global flags."
sources: [https://docs.dagger.io/0.21/reference/cli]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dagger CLI: running functions and tuning output

Goal: pick the right `dagger` subcommand to execute work and the right global flags to see what you need. Based on the Dagger 0.21 docs CLI reference.

## Method

Usage form: `dagger [options] [subcommand | file...]`.

- `dagger functions [function]...` lists functions of the loaded module (like `dagger call --help` but only the function list).
- `dagger call` runs one or more functions chained into a pipeline. Own flags: `-j/--json` (result as JSON), `-o/--output <path>` (save result to a local file or directory), `-m/--mod`, `-M/--no-mod`.
- `dagger core` calls a core API function; same `-j` and `-o` flags.
- `dagger query [operation]` sends a GraphQL document to the engine. It reads stdin unless `--doc <file>` is given; pass variables with `--var key=value` (repeatable) or `--var-json '<json>'` (overrides `--var`). Docs example:

```
dagger query <<EOF
{ container { from(address:"hello-world") { withExec(args:["/hello"]) { stdout } } } }
EOF
```

- `dagger run <command>...` executes any command inside a Dagger session with a live TUI. It injects `DAGGER_SESSION_PORT` and `DAGGER_SESSION_TOKEN`, so a script can hit `http://127.0.0.1:$DAGGER_SESSION_PORT/query` with basic auth using the token as username. Examples: `dagger run go run main.go`, `dagger run node index.mjs`, `dagger run python main.py`. Extra flags: `--cleanup-timeout` (wait between SIGTERM and SIGKILL, default 10s) and `--focus` (only show output of focused commands).
- `dagger -c '<shell command>'` executes a Dagger shell command.
- `dagger version [--check]` prints the version; `--check` looks for updates.

## Global flags worth knowing

- Which module: `-m/--mod <local path or git repo>` (default: current directory); `-M/--no-mod` loads none (mutually exclusive with `-m`).
- Verbosity: `-v` (repeat as `-vv`, `-vvv`), `-q` (progress, cleaned up at end), `-s` (no progress), `-d/--debug` (debug logs, full verbosity).
- `--progress auto|plain|tty|dots|logs` selects the output format (default auto).
- `-E/--no-exit` keeps the TUI open after completion; `-w/--web` opens the trace URL in a browser.
- `-i/--interactive` opens a terminal on container exec failure; `--interactive-command` changes the default `/bin/sh`.
- `-y/--auto-apply` applies a returned changeset without asking.
- `--lock disabled|live|pinned|frozen` (see computing-software.devops-ci-cd.dagger.lockfiles).
- LLM: `--model`, `--allow-llm <module URL>... | all` (see computing-software.devops-ci-cd.dagger.llm-providers).
- `--eager-runtime` loads the module runtime eagerly; `--x-release <git ref>` runs an experimental release.

## Gotchas

- `-M` and `-m` cannot be combined.
- Related skills: computing-software.devops-ci-cd.dagger.cli-module-lifecycle, computing-software.devops-ci-cd.dagger.troubleshooting.

## Gaps

The CLI page lists flags only; semantics of `--eager-runtime` and `--x-release` are not explained.

## Checked

2026-11-07

Read in full from the docs source: reference/cli/index.mdx. Confirmed the usage line, call, core, functions, query, run, version options and defaults, the DAGGER_SESSION_PORT and DAGGER_SESSION_TOKEN note, and every global flag listed. The Gaps note matches the page (flags only). No corrections needed.

Method: documentation only; no commands were run.
