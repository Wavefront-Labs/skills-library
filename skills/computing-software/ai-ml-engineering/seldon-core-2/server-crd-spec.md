---
id: computing-software.ai-ml-engineering.seldon-core-2.server-crd-spec
name: server-crd-spec
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, server, crd, serverconfig, capabilities, replicas, podspec]
level: practitioner
status: docs-checked
description: "Define a Seldon Core 2 Server: serverConfig reference, replicas, extraCapabilities, capabilities, imageOverrides, podSpec overrides and disableAutoUpdate."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/server.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server custom resource

A Server defines an inference server onto which Models are placed. A default installation deploys two server StatefulSets, one MLServer and one Triton, so you only define more for advanced cases.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Server
metadata:
  name: mlserver
spec:
  serverConfig: mlserver
  replicas: 1
```

The one required field is `serverConfig`, which names a ServerConfig resource.

## ServerSpec fields
- `serverConfig`: the ServerConfig to build from (required).
- `extraCapabilities`: capabilities added to those from the ServerConfig.
- `capabilities`: capabilities that override the ones from the ServerConfig.
- `imageOverrides`: container overrides for the `agent` and `rclone` containers.
- `podSpec`: PodSpec overrides; slices such as `containers` are appended, not replaced.
- scaling fields, inlined from ScalingSpec (the example sets `replicas`).
- `disableAutoUpdate`: when true, a change to the referenced ServerConfig is not applied to the Server immediately; explicit changes to the Server itself still force a reconcile.

Models find a Server by matching their `requirements` against the Server capabilities, or by naming it in `spec.server`.

## Checked
2026-11-09. Confirmed against docs-gb/kubernetes/resources/server.md (Seldon Core v2 branch): the default MLServer and Triton StatefulSets, the example Server, `serverConfig` as the main requirement, every ServerSpec field and comment (`extraCapabilities`, `capabilities`, `imageOverrides` for `agent` and `rclone`, `podSpec` append semantics, inline ScalingSpec, `disableAutoUpdate`), and targeting a server by name from a Model. Removed: the claim that the scaling fields are `minReplicas` and `maxReplicas` (the page only shows `replicas` and names ScalingSpec).
Method: documentation only; no commands were run.
