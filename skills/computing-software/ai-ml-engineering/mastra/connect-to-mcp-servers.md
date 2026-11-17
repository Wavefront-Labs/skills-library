---
id: computing-software.ai-ml-engineering.mastra.connect-to-mcp-servers
name: connect-to-mcp-servers
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, mcp, mcpclient, mcpserver, tool-approval, toolsets, registries, mcp-apps]
level: practitioner
status: docs-checked
description: "Connect Mastra agents to MCP servers with MCPClient, load static or per-request tools, require approval, harden security, and expose your own MCPServer."
sources:
  - https://mastra.ai/docs/connections/mcp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use external MCP tools in a Mastra agent and publish your own. `MCPClient` and `MCPServer` speak the MCP `2026-07-28` revision over stdio and Streamable HTTP.

## Connect
```bash
npm install @mastra/mcp@latest
```
```typescript
import { MCPClient } from '@mastra/mcp'
export const mcpClient = new MCPClient({
  id: 'my-mcp-client',
  servers: {
    wikipedia: { command: 'npx', args: ['-y', 'wikipedia-mcp'] },
    weather: {
      url: new URL('https://weather.example.com/mcp'),
      requestInit: { headers: { Authorization: `Bearer ${process.env.WEATHER_API_KEY}` } },
    },
  },
})
```
Give an agent the tools with `tools: await mcpClient.listTools()`. For OAuth-protected servers use `authenticate()`.

## Static vs runtime tools
| | Static | Runtime |
| - | - | - |
| Method | `listTools()` | `listToolsets()` |
| Use | fixed shared config | per-user or per-request credentials |
| Agent API | `tools` in `Agent` constructor | `toolsets` in `generate()`/`stream()` |

For runtime, build an `MCPClient` per request with that user's key, call `agent.generate(prompt, { toolsets: await userMcpClient.listToolsets() })`, then `await userMcpClient.disconnect()`.

## Approval and security
- `requireToolApproval: true` on a server, or a function such as `({ toolName }) => toolName.startsWith('delete_')`. Treat annotations from servers you don't control as untrusted hints.
- Stdio subprocesses inherit only the MCP SDK's curated environment whitelist; set `inheritDefaultEnv: false` to pass only variables in `env`.
- Set `allowedHosts` when HTTP URLs come from untrusted config. A custom `fetch` must enforce its own redirect policy.
- Tool results are untrusted model input: sanitize with input/output processors and use approval for sensitive tools.

## Generate types (optional)
Pass `typegen: { outFile: 'src/mcp/mcp-types.generated.ts' }` and the generated `MCPServers` interface to `new MCPClient<MCPServers>(...)`, then run `npx @mastra/mcp generate ./src/mcp/client.ts` with credentials and env loaded. Discovery lists schemas without executing tools. Narrow results before use.

## Registries
Klavis AI, mcp.run (signed URL, treat as secret), Composio, Smithery, Apify, Ampersand all work with the same client config. Keep URLs, keys and tokens in env vars.

## Expose a server
```typescript
export const mcpServer = new MCPServer({
  id: 'my-mcp-server', name: 'My MCP Server', version: '1.0.0',
  agents: { assistant }, tools: { weatherTool }, workflows: { weatherWorkflow },
})
// new Mastra({ mcpServers: { mcpServer } })
```
Served at `/api/mcp/:serverId/mcp` over Streamable HTTP. A tool needing user input calls `context.suspend()` with a `resumeSchema`; the client answers via the `inputRequests` handler. For an npx-runnable stdio package, add an entry file with a shebang that calls `mcpServer.startStdio()` and point `bin` at the built file.

MCP Apps and MCP events (SEP-3415, a draft, experimental) are covered in the page: link a tool to a `ui://` resource via `mcp._meta.ui.resourceUri` with `appResources`; events use `defineEvent()` and `mcp.events.subscribe()`.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. Clarified SEP-3415 refers to MCP events. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
