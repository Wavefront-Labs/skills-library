---
id: computing-software.cybersecurity-defensive.pomerium.mcp-tool-deny-policies
name: mcp-tool-deny-policies
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [mcp-tool, tool-allowlist, tools-call, mcp-log-fields, deny-block]
level: practitioner
status: docs-checked
description: "Limit which MCP tools users can call through Pomerium with the mcp_tool criterion in deny blocks, allowlists, and log verification."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/mcp/limit-mcp-tools.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`mcp_tool` is a string matcher on the tool `name` in `tools/call` payloads. Operators: `is`, `starts_with`, `ends_with`, `contains`, `in`, `not_in`.

It applies only to `tools/call`; for `tools/list`, `resources/list` and similar methods it evaluates false. A matching deny returns 403 Forbidden.

Rule: put `mcp_tool` under `deny` and identity checks (domain, groups, email) under `allow`. If `mcp_tool` appears only under `allow`, non-call requests such as `tools/list` are denied.

Patterns (route has `mcp: server: {}`):
- Block one tool: deny `mcp_tool: { is: drop_table }`.
- Block a category: deny `starts_with: 'admin_'`.
- Allowlist: deny `not_in: ['query', 'list_tables']`.
- Combined: allow `domain` and `groups: has: data-analysts`; deny `or` of `in: ['update_data', 'drop_table', 'delete_records']` and `starts_with: 'admin_'`.

Find tool names with MCP Inspector (`npx -y @modelcontextprotocol/inspector@latest`) or `tools/list`.

Verify with logs:

```yaml
authorize_log_fields:
  - request-id
  - email
  - mcp-method
  - mcp-tool
```

Allowed shows `"allow-why-true": ["domain-ok", "mcp-tool-ok"]`; blocked shows `"allow-why-false": ["mcp-tool-unauthorized"]`.

## Checked

2026-11-04. Read the Limit MCP Tool Calling page: operators, tools/call-only scope, deny-versus-allow placement and its gotcha, the four patterns, inspector command, log fields and sample log values all confirmed. Nothing removed.

Method: documentation only; no commands were run.
