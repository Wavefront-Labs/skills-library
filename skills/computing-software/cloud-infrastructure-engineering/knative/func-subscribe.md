---
id: computing-software.cloud-infrastructure-engineering.knative.func-subscribe
name: func-subscribe
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [func-subscribe, function-triggers, filter-flag, source-broker, cloudevents]
level: practitioner
status: docs-checked
description: "Connect a function to Broker events with func subscribe filters; func deploy then creates Triggers."
sources:
  - https://knative.dev/docs/functions/subscribing-functions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: have a function receive CloudEvents from a Knative Broker.

Prerequisite: Knative Eventing installed on the cluster.

The `subscribe` command connects the function to a set of events. It matches a series of filters on CloudEvent metadata, with a Knative Broker as the source the events are consumed from.

Subscribe to events from a named Broker:

```bash
func subscribe --filter type=com.example --filter extension=my-extension-value --source my-broker
```

Subscribe to events from the default Broker by omitting `--source`:

```bash
func subscribe --filter type=com.example --filter extension=my-extension-value
```

The `kn func subscribe` form takes the same flags.

Deployment with Triggers: when you run `func deploy`, the CLI creates Knative Triggers for the function from its subscriptions. The expected output includes a line saying Triggers are being created on the cluster, before the line reporting the function deployed in its namespace and exposed at a URL.

Run `func deploy` after subscribing so the Triggers are created along with the image build and the Knative Service.

## Checked

2026-11-04. Confirmed against the Subscribe functions to CloudEvents page and its snippet (knative/docs source): the Knative Eventing prerequisite, the purpose of `subscribe` (filters on CloudEvent metadata, a Knative Broker as source), both `func subscribe` examples with `--filter` and `--source`, the `kn func` equivalents, `func deploy` creating Knative Triggers, and the expected output order (image built, Creating Triggers on the cluster, function deployed at a URL). Nothing removed.

Method: documentation only; no commands were run.
