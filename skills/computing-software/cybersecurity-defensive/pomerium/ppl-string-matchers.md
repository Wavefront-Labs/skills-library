---
id: computing-software.cybersecurity-defensive.pomerium.ppl-string-matchers
name: ppl-string-matchers
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [string-matcher, starts-with, not-in-allowlist, email-criterion, domain-criterion]
level: intro
status: docs-checked
description: "Use the PPL string matcher operators (is, in, not_in, contains, starts_with, ends_with) in Pomerium email, domain, path and tool criteria."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/ppl.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Criteria such as `email`, `domain`, `http_method`, `http_path`, `user` and `mcp_tool` take a string matcher.

Keys: `contains`, `ends_with`, `in`, `not_in`, `is`, `starts_with`.

Shorthand: an array, string, number or boolean used directly behaves like `is`.

```yaml
allow:
  and:
    - email:
        ends_with: '@example.com'
```

`not_in` makes an allowlist when placed under `deny`. The docs show this for `mcp_tool`: deny any tool whose name is not in the approved list.

Related matchers:
- String list matcher: key `has`, used by `groups` and `record`; a direct value behaves like `has`.
- `domain` compares only the part of the email after `@`; `email` compares the full address.
- `claim/<name>` matches a token claim exactly, with the claim named by the sub-path.

## Checked

2026-11-04. Read the Pomerium Policy Language page: the six string matcher operators, the shorthand, the not_in deny example for mcp_tool, the string list matcher and the claim sub-path rule all confirmed. Nothing removed.

Method: documentation only; no commands were run.
