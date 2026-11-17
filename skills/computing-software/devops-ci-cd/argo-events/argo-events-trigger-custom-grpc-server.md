---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-custom-grpc-server
name: argo-events-trigger-custom-grpc-server
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, custom-trigger, grpc, fetchresource, execute, applypolicy, serverurl]
level: sme
status: docs-checked
description: "Build your own trigger by running a gRPC server implementing FetchResource, Execute and ApplyPolicy and referencing it with the custom trigger."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/build-your-own-trigger.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger custom grpc server

For logic outside the built-in triggers (the docs mention triggering TektonCD or Airflow pipelines from GitHub events), run a gRPC server implementing the Sensor's `Trigger` service from `pkg/sensors/triggers/trigger.proto`:
- `FetchResource`: fetch the resource to trigger from an external source such as S3, Git or a URL; for a Tekton trigger server, fetch the `PipelineRun` from Git and return it to the Sensor.
- `Execute`: invoke the trigger, such as creating the pipeline resource in the cluster.
- `ApplyPolicy`: check whether the triggered resource reached success; the Sensor then stops or continues with later triggers.

Reference it in the Sensor with the `custom` key:

```yaml
triggers:
  - template:
      name: webhook-workflow-trigger
      custom:
        serverURL: tekton-trigger.argo-events.svc:9000
        spec:
          url: "https://raw.githubusercontent.com/VaibhavPage/tekton-cd-trigger/master/example.yaml"
        parameters:
          - src: {dependencyName: test-dep, dataKey: body.namespace}
            dest: metadata.namespace
    parameters:
      - src: {dependencyName: test-dep, dataKey: body.url}
        dest: custom.spec.url
```

- `serverURL`: address of the gRPC trigger server.
- `spec`: map of string to string sent to the server; its meaning is entirely up to your server.
- `parameters` inside `custom` apply to the resource the server returns; the outer `parameters` apply to the whole template body (so `serverURL` and `spec` can be parameterized).
- `payload`: data to send to the server.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/build-your-own-trigger.md. Confirmed: Trigger service methods FetchResource, Execute, ApplyPolicy, custom key fields serverURL, spec, parameters, payload, and the two parameters levels. Removed or changed: nothing; every claim matched the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
