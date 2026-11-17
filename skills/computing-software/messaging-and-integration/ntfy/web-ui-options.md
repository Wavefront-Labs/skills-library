---
id: computing-software.messaging-and-integration.ntfy.web-ui-options
name: web-ui-options
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, web-ui, web-root, require-login, enable-signup]
level: practitioner
status: docs-checked
description: "Control the ntfy web app on a self-hosted server: disable it, require login, or enable signup and topic reservations."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web UI options

| Key | Env | Default | Effect |
|---|---|---|---|
| `web-root` | `NTFY_WEB_ROOT` | `/` | web app root path, or `disable` |
| `enable-login` | `NTFY_ENABLE_LOGIN` | `false` | login via web app or API |
| `enable-signup` | `NTFY_ENABLE_SIGNUP` | `false` | signup via web app or API |
| `enable-reservations` | `NTFY_ENABLE_RESERVATIONS` | `false` | users reserve topics (tier permitting) |
| `require-login` | `NTFY_REQUIRE_LOGIN` | `false` | login required for all web app actions |

```yaml
web-root: disable
```

or

```yaml
require-login: true
```

## Notes

- The web app is a static site with no backend beyond the ntfy API; its data stays in the browser. The FAQ considers exposing it harmless if the backend is protected by ACLs.
- `--disallowed-topics` (env `NTFY_DISALLOWED_TOPICS`, repeatable) blocks topic names.

## Checked

2026-11-04. Confirmed against the ntfy config page (options table defaults, disallowed-topics flag) and FAQ (static web app, ACLs). Removed: the Verify step.
Method: documentation only; no commands were run.
