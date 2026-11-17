---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-http-serverless-openfaas-kubeless
name: argo-events-trigger-http-serverless-openfaas-kubeless
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, http-trigger, openfaas, kubeless, knative, nuclio, fission, serverlessurl]
level: intro
status: docs-checked
description: "Invoke serverless functions (OpenFaaS, Kubeless, Knative, Nuclio, Fission) from Sensor events with the http trigger."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/http-trigger.md", "https://github.com/argoproj/argo-events/blob/master/docs/APIs.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger http serverless openfaas kubeless

The http trigger doubles as a serverless function invoker.

OpenFaaS: point `url` at the gateway function route. Example with a Redis PubSub EventSource:

```yaml
http:
  url: http://gateway.openfaas.svc.cluster.local:8080/function/gohash
  payload:
    - src:
        dependencyName: test-dep
      dest: bucket
  method: POST
```

Publishing `PUBLISH FOO hello` to the subscribed channel makes the Sensor invoke the `gohash` function.

Kubeless: point `url` at the function Service. The docs page writes this field as `serverURL`, but the API reference lists `serverURL` only on the custom trigger and `url` on the http trigger, so use `url`:

```yaml
http:
  url: http://hello.kubeless.svc.cluster.local:8080
  payload:
    - src:
        dependencyName: test-dep
        dataKey: body.first_name
      dest: first_name
    - src:
        dependencyName: test-dep
        dataKey: body.last_name
      dest: last_name
  method: POST
```

With a NATS EventSource, a message `{"first_name": "foo", "last_name": "bar"}` on subject `foo` invokes the Kubeless function `hello`, which receives the data as the event.

Other frameworks follow the same pattern: the docs say Knative, Nuclio and Fission functions can be triggered the same way with the http trigger.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/http-trigger.md. docs/APIs.md is too large to read in full; only the HTTPTrigger section (field list starts with url) and a search for serverURL (found only under CustomTrigger) were read. Confirmed: OpenFaaS and Kubeless examples, PUBLISH FOO hello, subject foo message, list of other frameworks. Removed or changed: the unsupported closing claim about Service reachability and sensor creation order; the Kubeless field serverURL changed to url, because the page example uses serverURL but the API reference lists serverURL only on CustomTrigger and url on HTTPTrigger. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
