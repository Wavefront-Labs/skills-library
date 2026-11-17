---
id: computing-software.ai-ml-engineering.mastra.wrap-external-sdk-agents
name: wrap-external-sdk-agents
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, sdk-agents, claudeagentsdk, cursor, openai-agents-sdk, claudesdkagent, mcp, resume]
level: advanced
status: docs-checked
description: "Register Claude Agent SDK, Cursor SDK and OpenAI Agents SDK agents in Mastra with ClaudeSDKAgent, CursorSDKAgent and OpenAISDKAgent, including tools, resume and structured output."
sources:
  - https://mastra.ai/docs/connections/sdk-agents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run a vendor SDK agent inside a Mastra project. The vendor SDK keeps its own runtime, tools, permissions and agent loop; Mastra gives `generate()`/`stream()` output and observability.

## Install and credentials
- Claude: `npm install @mastra/claude @anthropic-ai/claude-agent-sdk zod`, `ANTHROPIC_API_KEY`
- Cursor: `npm install @mastra/cursor @cursor/sdk`, `CURSOR_API_KEY`
- OpenAI: `npm install @mastra/openai @openai/agents zod`, `OPENAI_API_KEY`

## Create (config goes in `sdkOptions`)
```typescript
new ClaudeSDKAgent({ id: 'claude-sdk-agent', name: 'Claude SDK Agent', description: '...',
  sdkOptions: { model: 'your-claude-model', cwd: process.cwd() } })

new CursorSDKAgent({ id: 'cursor-sdk-agent', name: '...', description: '...',
  sdkOptions: { apiKey: process.env.CURSOR_API_KEY, model: { id: 'your-model' }, local: { cwd: process.cwd() } } })

new OpenAISDKAgent({ id: 'openai-sdk-agent', name: '...', description: '...',
  sdkOptions: { name: 'Repository assistant', instructions: '...', model: 'your-model' } })
```
Cursor local agents require an explicit `sdkOptions.model`. Cursor and OpenAI also accept an existing SDK agent via `agent: cursorAgent` / `agent: sdkAgent` instead of `sdkOptions`. `OpenAISDKAgent` creates the SDK agent on first use.

## Tools
Tools are configured with the vendor SDK, not Mastra's `tools` option or `createTool()`.
- Claude: build with the SDK `tool(name, description, rawZodShape, handler)` (raw shape, not `z.object()`; handler returns MCP content), wrap in `createSdkMcpServer({ name, version, tools })`, pass via `sdkOptions.mcpServers`, and allow with `allowedTools: ['mcp__<server>__<tool>']`.
- Cursor: pass MCP servers through `sdkOptions.mcpServers`.
- OpenAI: create with `tool({ name, description, parameters: z.object(...), execute })` from `@openai/agents` and pass `sdkOptions.tools`.

## Register and run
```typescript
export const mastra = new Mastra({ agents: { claudeSDKAgent, cursorSDKAgent, openaiSDKAgent } })
const agent = mastra.getAgentById('cursor-sdk-agent')
const stream = await agent.stream('Inspect this project and describe the test setup.')
for await (const chunk of stream.textStream) process.stdout.write(chunk)
```

## Resume
`resumeGenerate()` / `resumeStream()` take provider-native data plus `message`: Claude `sessionId`; OpenAI `previousResponseId` (or conversation/session); Cursor continues with the wrapped agent, or pass `agentId` in `resumeData` to resume a stored one.

## Structured output
Claude and OpenAI agents support `structuredOutput: { schema }` and return the value on `result.object`. Cursor throws an error when `structuredOutput` is requested.

## Observability
Mastra records agent and model spans plus SDK-provided usage, tool activity and metadata. Claude runs can include SDK-estimated cost; Cursor and OpenAI include token usage.

Related: coding agents without a dedicated package (Cline, OpenCode) go through the Agent Client Protocol instead.

## Checked
Method: 2026-11-08 read the Mastra SDK agents docs page in full (served as markdown). Install commands, sdkOptions config, tool wiring per SDK, resume data, structured-output limits and observability notes match the page; no content changed (example model IDs left as placeholders in the skill).
