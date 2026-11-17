---
id: computing-software.web-development.astro.cli-background-server
name: cli-background-server
category: computing-software
field: web-development
product: astro
tags: [background-server, lock-file, json-logging, ignore-lock, agent-detection]
level: advanced
status: docs-checked
description: "Run astro dev or preview as a detached background server with --background, manage it with stop/status/logs, and the lock file and --ignore-lock rules."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/reference/cli-reference.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--background` starts the dev server (and the preview server since v7.2.0) as a detached background process and enables JSON logging. A lock file (`.astro/dev.json` or `.astro/preview.json`) records the URL, port and PID, preventing many instances for the same project.

The flag is provided automatically when an AI agent is detected on macOS and Linux. On Windows automatic backgrounding does not happen; the server stays in the foreground. You can always pass it manually:

```shell
astro dev --background
```

If a server is already running, the command prints its info and exits. `--force` stops the existing server and starts a new one:

```shell
astro dev --background --force
```

Subcommands for `astro dev` (and `astro preview` since v7.2.0):

- `stop`: sends `SIGTERM`, waits up to 5 seconds, then escalates to `SIGKILL`.
- `status`: shows whether a background server is running, with URL, PID and uptime.
- `logs`: prints logs; works only for servers started with `--background`. `--follow` (`-f`) streams like `tail -f`.

`--ignore-lock` skips the lock-file check and write so a second server can run alongside (preview since v7.3.0). It errors when combined with `--background` or `--force`, and the new server is not tracked by the subcommands:

```shell
astro dev --ignore-lock --port 4322
```

`--json` enables machine-readable JSON logging.

## Checked

2026-11-04. Confirmed against the Astro CLI reference: --background, lock files, automatic agent detection (not on Windows), stop/status/logs, --follow, --ignore-lock rules and --json. Nothing removed.

Method: documentation only; no commands were run.
