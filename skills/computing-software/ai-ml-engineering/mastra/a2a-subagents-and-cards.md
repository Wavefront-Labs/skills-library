---
id: computing-software.ai-ml-engineering.mastra.a2a-subagents-and-cards
name: a2a-subagents-and-cards
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, a2a, agent-to-agent, subagents, agent-card, push-notifications, a2aagent, mastraclient]
level: advanced
status: docs-checked
description: "Consume remote A2A agents in Mastra with A2AAgent, call A2A endpoints with the client SDK, handle input-required resume, push notifications and signed agent cards."
sources:
  - https://mastra.ai/docs/connections/a2a
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: delegate work to a remote A2A agent (or call a Mastra A2A endpoint) with discovery, resume, push and card verification.

## Discovery
With the default `apiPrefix` of `/api`, an agent registered as `weather-agent` exposes the card at `/api/.well-known/weather-agent/agent-card.json` and the execution endpoint at `/api/a2a/weather-agent`. Mastra supports A2A v0.3 and v1.0 on the same URLs; the `A2A-Version` header selects (missing, empty or `0.3` = v0.3, `1.0` = v1.0, anything else = `VersionNotSupported`).

## Consume a remote agent as a subagent
```typescript
import { Agent } from '@mastra/core/agent'
import { A2AAgent } from '@mastra/core/a2a'

const remote = new A2AAgent({
  url: 'https://weather.example.com/api/.well-known/weather-agent/agent-card.json',
  protocolVersion: '1.0', // omit for v0.3
  headers: { Authorization: `Bearer ${process.env.WEATHER_AGENT_TOKEN}` },
})
export const supportAgent = new Agent({ id: 'support-agent', name: 'Support Agent',
  instructions: '...', model: 'your-model', agents: { remote } })
```
- A domain URL makes it fetch `/.well-known/agent-card.json` (single-agent servers). For multi-agent servers pass the full card URL.
- Other options: `retries`, `backoffMs`, `maxBackoffMs`, `timeoutMs`, `credentials`, `fetch`, `abortSignal`.
- If the card does not advertise streaming, `stream()` falls back to generate and returns a buffered stream.

## Call from application code
```typescript
import { MastraClient } from '@mastra/client-js'
const client = new MastraClient({ baseUrl: 'https://agent.example.com', headers: { Authorization: `Bearer ${process.env.AGENT_API_TOKEN}` } })
const a2a = client.getA2A('weather-agent')
const card = await a2a.getAgentCard()
const stream = a2a.sendMessageStream({ message: { kind: 'message', role: 'user',
  messageId: crypto.randomUUID(), parts: [{ kind: 'text', text: "What's the weather in Prague?" }] } })
for await (const event of stream) if (event.kind === 'artifact-update') console.log(event.artifact.parts)
```
Set `apiPrefix` if the server is not on `/api`. After a dropped stream use `a2a.resubscribeTask({ id: 'task-123' })`. For v1.0 use `client.getA2AV1(...)` (adds `listTasks()`, with `ListTasksRequest.fromJSON` from `@mastra/core/a2a/v1`; also `getTask`, `cancelTask`).

## Human in the loop
A suspended server task becomes `input-required`; the client resumes by sending a follow-up message with the same `taskId`. As a client, `A2AAgent` returns `finishReason: 'suspended'` with a `suspendPayload` for `input-required` or `auth-required`; continue with `resumeGenerate(data, { runId })` or `resumeStream()`. Resuming needs storage on the server.

## Push notifications
For agents advertising `capabilities.pushNotifications`: `a2a.setTaskPushNotificationConfig({ taskId, pushNotificationConfig: { url, token } })`. Sent on completed, failed, canceled, rejected, input-required, auth-required; best-effort.

## Trust
- Sign cards on the server: `new Mastra({ server: { a2a: { agentCardSigning: { privateKey, protectedHeader: { alg: 'ES256', kid } } } } })`. Verify on the client with `getAgentCard({ verifySignature: { algorithms: ['ES256'], keyProvider: async ({ kid, jku }) => ... } })`; verification is opt-in.
- Parent-side check: `A2AAgent({ verifyAgentCard: { verify: async (card, context) => { ... throw to reject } } })`.

## Gotchas (from the page)
- Task records and push configs are in memory: a paused task resumes only on the same server process; restart or unsticky scaling gives task-not-found, and push configs must be re-registered.
- Protect callback URLs, validate tokens, and avoid internal network targets as push destinations.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
