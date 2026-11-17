---
id: computing-software.ai-ml-engineering.mastra.agent-network-routing
name: agent-network-routing
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, network, routing, routing-agent, deprecated, suspend, resume, agent]
level: advanced
status: docs-checked
description: "Use or migrate deprecated Mastra agent networks: routing agent setup, calling .network(), structured output, network tool approvals, and suspend/resume."
sources:
  - https://mastra.ai/docs/agents/networks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: operate a Mastra routing agent via `.network()`. Agent networks are deprecated and will be removed in a future major release; the page says to replace them with supervisor agents (`agent.stream()`/`generate()` with `agents`) and points to a migration guide.

## Create
A routing agent uses an LLM to choose which subagents, workflows or tools to call. Give it `agents`, `workflows`, `tools` and Memory (required: `.network()` stores task history to decide when the task is complete). Each primitive needs a `description`; workflows and tools also need `inputSchema` and `outputSchema`.

```typescript
export const routingAgent = new Agent({
  id: 'routing-agent',
  name: 'Routing Agent',
  instructions: '...',
  model: 'openai/<model>',
  agents: { researchAgent, writingAgent },
  workflows: { cityWorkflow },
  tools: { weatherTool },
  memory: new Memory({ storage: new LibSQLStore({ id: 'mastra-storage', url: 'file:../mastra.db' }) }),
})
```

## Call
```typescript
const result = await routingAgent.network('Tell me three cool ways to use Mastra')
for await (const chunk of result) {
  if (chunk.type === 'network-execution-event-step-finish') console.log(chunk.payload.result)
}
```

## Structured output
`routingAgent.network('Research AI trends', { structuredOutput: { schema } })`; iterate `stream.objectStream` for partial objects and `await stream.object` for the final value.

## Approvals
A primitive needing approval emits `agent-execution-approval` or `tool-execution-approval`. Respond with `routingAgent.approveNetworkToolCall(chunk.payload.toolCallId, { runId: stream.runId, memory: { thread, resource } })`, or `declineNetworkToolCall()` with the same arguments. Approval uses snapshots, so enable a storage provider.

## Suspend and resume
A primitive calling `suspend()` emits a suspension chunk (for example `tool-execution-suspended`, `workflow-execution-suspended`; read `chunk.payload.suspendPayload`). Continue with `routingAgent.resumeNetwork({ confirmed: true }, { runId: stream.runId, memory: { thread, resource } })`.

Or set `autoResumeSuspendedTools: true` in the `.network()` options so the user's next message resumes it. Requirements: memory configured, the same `thread` and `resource`, and a `resumeSchema` on the tool. Manual suits custom UIs with approval buttons; automatic suits chat-style interfaces.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. Removed guessed migration URL path. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
