---
id: computing-software.devops-ci-cd.argo-events.argo-events-generic-eventsource-grpc-contract
name: argo-events-generic-eventsource-grpc-contract
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, generic-eventsource, grpc, proto, custom-eventsource, config]
level: sme
status: docs-checked
description: "Onboard a custom event source with the generic EventSource: implement the Eventing gRPC service and configure url, insecure and config."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/generic.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events generic eventsource grpc contract

The generic EventSource extends Argo Events with your own source through a gRPC contract. The server must implement:

```proto
service Eventing {
    rpc StartEventSource(EventSource) returns (stream Event);
}
message EventSource { string name = 1; bytes config = 2; }
message Event       { string name = 1; bytes payload = 2; }
```

(proto file: `pkg/eventsources/sources/generic/generic.proto`.)

Configure the client:

```yaml
spec:
  generic:
    example:
      insecure: true
      url: "generic-event-source-server.argo-events.svc:8080"
      config: |-
        key1: value1
        key2: value2
```

`config` is free-form; Argo Events does not interpret it, and your server must parse it.

Flow: the client connects to `url` and sends `config` in the RPC; the server parses it and connects to any external system (or produces events itself, such as a special calendar); events stream back; the client writes them to the EventBus for Sensors.

Connection strategy: the client retries indefinitely to connect, including after the server goes down, and resumes receiving over the stream. Generic is listed as an active-passive type on the EventSource High Availability page.

## Checked

2026-11-04. Confirmed against the Generic EventSource page (the proto contract, proto file path, the YAML with `insecure`, `url` and `config`, free-form `config`, the four-step flow and the retry behaviour) and the EventSource High Availability page (Generic is Active-Passive). The skill drops the proto `package generic;` line and comments, which do not change the contract. Nothing else removed.
Method: documentation only; no commands were run.
