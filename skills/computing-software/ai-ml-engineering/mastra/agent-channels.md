---
id: computing-software.ai-ml-engineering.mastra.agent-channels
name: agent-channels
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, channels, slack, discord, webhooks, tool-approval, chat-sdk, serverless]
level: advanced
status: docs-checked
description: "Connect a Mastra agent to Slack, Discord, Teams and more via Chat SDK adapters: webhook routes, thread context, approval cards, formatting, media and serverless setup."
sources:
  - https://mastra.ai/docs/channels
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: expose a Mastra agent in messaging platforms using Chat SDK adapters (added in `@mastra/core@1.22.0`).

## Configure
```typescript
import { createSlackAdapter } from '@chat-adapter/slack'
export const yourAgent = new Agent({
  id: 'your-agent', name: 'Your Agent', instructions: 'You are a helpful assistant.', model: 'openai/<model>',
  channels: { adapters: { slack: createSlackAdapter() } },
})
```
Adapters need provider env vars (bot tokens, signing secrets, etc.; names are in the platform guide or Chat SDK catalog). Configure `storage` on `Mastra` (e.g. `LibSQLStore`) to preserve subscriptions and tool approvals across restarts. Mastra Connect can manage channel credentials for you.

## Webhooks
Route per adapter: `/api/agents/<AGENT_ID>/channels/<PLATFORM>/webhook` (e.g. `/api/agents/your-agent/channels/slack/webhook`). Point the platform's webhook/event/interactions URL here. Local dev: `npx cloudflared tunnel --url http://localhost:4111`; swap to the production URL after deploy.

Delivery: the webhook acknowledges before the agent finishes (200 means received). Bad requests are rejected first: `401` failed verification, `400` unparseable body, `503` transient state failure; the platform redelivers on non-2xx. After the 200 Mastra owns errors; the default handler posts an error (customize with `formatError`, default `Error: {message}` style). A throwing custom handler is only logged, so catch failures yourself. Redeliveries can duplicate events; dedupe is best effort, so make custom handler side effects idempotent.

## Thread context
On the first mention in a non-DM thread Mastra saves earlier messages into memory (`source: 'thread-history'`): the first message plus up to `maxMessages - 1` recent ones (default `maxMessages` 10), with an omitted-messages marker. Disable: `threadContext: { maxMessages: 0 }`. Without memory (or on write failure) the history is passed as context text. Set memory `lastMessages` to at least `maxMessages + 1` (default 10 trims history). `threadContext: { addSystemMessage: false }` skips the channel/platform system message. Group chats prefix messages like `[Alice (@U123ABC)]: ...`.

## Tool approval
Tools with `requireApproval: true` render as Approve/Deny cards. Only the requester may answer; set per adapter `{ adapter: createSlackAdapter(), toolApprovers: 'anyone' }` for shared channels (runs with no recorded requester, e.g. scheduled, may let another member respond; requester-only mode rejects clicks if several requesters are possible after restart). `toolDisplay: 'text'` renders plain text; `'hidden'` suppresses buttons and, with memory, `autoResumeSuspendedTools` can resume data-bearing `suspend()` flows on a later message (approval-required tools stay suspended until explicit approve/decline). A custom `toolDisplay` function (return `{ kind: 'post', message: card }`) replaces rendering for every tool event; the default action handler only resumes if button ids are the ones it expects.

`handlers.onAction: async (event, defaultHandler, ctx) => {...}` handles your own cards; call `defaultHandler()` for others. `onAction: false` disables all action handling including approval buttons. More Chat SDK handlers: `agent.getChannels()?.sdk`.

## Formatting and reply control
Replies post as markdown (converted per platform). `textFormat: 'plain'` per adapter posts literal text (affects final reply text only). `textDisplay: 'hidden'` stops posting reply text so the agent speaks only through tools; text still reaches the stream and memory.

## Handlers and metadata
Handlers: `onDirectMessage(thread, message, defaultHandler, ctx)`, `onMention`, `onAction`. `ctx.signalMetadata.x = ...` attaches JSON-serializable, non-sensitive per-message context (not added to the prompt; may be stored or sent over shared pubsub). Use `requestContext` for run-scoped config like credentials. Batches from `chatOptions.concurrency` (`burst`, `debounce`, `queue`) are split into one turn per sender; await `defaultHandler` so turns don't overlap.

Runs not started by a message (schedule, Studio prompt, signal) get the same channel instructions; inbound messages carry a `platform` attribute.

## Multimodal
```typescript
channels: {
  adapters: { discord: createDiscordAdapter() },
  inlineMedia: ['image/*', 'video/*', 'audio/*'],
  inlineLinks: [{ match: 'youtube.com', mimeType: 'video/*' }, { match: 'youtu.be', mimeType: 'video/*' }, 'imgur.com'],
}
```
Default `inlineMedia: ['image/*']`; unsupported types become text summaries.

## Serverless
- `waitUntil`: pass it in `channels` (e.g. `import { waitUntil } from '@vercel/functions'`) so the platform keeps the instance alive. Vercel and AWS Lambda require it; Cloudflare Workers and Netlify Functions are auto-detected; `resolveWaitUntil` for runtimes with it on the request context.
- Shared pubsub: in-memory pubsub cannot cross instances, so a follow-up can start a second run on the same thread. Use `new Mastra({ agents, pubsub: new RedisStreamsPubSub({ url: process.env.REDIS_URL, keyPrefix: 'mastra:my-app' }) })` from `@mastra/redis-streams`.

## Other adapters
Any compatible Chat SDK adapter factory works in `channels.adapters`; check its docs for credentials, scopes, attachments and whether it needs long-running listeners or separate routes.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. Replaced placeholder model string with openai/<model>. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
