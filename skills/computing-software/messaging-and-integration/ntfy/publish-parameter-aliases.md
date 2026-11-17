---
id: computing-software.messaging-and-integration.ntfy.publish-parameter-aliases
name: publish-parameter-aliases
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, headers, aliases, query-parameters, parameters]
level: intro
status: docs-checked
description: "Lookup of every ntfy publish header with its aliases, and the rules for header versus query parameter casing."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publish options and aliases

Header names are case-insensitive. Query parameters must be lowercase.

| Header | Aliases |
|---|---|
| `X-Message` | `Message`, `m` |
| `X-Title` | `Title`, `t` |
| `X-Sequence-ID` | `Sequence-ID`, `SID` |
| `X-Priority` | `Priority`, `prio`, `p` |
| `X-Tags` | `Tags`, `Tag`, `ta` |
| `X-Delay` | `Delay`, `X-At`, `At`, `X-In`, `In` |
| `X-Timezone` | `Timezone` |
| `X-Actions` | `Actions`, `Action` |
| `X-Click` | `Click` |
| `X-Attach` | `Attach`, `a` |
| `X-Markdown` | `Markdown`, `md` |
| `X-Icon` | `Icon` |
| `X-Filename` | `Filename`, `file`, `f` |
| `X-Email` | `X-E-Mail`, `Email`, `E-Mail`, `mail`, `e` |
| `X-Call` | `Call` |
| `X-Cache` | `Cache` |
| `X-Firebase` | `Firebase` |
| `X-UnifiedPush` | `UnifiedPush`, `up` |
| `X-Poll-ID` | `Poll-ID` (internal, used for iOS push) |

`Authorization` and `Content-Type` have no aliases; `Content-Type: text/markdown` enables Markdown.

## Checked

2026-11-04. Confirmed every header and alias row against the ntfy publish page (List of all parameters), plus the case rule and Content-Type: text/markdown. Removed: the alias-style gotcha and the Verify step, which the page does not state.
Method: documentation only; no commands were run.
