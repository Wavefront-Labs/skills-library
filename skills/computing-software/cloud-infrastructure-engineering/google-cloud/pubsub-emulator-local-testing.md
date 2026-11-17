---
id: computing-software.cloud-infrastructure-engineering.google-cloud.pubsub-emulator-local-testing
name: pubsub-emulator-local-testing
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, pubsub, pubsub-emulator, local-development, integration-testing, docker]
level: practitioner
status: docs-checked
description: "Run the Pub/Sub emulator locally or in CI, point client libraries at it with PUBSUB_EMULATOR_HOST, create topics and subscriptions, and know what it does not emulate."
sources: ["https://docs.cloud.google.com/pubsub/docs/emulator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pub/Sub emulator

## 1. Start it
```bash
gcloud components install pubsub-emulator
gcloud beta emulators pubsub start --project=local-test --host-port=localhost:8085
```

## 2. Point clients at it
```bash
$(gcloud beta emulators pubsub env-init)     # Linux/macOS: exports PUBSUB_EMULATOR_HOST from the running emulator
export PUBSUB_PROJECT_ID=local-test
```
On Windows, redirect the `env-init` output to a `.cmd` file and run it. Except for Java, C# and Rust, client libraries use the emulator automatically when `PUBSUB_EMULATOR_HOST` is set (the docs list Java, C# and Rust as needing explicit setup). `PUBSUB_PROJECT_ID` is optional. The emulator has no topics or subscriptions at first: create them in test setup (resources and messages are kept for the lifetime of the emulator session):
```python
from google.cloud import pubsub_v1
pub, sub = pubsub_v1.PublisherClient(), pubsub_v1.SubscriberClient()
t = pub.create_topic(name=pub.topic_path("local-test", "orders"))
sub.create_subscription(name=sub.subscription_path("local-test", "orders-sub"), topic=t.name)
```
The emulator does not support the Google Cloud console or `gcloud pubsub` commands; use client code.

## Gotchas
- Documented limitations include: no IAM operations, no UpdateTopic or UpdateSnapshot RPCs, no configurable message retention (messages are retained indefinitely), and BigQuery subscriptions can be created but do not deliver to BigQuery. See the emulator page for the full list.
- Leaving `PUBSUB_EMULATOR_HOST` set in a shell that runs production code sends traffic to the emulator instead of the service.
- Use the real service in a sandbox project for tests that depend on unsupported features.

## Verify
- [ ] An integration test publishes and receives a message against the emulator.

## Checked
Checked 2026-10-24 against the Pub/Sub emulator documentation (docs.cloud.google.com). Confirmed install command, `start --project`, `env-init`, `PUBSUB_EMULATOR_HOST`, optional `PUBSUB_PROJECT_ID`, library behaviour, no gcloud pubsub support, session-lifetime state and the listed limitations. Removed the Docker command, REST example, push-subscription advice and unlisted limitation claims, which the page does not confirm.
Method: documentation only; no commands were run.
