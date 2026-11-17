---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.connect-mcp-server-and-load-tools
name: connect-mcp-server-and-load-tools
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [mcp-tools, create-mcp-client, http-transport, structured-content, max-retries]
level: practitioner
status: docs-checked
description: "Create an MCP client with createMCPClient, pick HTTP, SSE or stdio transport, load tools with or without schemas, retry transient failures, and close it."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools
  - https://ai-sdk.dev/docs/reference/ai-sdk-core/create-mcp-client
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use an MCP server's tools in `generateText` / `streamText`.

## Create the client (package `@ai-sdk/mcp`)
```ts
import { createMCPClient } from '@ai-sdk/mcp';
const mcpClient = await createMCPClient({
  transport: {
    type: 'http',                       // recommended for production
    url: 'https://your-server.com/mcp',
    headers: { Authorization: 'Bearer my-api-key' },
    // authProvider: myOAuthClientProvider, redirect: 'follow' (default 'error' to prevent SSRF)
  },
  maxRetries: 2,                        // opt-in; default 0; only tools/call
});
```
Transports: `type: 'http'` (recommended) or the official `StreamableHTTPClientTransport`; `type: 'sse'`; stdio (`StdioClientTransport` from the MCP SDK or `StdioMCPTransport` from `@ai-sdk/mcp/mcp-stdio`), for local servers only because it cannot be deployed to production; or your own `MCPTransport` implementation (`start`, `send`, `close`, `onclose`, `onerror`, `onmessage`). Config also includes `clientName` (default `ai-sdk-mcp-client`), `version`, `capabilities`, `initializationOptions` (signal and timeout), `onUncaughtError`, `protocolVersionDiscovery`.

Protocol: the client supports legacy initialize and stateless MCP `2026-07-28`; stdio probes `server/discover` then falls back to `initialize`. Set `protocolVersionDiscovery: false` for a known legacy endpoint. The client is lightweight: no automatic session persistence, resumable streams or in-band notifications.

## Load tools
```ts
const tools = await mcpClient.tools();   // schema discovery: all server tools, untyped
```
Schema definition (typed, and only the listed tools are loaded):
```ts
const tools = await mcpClient.tools({ schemas: {
  'get-weather': { inputSchema: z.object({ location: z.string() }),
                   outputSchema: z.object({ temperature: z.number(), conditions: z.string() }) },
  'tool-with-no-args': { inputSchema: z.object({}) },   // zero-input tools need an empty object
}});
```
With `outputSchema` the client reads `structuredContent`, validates it, and falls back to parsing JSON from text content; otherwise it errors. Without it you get the raw `CallToolResult` (`content`, optional `isError`). Other methods: `listTools`, `toolsFromDefinitions`, `callTool({ name, arguments })`, and fields `serverInfo`, `instructions` (good for the system prompt), `initializeResult`.

## Close it
Streaming: `onEnd: async () => { await mcpClient.close(); }`. Non-streaming: try/finally with `await mcpClient?.close()`. Short-lived requests close when done; long-running CLIs close on exit.

## Retries and errors
Retries cover transient HTTP/network failures only; JSON-RPC errors and results with `isError: true` are not retried. Only enable retries for idempotent tools (email or create-record tools could duplicate side effects). Initialization failures throw `MCPClientError` (`code`, `statusCode`, `url`, `responseBody`; redact before logging); a missing `statusCode` does not mean retryable. Tool failures surface as `CallToolError`; OAuth failures as `UnauthorizedError` / `MCPClientOAuthError`.

## Gotchas
- With OpenAI Responses you can instead use the built-in `openai.tools.mcp`.

## Checked

Date: 2026-11-07. Read the 2 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Removed the production-versus-MCP gotcha (not on the cited pages).

Method: documentation only; no commands were run.
