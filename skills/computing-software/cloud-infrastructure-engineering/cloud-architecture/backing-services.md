---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.backing-services
name: backing-services
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, twelve-factor, 12-factor-app, backing-services, attached-resources, connection-strings, service-binding, swap-without-code-change, local-dev-parity]
level: practitioner
status: docs-checked
description: "Apply factor IV: treat databases, queues, caches and SaaS APIs as attached resources located by config, swappable without code changes, with Kubernetes service binding."
sources: ["https://12factor.net/backing-services", "https://servicebinding.io/spec/core/1.0.0/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor IV: backing services as attached resources

**Rule:** a backing service is any service the app consumes over the network as part of normal operation:
datastores, messaging and queueing systems, SMTP services, caches, and third-party services such as asset
storage, metrics or consumer APIs. The code makes no distinction between local and third-party services; each
is an attached resource reached through a URL or other locator and credentials stored in config.

## Steps
1. Address every backing service through config, not hard-coded hostnames.
2. Swappability test: a local database can be replaced by a managed one, or a local SMTP server by a
   third-party one, by changing only the resource handle in config, with no code change.
3. Each distinct service is its own resource: two databases used for application-layer sharding are two
   resources.
4. Attach and detach at will: if a database misbehaves, restore a new one from a recent backup, attach it and
   detach the old one without code changes.
5. On Kubernetes, the Service Binding specification standardises how a workload receives credentials. A
   provisioned service exposes a Secret through `.status.binding`; a projected binding is volume-mounted at
   `$SERVICE_BINDING_ROOT/<binding-name>` and must contain a `type` entry, with `provider` recommended.

## Gotchas
- Vendor-specific features reduce swappability. That can be acceptable; record it as a deliberate dependency.
- Handle connection failures and reconnects in your own code and driver settings; the factor page does not
  prescribe pool or DNS settings.

## Verify
- [ ] A backing service is swapped by changing config and restarting only.
- [ ] No hostnames or credentials for backing services appear in source.

## Checked
2026-11-01. Confirmed against the 12factor.net Backing Services page and the Service Binding Specification
for Kubernetes 1.0.0 (`.status.binding`, `$SERVICE_BINDING_ROOT`, `type` and `provider` entries). Removed: the
named env var examples, emulator list (MinIO, LocalStack, Azurite), the JVM DNS cache setting and operator
list (Crossplane, ACK, ASO), none of which those pages state.
Method: documentation only; no commands were run.
