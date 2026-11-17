---
id: computing-software.ai-ml-engineering.mastra.create-first-mastra-agent
name: create-first-mastra-agent
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, agent, instructions, generate, stream, quickstart, typescript]
level: intro
status: docs-checked
description: "Scaffold a Mastra project, define an Agent with model and instructions, register it on Mastra, and call generate or stream."
sources:
  - https://mastra.ai/docs/agents/overview
  - https://mastra.ai/docs/develop
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get a Mastra `Agent` defined, registered and answering calls, then test it locally.

## Setup (condensed quickstart)
- `package.json` with `{ "type": "module" }`, then `npm install @mastra/core@latest zod@latest typescript@latest @types/node@latest mastra@latest`.
- tsconfig.json: target/module `ES2022`, `moduleResolution: bundler`, `strict`, `skipLibCheck`, `types: ["node"]`, `noEmit`, `allowImportingTsExtensions`, include `src/**/*`.
- `model` is a string in `provider/model` format (for example `openai/<model>`, not `openai:<model>`). Do not import a provider object or install an AI SDK package. The provider's env var must be set: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` or `GOOGLE_API_KEY`.

## Define the agent
```typescript
// src/mastra/agents/test-agent.ts
import { Agent } from '@mastra/core/agent'

export const testAgent = new Agent({
  id: 'test-agent',
  name: 'Test Agent',
  instructions: 'You are a helpful assistant.',
  model: 'openai/<model>',
})
```
`instructions` are the system-level prompt defining behavior and expertise.

## Register it
```typescript
// src/mastra/index.ts
import { Mastra } from '@mastra/core'
import { testAgent } from './agents/test-agent'

export const mastra = new Mastra({ agents: { testAgent } })
```
Registered agents get shared resources (memory, logging, observability) and can be called from workflows, tools or other agents.

## Call it
Fetch with `mastra.getAgentById('test-agent')` (a directly imported agent works with its own local config but lacks instance-level storage, logging and the agent registry).
```ts
const agent = mastra.getAgentById('test-agent')
const response = await agent.generate('Help me organize my day')
console.log(response.text) // result also has toolCalls, toolResults, steps, usage

const stream = await agent.stream('Help me organize my day')
for await (const chunk of stream.textStream) process.stdout.write(chunk)
```
`stream()` also exposes promises for `toolCalls`, `toolResults`, `steps` and `usage` that resolve when it finishes. Node.js 22.18.0+ can run TypeScript directly; include file extensions on local imports.

## Run and test locally
`npx mastra dev` starts Studio at http://localhost:4111 and an API browser at http://localhost:4111/api. Changes under `src/mastra/` restart the server automatically.

## Alternative: file-based agent
Under `src/mastra/agents/writing-assistant/` add `config.ts` (`export default agentConfig({ model: 'openai/<model>' })`, importing `agentConfig` from `@mastra/core/agent`) and `instructions.md`. The directory name becomes the agent `id` and `name`. Discovery only runs via `mastra dev` or `mastra build`; if your app imports `mastra` directly (web framework, server adapter) these agents are not discovered, so register in code instead.

## Choosing agents
Agents suit open-ended tasks where steps are not known in advance; use workflows for predetermined multi-step processes.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
