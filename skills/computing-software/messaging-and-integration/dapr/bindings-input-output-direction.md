---
id: computing-software.messaging-and-integration.dapr.bindings-input-output-direction
name: bindings-input-output-direction
category: computing-software
field: messaging-and-integration
product: dapr
tags: [bindings, input-binding, output-binding, direction, triggers, components, options-request]
level: practitioner
status: docs-checked
description: "How Dapr input bindings trigger your app and output bindings call external systems (create, update, delete, exec), plus the direction metadata that avoids waiting for the app."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/bindings/bindings-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The bindings API connects an app to external systems without their SDKs, polling code or WebSocket handling, and lets you switch bindings at runtime with environment-specific component YAML and no code change. The page's example is responding to incoming Twilio SMS without any Twilio SDK. Bindings are developed independently of the Dapr runtime in the components-contrib repository. For plain HTTP targets the page prefers service invocation of non-Dapr endpoints.

Input bindings trigger your application when an external event happens, with an optional payload and metadata.

1. Define the component YAML naming the binding type and its metadata such as connection info.
2. Listen for the event on an HTTP endpoint or with the gRPC proto library.

On startup Dapr sends an OPTIONS request to the app for every defined input binding. If the app wants to subscribe to the binding, Dapr expects a status code of 2xx or 405.

Output bindings let the app invoke external resources, again with optional payload and metadata.

1. Define the component YAML.
2. Call the HTTP endpoint or gRPC method of the binding.
3. Name an output operation. Operations depend on the component and can include `"create"`, `"update"`, `"delete"` and `"exec"`.

Direction: the optional `direction` metadata field declares what a binding supports: `"input"`, `"output"` or `"input, output"`. With it set, the sidecar avoids the state of waiting for the app to become ready, which reduces the lifecycle dependency between the app and the sidecar. The page highly recommends that all input bindings include `direction`.

## Checked

2026-11-08. Input and output binding steps, the startup OPTIONS request, output operations, the HTTP binding note and direction values confirmed on the Bindings overview page. Changed: added the 2xx or 405 expectation and the input-binding recommendation, and dropped an unstated limitation to output-only bindings.

Method: documentation only; every cited page read in full; no commands were run.
