---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-http-request-payload-and-policy
name: argo-events-trigger-http-request-payload-and-policy
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, http-trigger, payload, policy, status-allow, retrystrategy, rest]
level: practitioner
status: docs-checked
description: "Call REST APIs from a Sensor with the http trigger, build the JSON payload from event data and mark success by allowed status codes."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/http-trigger.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger http request payload and policy

The HTTP trigger calls REST APIs and serverless functions, moving event consumption out of your API server. Basic form:

```yaml
http:
  url: http://http-server.argo-events.svc:8090/hello
  method: POST        # GET, DELETE, POST, PUT, HEAD, ...
  payload:
    - src:
        dependencyName: test-dep
        dataKey: notification.0.s3.bucket.name
      dest: bucket
    - src:
        dependencyName: test-dep
        contextKey: type
      dest: type
```

`payload` is a list of `src` (an event dependency plus a `dataKey` in the data or a `contextKey` in the context) mapped to a `dest` key in the request body. The example generates `{"type": "minio", "bucket": "input"}`; add as many pairs as needed.

Policy: to judge success by the response code, add

```yaml
retryStrategy:
  steps: 3
  duration: 3s
policy:
  status:
    allow:
      - 200
      - 201
```

The trigger is then successful only when the response is 200 or 201. `parameters` can additionally rewrite the URL and other fields on the fly. Walkthrough: Go server printing the body, Minio event source, `examples/sensors/http-trigger.yaml`, drop a file in the `input` bucket.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/http-trigger.md. Confirmed: payload src (dataKey or contextKey) and dest, generated body, retryStrategy and policy.status.allow, parameterization, walkthrough. Removed or changed: nothing; every claim matched the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
