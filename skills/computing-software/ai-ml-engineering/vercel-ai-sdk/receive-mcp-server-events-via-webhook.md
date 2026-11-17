---
id: computing-software.ai-ml-engineering.vercel-ai-sdk.receive-mcp-server-events-via-webhook
name: receive-mcp-server-events-via-webhook
category: computing-software
field: ai-ml-engineering
product: vercel-ai-sdk
tags: [mcp-events, webhook, event-store, subscription, experimental-events]
level: sme
status: docs-checked
description: "Subscribe to MCP server events with client.experimental_events and receive signed webhook deliveries via experimental_createMCPEventWebhook and an event store."
sources:
  - https://ai-sdk.dev/docs/ai-sdk-core/mcp-events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: have an MCP server notify your app (for example a new comment) through a verified webhook. Experimental; webhook delivery only, no polling or push streams.

## Choose who manages subscriptions
- `experimental_events: { adapter }`: a backend manages subscriptions, delivery and renewal. The adapter's `createAdapter({ transport })` receives the transport type and URL. No AI SDK event store needed.
- `experimental_events: { store }`: you register webhooks, persist secrets and schedule renewal (flow below). `list()` works in either mode, or with neither.

## Protocol flow
1. `events/subscribe` carries event name, filters, webhook URL, signing secret, optional `ttlMs` and `cursor`.
2. The server may send a signed challenge; then it returns subscription ID, `refreshBefore`, `cursor`, `truncated`.
3. Events arrive as signed POSTs; the webhook verifies and acknowledges.
4. Renew before `refreshBefore` (same identity) or `events/unsubscribe`. Finite subscriptions expire if not renewed.

Deliveries can be duplicated or reordered: deduplicate by subscription ID and event ID.

## Step 1: expose the webhook route (before subscribing)
```ts
import { experimental_createMCPEventWebhook } from '@ai-sdk/mcp';
export const POST = experimental_createMCPEventWebhook({
  store: eventStore,
  async onEvent({ subscription, event }) { /* event.name, event.data */ },
  async onGap({ subscription, gap }) { /* replay gap: reconcile state */ },
  async onTerminated({ subscription, termination }) { /* termination.error */ },
});
```
It verifies signatures, echoes challenges, never exposes the secret, returns `204` on success and `503` on processing failure so the server retries. Resolve callbacks only after processing or durable acceptance; deduplicate on subscription ID and `messageId` (signed `webhook-id`). After `onGap` succeeds the helper saves `gap.cursor` and `truncated: true`; after `onTerminated` it removes the saved subscription. It does not run an agent for you.

## Step 2: subscribe with the same store
```ts
const client = await createMCPClient({
  transport: { type: 'http', url: 'https://service.example/mcp' },
  experimental_events: { store: eventStore },
});
const { events } = await client.experimental_events.list();
const sub = await client.experimental_events.subscribe({
  name: 'comment.created', arguments: { document_id: 'doc_123' },
  delivery: { mode: 'webhook', url: 'https://my-app.example/api/mcp-events' },
  ttlMs: 60 * 60 * 1000,
});
// persist sub.id, schedule renewal before sub.refreshBefore
await client.close(); // delivery continues until unsubscribe or expiry
```
Also `refresh({ id })` (reuses saved URL, arguments, secret and latest cursor) and `unsubscribe({ id })`.

## The event store
Implement `Experimental_MCPEventStore` with `get`, `getById`, `set`, `update`, `delete`. Use shared durable storage scoped to one MCP server and authenticated principal; `update` must atomically merge fields.

## Gotchas
- The SDK generates and saves `delivery.secret` before `events/subscribe` and appends a `mcp_event_subscription` query parameter to your callback URL. Preserve it and pass the raw request body to the handler.
- Local HTTP callbacks need `delivery.allowInsecureLocalhost: true`; production uses HTTPS.
- A failure after an agent finishes inside `onEvent` yields `503` and a redelivery, so the agent can run twice. Put server, event name, subscription ID and event ID into `runtimeContext` with `telemetry.includeRuntimeContext` to identify duplicate spans; you still must deduplicate.

## Checked

Date: 2026-11-07. Read the 1 cited page(s) in full from the vercel/ai docs source and confirmed the commands, parameters, defaults and error strings above. No content change needed.

Method: documentation only; no commands were run.
