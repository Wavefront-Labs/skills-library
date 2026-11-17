---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.orchestrate-tools-with-code-mode
name: orchestrate-tools-with-code-mode
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [code-mode, tool-callers, quickjs, execution-policy, tool-discovery]
level: advanced
status: docs-checked
description: "Let a model call AI SDK tools from sandboxed JavaScript with codeModeTool, experimental_toolCallers, executionPolicy limits and runCodeMode."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/code-mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: have the model write a program that calls several tools concurrently and returns a filtered JSON result. Experimental; needs Node.js 22 or newer; not available in browser or edge runtimes. Install `ai @ai-sdk/code-mode zod`.

## Wire it up
```ts
import { DIRECT_TOOL_CALL, experimental_codeModeTool as codeModeTool } from '@ai-sdk/code-mode';
import { generateText, isStepCount, tool } from 'ai';

const tools = {
  code_mode: codeModeTool({ executionPolicy: { timeoutMs: 30_000 } }),
  getInventory, getDemand, // normal tool({ inputSchema, outputSchema, execute }) definitions
} as const;

const result = await generateText({
  model, tools,
  experimental_toolCallers: { getInventory: ['code_mode'], getDemand: ['code_mode'] },
  stopWhen: isStepCount(10),
  prompt: 'Compare inventory and demand for product sku_123.',
});
```
Keys of `experimental_toolCallers` are the governed tools; values are allowed callers. Listed tools are not exposed to the model as direct tools unless you add `DIRECT_TOOL_CALL` (`['code_mode', DIRECT_TOOL_CALL]`). Tools without an entry keep direct calling. The code mode description includes TypeScript signatures generated from input and output schemas, so precise schemas, descriptions and `inputExamples` improve generated code.

The model's program uses the global `tools` object and top-level `await` / `return`:
```ts
const [inventory, demand] = await Promise.all([
  tools.getInventory({ productId: 'sku_123' }), tools.getDemand({ productId: 'sku_123' }),
]);
return { sufficient: inventory.availableUnits >= demand.requestedUnits };
```
Names that are not valid identifiers use brackets: `tools['lookup-user']`.

## Keep the tool definition stable
`codeModeTool({ toolDiscovery: 'conversation' })` puts the current tool catalog in a user message instead of the tool description, so the provider-visible definition does not change. Changed tools produce a new catalog that replaces earlier ones. Cache benefits depend on the provider.

## Limits
Override with `executionPolicy`: `timeoutMs` (includes tool waits), `cpuTimeoutMs`, `memoryLimitBytes`, `maxStackSizeBytes`, `maxSourceBytes`, `maxResultBytes`, `maxConsoleOutputBytes`, `maxToolInputBytes`, `maxToolOutputBytes`, `maxBridgeRequests`, `maxInFlightBridgeRequests`. Cap concurrent workers process-wide with `experimental_setMaxWorkers(4)`; without it code mode picks a cap from available memory, up to 32.

## Run a program directly
```ts
import { experimental_runCodeMode as runCodeMode } from '@ai-sdk/code-mode';
const out = await runCodeMode({ js: 'return await tools.getInventory({ productId: "sku_123" });', tools: { getInventory } });
```

## Gotchas
- Return only JSON-serializable values; TypeScript is only type-stripped, never type-checked.
- Await every tool call; returning with detached calls fails the invocation and aborts them.
- Supported: `Promise.all`, `JSON`, `console.log/info/debug/error`. Not available: `process`, `require`, `fetch`, `eval`, file system.
- Approval is not integrated: a nested tool that needs approval is rejected. Keep approval-gated tools directly callable.
- Tools run in the host, outside QuickJS. Treat generated code and arguments as untrusted and authorize and validate inside each tool.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
