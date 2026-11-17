---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-log-level-endpoint
name: proxy-log-level-endpoint
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, proxy, logging, debugging, admin-port]
level: practitioner
status: docs-checked
description: "Raise a running proxy's log level through its admin port without restarting the pod, and persist it with an annotation."
sources:
  - https://linkerd.io/2.19/tasks/modifying-proxy-log-level/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Proxy debug logging is expensive, so by default proxies only log exceptional events. You can change the level of a live proxy through the `/proxy-log-level` endpoint on its admin port (4191 by default, named `linkerd-admin`):

```sh
kubectl port-forward ${POD:?} linkerd-admin
curl -v --data 'linkerd=debug' -X PUT localhost:4191/proxy-log-level
kubectl logs ${POD:?}
```

The change lasts only for the life of the pod. To keep it across restarts, add the `config.linkerd.io/proxy-log-level` annotation to the pod template.

Notes:

- Logging has a noticeable negative impact on proxy throughput. If the pod still serves production traffic, put the level back when you finish.
- Proxy debug logging is separate from the HTTP access log. The access log is configured with its own annotation, `config.linkerd.io/access-log`.
- The value uses the log directive syntax described in the proxy log level reference, so you can target a single module instead of raising everything.

A reasonable workflow is to port-forward to the one pod showing the problem, set a narrow directive, reproduce, read `kubectl logs`, then reset the log level once you are done.

## Checked

2026-11-08. Read in full against the Linkerd 2.19 docs source (markdown in linkerd/website) of https://linkerd.io/2.19/tasks/modifying-proxy-log-level/. Confirmed the admin endpoint usage, persistence annotation and throughput note. Removed an unsourced reset-directive suggestion.

Method: documentation only; no commands were run.
