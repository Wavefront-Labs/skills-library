---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.add-agent-memory
name: add-agent-memory
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [agent-memory, anthropic-memory-tool, mem0, letta, custom-tool]
level: practitioner
status: docs-checked
description: "Choose and wire persistent memory for a ToolLoopAgent using the Anthropic memory tool, a memory provider such as Mem0 or Letta, or a custom tool."
sources:
  - https://ai-sdk.dev/docs/agents/memory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let an agent save and recall information across conversations.

Choosing (effort / flexibility / lock-in): provider-defined tools (low / medium / yes), memory providers (low / low / depends), custom tool (high / high / no).

1. Provider-defined tool, Anthropic: implement storage in `execute`.
```ts
const memory = anthropic.tools.memory_20250818({
  execute: async action => { /* action.command, action.path ... return a string */ },
});
const agent = new ToolLoopAgent({ model: 'anthropic/claude-haiku-5.5', tools: { memory } });
```
Commands: `view`, `create`, `str_replace`, `insert`, `delete`, `rename`, each with a `path` scoped to `/memories`. Map them to a filesystem or database. Works only with Claude.

2. Memory providers (storage, retrieval and injection handled for you):
- Letta: `pnpm add @letta-ai/vercel-ai-sdk-provider`; `model: lettaCloud()` with `providerOptions: { letta: { agent: { id: 'your-agent-id' } } }`; optional `lettaCloud.tool('core_memory_append' | 'memory_insert' | 'memory_replace')`.
- Mem0: `pnpm add @mem0/vercel-ai-provider`; `createMem0({ provider: 'openai', mem0ApiKey, apiKey })` then `model: mem0('gpt-6-astra', { user_id: 'user-123' })`; explicit `addMemories(messages, { user_id })` and `retrieveMemories(prompt, { user_id })`.
- Supermemory: `pnpm add @supermemory/tools`; `tools: supermemoryTools(process.env.SUPERMEMORY_API_KEY!)` gives `addMemory` and `searchMemories`.
- Hindsight: `createHindsightTools({ client, bankId: 'user-123' })`; tools `retain`, `recall`, `reflect`, `getMentalModel`, `getDocument`. Create the tools inside the request handler so each request gets the right bank.
- MongoDB (`@mongodb-developer/vercel-ai-memory`, targets AI SDK v6): `createMongoDBMemory({ uri, embedder: openai.embedding('text-embedding-3-small') })`, then `tools: mongodbMemory({ userId, sessionId })` with `stopWhen: isLoopFinished()` so memory tools can read and write before the answer. Session memory is tool-driven (prototypes) or hook-driven via `prepareCall` plus `onEnd` (recommended for production).

3. Custom tool: structured actions (`view`, `create`, `update`, `search`; safe by design) or bash-backed (sandboxed `cat`, `grep`, `sed`, `echo`; needs command validation).

Gotcha: with memory providers the provider controls what is stored and retrieved, and you depend on an external service; with a custom tool you own both.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
