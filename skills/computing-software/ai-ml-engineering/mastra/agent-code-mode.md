---
id: computing-software.ai-ml-engineering.mastra.agent-code-mode
name: agent-code-mode
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, codemode, sandbox, createcodemode, tools, isolated-vm, quickjs, agent]
level: advanced
status: docs-checked
description: "Configure Mastra code mode with createCodeMode so agents orchestrate tools in one sandboxed TypeScript call: scoping, remote sandboxes, in-process isolation."
sources:
  - https://mastra.ai/docs/agents/code-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let an agent write one function that calls several tools (exposed as `external_*` functions) and returns an aggregated result, run in a sandbox. Added in `@mastra/core@1.38.0`.

Why: fewer round-trips, smaller context (results reduced in code), arithmetic done in JavaScript, parallel calls via `Promise.all`. Your tools still run on the host with validation, request context and tracing; only the model's orchestration code runs in the sandbox.

## Quickstart
```typescript
import { createCodeMode } from '@mastra/core/tools'
import { LocalSandbox } from '@mastra/core/workspace'

const { tool, instructions } = createCodeMode({
  tools: { getTopProducts, getProductRatings },
  sandbox: new LocalSandbox(), // required; runs a host node process with host privileges
})

const agent = new Agent({
  id: 'shop-assistant',
  name: 'shop-assistant',
  instructions: ['You are a helpful shopping assistant.', instructions],
  model: 'openai/<model>',
  tools: { execute_typescript: tool },
})
```
The default tool id is `execute_typescript`. The model emits code such as `await external_getTopProducts({ limit: 5 })`. Because model-authored code runs, choose the execution boundary deliberately (pass `sandbox` or use a workspace that provides one); `LocalSandbox` is for trusted or local development only. Keep tools focused so the model composes them.

## Scope tools
Each `createCodeMode()` call captures its own allow-list. Give each a distinct `id` and add each `instructions` to the agent:
```typescript
const sales = createCodeMode({ id: 'sales_code', tools: { listRecentOrders, getCustomer }, sandbox })
const inventory = createCodeMode({ id: 'inventory_code', tools: { listProducts, getSupplier }, sandbox })
// agent tools: { sales_code: sales.tool, inventory_code: inventory.tool }
```
Generated code for one cannot call the other's tools.

## Remote sandboxes
The default transport writes the program to the host filesystem and runs `node`, which fails for remote micro-VM sandboxes. For E2B pass a transport as the second argument:
```typescript
import { E2BSandbox, E2BCodeModeTransport } from '@mastra/e2b'
createCodeMode({ tools, sandbox: new E2BSandbox() }, new E2BCodeModeTransport())
```

## In-process isolation (no sandbox needed)
- `new IsolatedVmCodeModeTransport({ memoryLimitMb: 128 })` from `@mastra/isolated-vm`: V8 isolate with no filesystem, network or process access; only the `external_*` bridge. It is a native addon, and on Node.js 20 and later the host process must start with `--no-node-snapshot`.
- `new QuickJsCodeModeTransport({ memoryLimitMb: 128 })` from `@mastra/quickjs`: QuickJS compiled to WebAssembly, for hosts that cannot install native addons or set Node flags (common on serverless); slower.

Use as `createCodeMode({ tools }, transport)`.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
