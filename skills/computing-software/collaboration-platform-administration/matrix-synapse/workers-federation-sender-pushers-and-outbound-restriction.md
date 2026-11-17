---
id: computing-software.collaboration-platform-administration.matrix-synapse.workers-federation-sender-pushers-and-outbound-restriction
name: workers-federation-sender-pushers-and-outbound-restriction
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, workers, federation-sender, pusher-instances, send-federation, outbound-federation-restricted-to, sygnal]
level: advanced
status: docs-checked
description: "Offload outbound federation and push to workers with federation_sender_instances, pusher_instances and outbound_federation_restricted_to."
sources:
  - https://element-hq.github.io/synapse/latest/workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Outbound federation and push notifications can each be moved to workers that need no inbound HTTP routing.

**Federation senders.** Use generic workers and list them in `federation_sender_instances` by `worker_name`, and stop the main process sending with `send_federation: false`:

```yaml
send_federation: false
federation_sender_instances:
    - federation_sender1
    - federation_sender2
```

All instances must be stopped and started when adding or removing senders. The docs say the dedicated `synapse.app.federation_sender` app is likely to be deprecated and is not recommended for new installs. These workers handle no REST endpoints.

**Pushers.** Generic workers can send push notifications to a push gateway such as sygnal, and email. Naming them in `pusher_instances` stops the main process doing so:

```yaml
pusher_instances:
  - pusher_worker1
  - pusher_worker2
```

With several, the work is balanced across them. Restart the main process and all pusher workers after changing the option. They need no incoming HTTP, so no extra reverse proxy rules. This supersedes the legacy `synapse.app.pusher`, which instead used `start_pushers: false` in the shared config.

**Restrict outbound traffic.** `outbound_federation_restricted_to` ensures outbound federation only leaves through chosen workers, so you can firewall every other worker and allow only the senders to reach the internet. Set a `worker_replication_secret` alongside it:

```yaml
outbound_federation_restricted_to:
  - federation_sender1

worker_replication_secret: "secret_secret"
```

In the docs' example, `federation_sender1` is also listed in `instance_map` with a host and port.

## Checked

Method: docs-checked 2026-11-09 against docs/workers.md (Synapse develop branch, raw markdown, read in full).
