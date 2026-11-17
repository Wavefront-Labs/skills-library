---
id: computing-software.messaging-and-integration.dapr.sidecar-http-limits-and-grpc-protocol
name: sidecar-http-limits-and-grpc-protocol
category: computing-software
field: messaging-and-integration
product: dapr
tags: [annotations, http-max-request-size, http-read-buffer-size, app-protocol, grpc, dapr-run, service-invocation]
level: practitioner
status: docs-checked
description: "Raise the sidecar 4 MB body and 4 KB header limits and switch the sidecar to app-protocol grpc: dapr-http-max-request-size, dapr-http-read-buffer-size, and their annotations."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/increase-request-size.md
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/increase-read-buffer-size.md
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/grpc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three sidecar settings that commonly need tuning, each available as a `dapr run` flag and a Kubernetes annotation.

Large request bodies: the default HTTP body limit is 4 MB.

```bash
dapr run --dapr-http-max-request-size 16 node app.js
```

sets 16 MB; on Kubernetes use the annotation `dapr.io/http-max-request-size: "16"` in the pod template.

Large headers: the default HTTP header read buffer is 4 KB. Oversized headers can surface as a `Too big request header` error during service invocation.

```bash
dapr run --dapr-http-read-buffer-size 16 node app.js
```

sets 16 KB; the annotation is `dapr.io/http-read-buffer-size: "16"`.

gRPC to the app: Dapr offers HTTP and gRPC APIs for local calls, and it can also call your app over gRPC if the app hosts a gRPC server implementing the Dapr `appcallback` service.

```bash
dapr run --app-protocol grpc --app-port 5005 node app.js
```

On Kubernetes:

```yaml
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "myapp"
        dapr.io/app-protocol: "grpc"
        dapr.io/app-port: "5005"
```

The annotations go in the Deployment pod template, as in the page examples.

## Checked

2026-11-04. Defaults, flags and annotations confirmed on the large HTTP body, large HTTP header and gRPC configuration pages.

Method: documentation only; no commands were run.
