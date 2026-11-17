---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-http-access-log
name: proxy-http-access-log
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, access-log, proxy, observability]
level: practitioner
status: docs-checked
description: "Enable the proxy HTTP access log in apache or json format with an annotation and read it from the proxy container's stderr."
sources:
  - https://linkerd.io/2.19/features/access-logging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set the annotation `config.linkerd.io/access-log` on a namespace or workload to make the proxy log every HTTP request that transits it. The injector turns it into an environment variable on the proxy container.

Values:

- `apache`: Apache Common Log Format, for example `10.42.0.63:51160 traffic.booksapp.serviceaccount.identity.linkerd.cluster.local - [2022-08-23T20:28:20.071809491Z] "GET http://webapp:7000/ HTTP/2.0" 200`
- `json`: structured entries with fields such as `client.addr`, `client.id`, `host`, `method`, `processing_ns`, `request_bytes`, `response_bytes`, `status`, `timestamp`, `total_ns` and a trace id.

```yaml
annotations:
  config.linkerd.io/access-log: json
```

Access logging is off by default because it has a performance cost. It may raise tail latency and CPU consumption under load, depending on traffic.

Where to read it: the access log is written to the proxy container's `stderr`, while the proxy's debug log goes to `stdout`. Today `kubectl logs` outputs both streams together, so filter on the format, for instance by selecting lines that parse as JSON. KEP 3289 proposes a way to separate the streams in `kubectl logs`.

It is distinct from proxy debug logging, which is configured by the proxy log level.

## Checked

2026-11-08. Read in full against the Linkerd 2.19 docs source (markdown in linkerd/website) of https://linkerd.io/2.19/features/access-logging/. Confirmed the annotation, apache and json formats, performance note and stderr versus stdout statements above. Nothing was removed.

Method: documentation only; no commands were run.
