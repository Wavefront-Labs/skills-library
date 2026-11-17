---
id: computing-software.ai-ml-engineering.mastra.pubsub-backends
name: pubsub-backends
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, pubsub, resumable, redis-streams, distributed, workers, event-bus]
level: advanced
status: docs-checked
description: "Choose a Mastra PubSub backend: in-process default, UnixSocket, Redis Streams or Google Cloud; delivery modes, distributed signals and resumable streams via CachingPubSub."
sources:
  - https://mastra.ai/docs/server/pubsub
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick and configure the event bus behind workflows, schedules, background tasks, agent signals and resumable streams.

One backend, set once via the `pubsub` option on `Mastra`, serves all of those systems. Without it Mastra uses `EventEmitterPubSub` (in-process, nothing persisted, fine for a single instance).

## Delivery modes
- Pull: consumers read via a long-lived worker loop (distributed backends such as `RedisStreamsPubSub`).
- Push: events arrive unprompted, in-process or over HTTP.
- Consumer groups: members of a group split events so each is handled once; ungrouped subscribers all receive every event.

## Backends
| Backend | Scope | Mode | Package |
| - | - | - | - |
| `EventEmitterPubSub` | single process | pull and push | `@mastra/core` |
| `UnixSocketPubSub` | processes on one host | push | `@mastra/core` |
| `RedisStreamsPubSub` | multiple hosts | pull | `@mastra/redis-streams` |
| `GoogleCloudPubSub` | multiple hosts | pull | `@mastra/google-cloud-pubsub` |

```typescript
new Mastra({ pubsub: new UnixSocketPubSub('/tmp/mastra/events.sock') }) // from '@mastra/core/events'; one process is elected broker
new Mastra({ pubsub: new RedisStreamsPubSub({ url: 'redis://localhost:6379' }) })
new Mastra({ pubsub: new GoogleCloudPubSub({ projectId: 'my-project' }) })
```

## Distributed deployments
Use a distributed backend when several instances must see the same events; for example, a signal sent to an agent run owned by another instance never arrives with the in-process default. Both distributed backends persist events for redelivery. For durable agent crash recovery when the storage adapter lacks run fencing, recovery relies on backend leases: `RedisStreamsPubSub` provides them across hosts, `GoogleCloudPubSub` doesn't.

## Resumable streams
Reconnecting clients need history. Distributed backends persist events and support replay. For in-process delivery, wrap it:
```typescript
import { CachingPubSub, EventEmitterPubSub } from '@mastra/core/events'
import { InMemoryServerCache } from '@mastra/core/cache'
new Mastra({ pubsub: new CachingPubSub(new EventEmitterPubSub(), new InMemoryServerCache()) })
```
`CachingPubSub` records events per topic so late or reconnecting subscribers catch up before continuing with live events.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
