---
id: computing-software.systems-network-administration.kopia.kopia-logging
name: kopia-logging
category: computing-software
field: systems-network-administration
product: kopia
tags: [logging, log-level, cli-logs, content-logs, log-dir, retention]
level: practitioner
status: docs-checked
description: "Find Kopia log files, understand cli versus content logs, and set levels and retention."
sources: ["https://kopia.io/docs/advanced/logging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Logs go to `~/.cache/kopia` on Linux, `~/Library/Logs/kopia` on macOS and the local app data `kopia` folder on Windows. Override with `--log-dir` or `KOPIA_LOG_DIR`.

The directory has two subdirectories, each with one file per invocation:

- `cli-logs`: general debugging output that may contain usernames, hostnames and file names. Sanitize before attaching to bug reports.
- `content-logs`: low-level logs that contain no file names or hostnames.

## Retention

| Flag | Environment variable | Default |
| --- | --- | --- |
| `--log-dir-max-files` | `KOPIA_LOG_DIR_MAX_FILES` | 1000 |
| `--log-dir-max-age` | `KOPIA_LOG_DIR_MAX_AGE` | 720h |
| `--content-log-dir-max-files` | `KOPIA_CONTENT_LOG_DIR_MAX_FILES` | 5000 |
| `--content-log-dir-max-age` | `KOPIA_CONTENT_LOG_DIR_MAX_AGE` | 720h |

## Levels

`debug` is the most detailed, `info` is normal output, `warning` shows errors and warnings and `error` shows errors only. `--log-level` sets the console level (default `info`) and `--file-log-level` sets the file level (default `debug`). `--disable-color` turns off colored console output and `--no-progress` suppresses progress output, which suits scripts and cron.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Logging page (locations, --log-dir, cli-logs and content-logs, retention flags, variables and defaults, level flags and defaults). Removed or corrected: the vague pointer to the command-line reference, replaced with the flags the page names.
Method: documentation only; no commands were run.
