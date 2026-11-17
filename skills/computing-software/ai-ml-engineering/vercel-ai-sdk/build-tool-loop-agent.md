---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.build-tool-loop-agent
name: build-tool-loop-agent
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [building-agents, toolloopagent, runtimecontext, toolscontext, createagentuistreamresponse, structured-output]
level: practitioner
status: docs-checked
description: "Create a reusable ToolLoopAgent with instructions, tools, runtimeContext and toolsContext, structured output and toolChoice, then call generate, stream or a UI route."
sources:
  - https://ai-sdk.dev/docs/agents/building-agents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define an agent once and reuse it across routes and scripts.

```ts
import { ToolLoopAgent, tool } from 'ai';
import { z } from 'zod';

const agent = new ToolLoopAgent({
  model: 'openai/gpt-6-luna',
  instructions: 'You are a helpful assistant.',
  tools: {
    searchTickets: tool({
      description: 'Search support tickets',
      inputSchema: z.object({ query: z.string() }),
      contextSchema: z.object({ apiKey: z.string(), accountId: z.string() }),
      execute: async ({ query }, { context }) => searchTickets(query, context.accountId, context.apiKey),
    }),
  },
  runtimeContext: { requestId: 'req_abc', escalated: false },
  toolsContext: { searchTickets: { apiKey: process.env.SUPPORT_API_KEY!, accountId: 'acct_123' } },
});
```

Configuration: the constructor accepts the same settings as `generateText` and `streamText`.
- `instructions`: role, rules, tool-usage guidance, output style.
- `runtimeContext`: shared agent state, visible in `prepareStep`, lifecycle callbacks and results. `toolsContext` (keyed by tool name) carries server-side values such as credentials; declare the shape with the tool `contextSchema` and read it as `context` in `execute`.
- `toolChoice`: `'auto'` (default), `'required'`, `'none'`, or `{ type: 'tool', toolName: 'weather' }`.
- `output: Output.object({ schema })` for structured output, read with `const { output } = await agent.generate({ prompt })`.
- `stopWhen`: default is `isStepCount(20)` (see run-multi-step-tool-loops-with-stopwhen-and-preparestep).
- `toolApproval: { runCode: 'user-approval' }` requires approval before a tool runs.
- Per-call dynamic context: `callOptionsSchema` plus `prepareCall` (see set-agent-call-options).

Use it:
- `await agent.generate({ prompt })` then `result.text`.
- `const result = await agent.stream({ prompt })` then `for await (const chunk of result.textStream)`.
- API route: `return createAgentUIStreamResponse({ agent: myAgent, uiMessages: messages })`.
- Types for the client: `export type MyAgentUIMessage = InferAgentUIMessage<typeof myAgent>` and `useChat<MyAgentUIMessage>()`.

Experimental sandbox: tools receive `experimental_sandbox` in their second execute argument; pass `experimental_sandbox` to `generate()` / `stream()`. Its description is not added to the prompt automatically, and passing it does not sandbox the tool; the tool must call `experimental_sandbox.run({ command, workingDirectory, abortSignal })` itself.

Gotchas:
- A `prepareStep` return such as `{ temperature: 0.1 }` applies to the current step only.
- The agent loop also ends when a tool has no `execute`, when a call needs approval, or on a non-tool-calls finish reason.
- Lifecycle callbacks (`onStart`, `onStepStart`, `onToolExecutionStart`, `onToolExecutionEnd`, `onStepEnd`, `onEnd`) may be set on the constructor and on `generate()` / `stream()`; both run, constructor first.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
