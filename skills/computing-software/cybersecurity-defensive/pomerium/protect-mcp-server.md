---
id: computing-software.cybersecurity-defensive.pomerium.protect-mcp-server
name: protect-mcp-server
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [mcp-server, mcp-route, mcp-inspector, streamable-http, mcp-oauth]
level: practitioner
status: docs-checked
description: "Front an internal MCP server with a Pomerium route so MCP clients authenticate via OAuth, and verify it with MCP Inspector."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/mcp/protect-mcp-server.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium proxies an internal MCP server so clients (Claude, ChatGPT, VS Code and others) can reach it while the server needs no auth logic of its own. External clients authenticate through Pomerium, deny policies can block destructive tools, and every tool call appears in authorize log fields.

Route:

```yaml
routes:
  - from: https://my-mcp-server.your-domain.com
    to: http://my-mcp-server.int:8080/mcp
    name: My MCP Server
    mcp:
      server: {}
    policy:
      allow:
        and:
          - domain:
              is: company.com
      deny:
        and:
          - mcp_tool:
              starts_with: 'admin_'
```

`mcp: server: {}` marks an MCP server route; the empty braces are required.

Steps:
1. Run the MCP server; it must support the HTTP Streamable transport.
2. Add the route.
3. Give the client the Pomerium route URL; it completes OAuth, gets a bearer token and uses it afterwards.
4. Verify: `npx -y @modelcontextprotocol/inspector@latest`, choose Streamable HTTP, enter the route URL, enable OAuth (Quick OAuth Flow), Connect, then Tools, List Tools.

See mcp-tool-deny-policies for tool-level controls.

## Checked

2026-11-04. Read the Protect an MCP Server page: purpose, route config, the significance of the empty braces, Streamable HTTP requirement, client OAuth flow and MCP Inspector steps confirmed. Nothing removed.

Method: documentation only; no commands were run.
