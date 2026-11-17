---
id: computing-software.devops-ci-cd.tilt.tilt-cli-logs-args-snapshot
name: tilt-cli-logs-args-snapshot
category: computing-software
field: devops-ci-cd
product: tilt
tags: [cli-logs-args-snapshot]
level: practitioner
status: docs-checked
description: "Read logs from a running Tilt, change its Tiltfile args live, and create or view snapshot files with tilt logs, args and snapshot."
sources:
  - "https://docs.tilt.dev/cli/tilt_logs.html"
  - "https://docs.tilt.dev/cli/tilt_args.html"
  - "https://docs.tilt.dev/cli/tilt_snapshot_create.html"
  - "https://docs.tilt.dev/cli/tilt_snapshot_view.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tilt logs, args, snapshot

Goal: inspect and steer a running Tilt. By default these look for Tilt on localhost:10350; change with `--host` / `--port` (or TILT_HOST / TILT_PORT).

## tilt logs

```
tilt logs [resource1, resource2...]
```

- `-f, --follow`: stream logs; otherwise print the current logs and exit.
- `--since`: only logs since a duration ago (e.g. "5m", "1h", "30s").
- `--tail`: number of lines from the end (-1 for all, the default).
- `--level`: one of "warn", "error".
- `--source`: "all" (default), "build" or "runtime".
- `--json`: JSON Lines output.

## tilt args

Changes the Tiltfile args of a running Tilt. Args can choose which resources Tilt enables, and can define custom key-value pairs read in a Tiltfile via `config.parse()`. Tiltfile args do not affect built-in Tilt args (such as `--legacy`, `--port`); they come after built-in args, following `--`.

```
tilt args [<flags>] [-- <Tiltfile args>]
```

```
# Set new args
tilt args frontend_service backend_service -- --debug on
# Edit the current args
tilt args
# Use an alternative editor
EDITOR=nano tilt args
```

With no args, it opens the current args in the editor from TILT_EDITOR or EDITOR, or an OS-appropriate default. `--clear` clears the args as if Tilt were run with none.

## tilt snapshot

Parent of two subcommands.

`tilt snapshot create [file to save]` writes a snapshot of a running Tilt; with no file it goes to stdout.

```
tilt snapshot create snapshot.json
tilt snapshot create > snapshot.json
```

`tilt snapshot view <path/to/snapshot.json>` serves a snapshot file and optionally opens it in the browser.

```
tilt ci --output-snapshot-on-exit=snapshot.json
tilt snapshot view snapshot.json
curl http://myci.com/path/to/snapshot | tilt snapshot view -
```

View flags: `--no-open` skips opening the browser; `--port` defaults to a random port; `--host` defaults to localhost (change only for remote access, understanding the security implications).

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/cli/tilt_logs.html, https://docs.tilt.dev/cli/tilt_args.html, https://docs.tilt.dev/cli/tilt_snapshot_create.html, https://docs.tilt.dev/cli/tilt_snapshot_view.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Added tilt_args and tilt_snapshot create/view pages to sources (resolve) and read them.

Method: documentation only; no commands were run.
