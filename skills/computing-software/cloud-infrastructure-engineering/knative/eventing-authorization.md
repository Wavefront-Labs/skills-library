---
id: computing-software.cloud-infrastructure-engineering.knative.eventing-authorization
name: eventing-authorization
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [eventpolicy, authorization, defaultauthorizationmode, allow-same-namespace, authentication-oidc]
level: advanced
status: docs-checked
description: "Restrict who may send events with EventPolicy resources and the defaultAuthorizationMode flag."
sources:
  - https://knative.dev/docs/eventing/features/authorization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control which senders may deliver events to eventing resources.

Knative Eventing offers the `EventPolicy` custom resource to specify which subjects may send events to a resource.

Prerequisites:
- Eventing installed.
- The `authentication-oidc` feature enabled. The page notes that `transport-encryption` should be enabled too for secure authentication.

Supported targets:
- Brokers: MTChannelBasedBroker and the Kafka Broker.
- Channels: InMemoryChannel and KafkaChannel.
- Flows: Sequence and Parallel.
- Others: KafkaSink.

Default behavior comes from the `defaultAuthorizationMode` feature flag, used whenever no EventPolicy applies to a resource:
- `allow-all`: all requests are allowed.
- `deny-all`: all requests are denied, enforcing the creation of EventPolicies.
- `allow-same-namespace`: only requests from subjects in the same namespace are allowed. This is the default.

Practical order:
1. Turn on OIDC authentication.
2. Choose the default mode in the feature flags.
3. Define EventPolicy resources for the targets that need exceptions to the default.

A request that passes no applicable EventPolicy is rejected with `403 Forbidden`; if several policies apply to a resource, matching at least one is enough. `EventPolicy` is `eventing.knative.dev/v1alpha1` on the page, with `spec.to` (`ref` or `selector`; empty means every resource in the namespace), `spec.from` (`ref` or `sub`, where `sub` may end in `*`) and optional `spec.filters`, which must also match. The upstream tracking issue is number 7256 in knative/eventing.

## Checked

2026-11-04. Confirmed against the Knative Eventing Authorization page (knative/docs source): the `EventPolicy` resource, prerequisites (`authentication-oidc`, with `transport-encryption` recommended), the compatibility list (MTChannelBasedBroker, Kafka Broker, InMemoryChannel, KafkaChannel, Sequence, Parallel, KafkaSink), the `defaultAuthorizationMode` values and the `allow-same-namespace` default, the 403 rejection and at-least-one-policy rule, and tracking issue 7256. Added the `spec.to`, `spec.from` and `spec.filters` summary from the same page. Nothing removed.

Method: documentation only; no commands were run.
