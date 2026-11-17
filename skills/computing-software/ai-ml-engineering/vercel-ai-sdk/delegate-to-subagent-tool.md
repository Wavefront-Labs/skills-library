---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.delegate-to-subagent-tool
name: delegate-to-subagent-tool
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [subagents, toolloopagent, context-isolation, abortsignal, converttomodelmessages]
level: practitioner
status: docs-checked
description: "Let a main agent delegate heavy work to a subagent through a tool whose execute calls subagent.generate, passing abortSignal and handling cancellation."
sources:
  - https://ai-sdk.dev/docs/agents/subagents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: offload context-heavy or parallelizable work so the main agent only sees a short result.

```ts
const researchSubagent = new ToolLoopAgent({
  model,
  instructions: `You are a research agent.
Summarize your findings in your final response.`,
  tools: { read: readFileTool, search: searchTool },
});

const researchTool = tool({
  description: 'Research a topic or question in depth.',
  inputSchema: z.object({ task: z.string().describe('The research task to complete') }),
  execute: async ({ task }, { abortSignal }) => {
    const result = await researchSubagent.generate({ prompt: task, abortSignal });
    return result.text;
  },
});

const mainAgent = new ToolLoopAgent({ model, instructions: '...', tools: { research: researchTool } });
```
The tool call blocks until the subagent finishes, then returns its final text. The subagent runs with its own fresh context window.

When to use: tasks that read many tokens, independent research to parallelize, context that would outgrow model limits, or isolating tool access by capability (for example a read-only exploration subagent, a file-editing subagent, a platform-integration subagent). Avoid for simple focused tasks or when sequential processing suffices; subagents add latency and complexity.

Cancellation: always pass `abortSignal` from the tool's second argument. Aborting stops the subagent with an `AbortError`, which fails the main tool execution and stops the main loop. To avoid incomplete-tool-call errors in later turns, convert history with `await convertToModelMessages(messages, { ignoreIncompleteToolCalls: true })`.

Giving the subagent history: `execute: async ({ task }, { abortSignal, messages }) => researchSubagent.generate({ messages: [...messages, { role: 'user', content: task }], abortSignal })`, then return `.text`. Use sparingly because it defeats some of the context isolation benefits.

Caveats:
- Subagent tools cannot use `toolApproval` (or deprecated `needsApproval`); all must run automatically.
- Write the subagent instructions to end with a clear summary; otherwise it may just say "Done".
- For live progress in the UI see stream-subagent-progress-to-ui.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. Softened "defeats context isolation".

Method: documentation only; no commands were run.
