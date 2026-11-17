---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.secure-mcp-tools-with-annotations-approval-and-drift-detection
name: secure-mcp-tools-with-annotations-approval-and-drift-detection
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [mcp-tools, tool-approval, rug-pull, fingerprint-tools, tool-annotations]
level: advanced
status: docs-checked
description: "Gate MCP tools by readOnlyHint annotations with toolApproval and pin approved definitions with fingerprintTools and detectToolDrift against rug-pull changes."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use third-party MCP tools without trusting server-supplied hints or silently mutated definitions.

## 1. Treat annotations as untrusted hints
MCP servers may annotate tools: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`. The client exposes them on each tool's `metadata.annotations` and on the tool call's `toolMetadata.annotations`. They do **not** become an approval policy automatically; combine with allowlists, scoped credentials and your own `toolApproval`. Conservative policy: auto-run only explicit read-only tools.
```ts
import { type McpProviderMetadata } from '@ai-sdk/mcp';
const result = streamText({
  model, tools,
  toolApproval: ({ toolCall }) => {
    const a = (toolCall.toolMetadata as McpProviderMetadata | undefined)?.annotations;
    return a?.readOnlyHint === true ? 'not-applicable' : {
      type: 'user-approval',
      reason: a?.destructiveHint === true
        ? 'The MCP server marks this tool as destructive.'
        : 'The MCP server does not mark this tool as read-only.',
    };
  },
  prompt,
});
```
Tools with `readOnlyHint: false` or no hint then require user approval. (The repo has a local tool-annotations example under examples/mcp, run with `pnpm server:tool-annotations` and `pnpm client:tool-annotations`.)

## 2. Detect tool-definition drift ("rug pull")
A server can send a different description or widened schema for the same tool name on a later `mcpClient.tools()` call, and the SDK would use it as-is. Pin approved definitions:
```ts
import { fingerprintTools, detectToolDrift } from 'ai';
const baseline = await fingerprintTools(await mcpClient.tools()); // at human-reviewed trust time; persist it
// every later fetch, before generateText:
const tools = await mcpClient.tools();
const drift = detectToolDrift(await fingerprintTools(tools), baseline);
if (drift.changed.length || drift.added.length) { /* block, force re-approval or alert */ }
```
`fingerprintTools` digests the string `description`, resolved input schema and `title` into a map of tool name to digest; `detectToolDrift` diffs two maps (`changed`, `added`).

## Limits
- Your app owns baseline storage and the reaction; core does not persist or block anything.
- It cannot detect a behaviour or endpoint swap where name, description and schema are unchanged, since the tool runs remotely.

## Related controls
- OAuth to MCP: implement `validateAuthorizationServerURL` on the `authProvider` to allow only trusted authorization-server origins; the hook runs before metadata is fetched. Pre-registered confidential clients must set `issuer` in `clientInformation()` exactly matching the discovered issuer. Pass the callback `iss` as `callbackIssuer` to `auth` from `@ai-sdk/mcp`.
- HTTP redirects default to `'error'`.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
