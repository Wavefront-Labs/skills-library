---
id: computing-software.messaging-and-integration.ntfy.cli-subscribe-command
name: cli-subscribe-command
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, cli, subscribe, command, environment-variables]
level: practitioner
status: docs-checked
description: "Run a command for every ntfy message with ntfy subscribe TOPIC COMMAND and use the NTFY_* environment variables it sets."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ntfy subscribe on the command line

`ntfy subscribe TOPIC` (alias `ntfy sub`) prints one JSON object per message and stays open unless `--poll` is passed.

```
ntfy sub mytopic 'notify-send "$m"'
ntfy sub topic1 /my/script.sh
ntfy sub topic1 'echo "Message $m was received. Its title was $t and it had priority $p"'
```

Wrap variables in double quotes inside the command string.

## Variables

| Variable | Aliases | Meaning |
|---|---|---|
| `$NTFY_ID` | `$id` | message ID |
| `$NTFY_TIME` | `$time` | Unix timestamp |
| `$NTFY_TOPIC` | `$topic` | topic |
| `$NTFY_MESSAGE` | `$message`, `$m` | body |
| `$NTFY_TITLE` | `$title`, `$t` | title |
| `$NTFY_PRIORITY` | `$priority`, `$prio`, `$p` | 1 to 5 |
| `$NTFY_TAGS` | `$tags`, `$tag`, `$ta` | comma-separated |
| `$NTFY_RAW` | `$raw` | raw JSON |

## Authentication

```
ntfy subscribe -u phil:mypass ntfy.example.com/mysecrets
```

## Gotchas

- The page's examples put the command in single quotes; ntfy passes the fields as environment variables.
- Self-hosters can set `default-host` in `client.yml` to use short topic names.

## Checked

2026-11-04. Confirmed against the ntfy subscribe CLI page: JSON streaming and `--poll`, command execution examples, variable table with aliases, `-u` auth example, `default-host`. Removed: the Verify step.
Method: documentation only; no commands were run.
