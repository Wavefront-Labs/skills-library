---
id: computing-software.devops-ci-cd.skaffold.port-forwarding
name: port-forwarding
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [portforward, forwarding, localport, services]
level: practitioner
status: docs-checked
description: "Forward container, service and user-defined ports to localhost, and learn the defaults per command."
sources:
  - "https://skaffold.dev/docs/port-forwarding/"
  - "https://skaffold.dev/docs/environment/templating/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Skaffold forwards ports from exposed Kubernetes resources to your machine in `dev`, `debug`, `deploy` and `run`. Forwarding classes: `user` (explicit entries in `skaffold.yaml`), `services`, `debug` (ports enabled by `skaffold debug`) and `pods` (all `containerPort`s of pods running Skaffold-built images).

Defaults per command, from the docs table:

| Command | Modes |
|---|---|
| `skaffold dev` | `user` |
| `skaffold dev --port-forward` | `user`, `services` |
| `skaffold debug` | `user`, `debug` |
| `skaffold debug --port-forward` | `user`, `services`, `debug` |
| `skaffold deploy` / `skaffold run` | off |
| `skaffold deploy --port-forward` / `skaffold run --port-forward` | `user`, `services` |

`--port-forward=off` disables forwarding everywhere.

User-defined rules:

```yaml
portForward:
- resourceType: service
  resourceName: web
  namespace: default
  port: 80
  address: 127.0.0.1
  localPort: 8080
```

Fields: `resourceType` (`pod`, `service`, `deployment`, `replicaset`, `statefulset`, `replicationcontroller`, `daemonset`, `job`, `cronjob` or `container`), `resourceName`, `port` (all three mandatory), `namespace` (defaults to the current namespace, or `default`), `address` (default `127.0.0.1`; use `0.0.0.0` to make it reachable from other hosts) and `localPort` (optional). `portForward.namespace` and `portForward.resourceName` support templating. For controllers, `kubectl port-forward` picks one pod.

Port selection: if the requested local port is unavailable, Skaffold forwards to a random open port. For automatic forwards, a matching local port is requested only when the remote port is above 1023 (a service on port 80 maps to some port of 1024 or higher). User-defined forwards can bind system ports.

With the docker deployer, user-defined forwards must use `resourceType: container`, otherwise Skaffold does not tell Docker to expose the port.

Prefer explicit user rules for anything you rely on and pin `localPort` for stable URLs.

## Checked

2026-11-04. Read the Skaffold Port Forwarding page and the Templated Fields page. Confirmed the classes, the default-mode table, `--port-forward=off`, rule fields and defaults, the above-1023 rule, container type for Docker deployments, and that namespace and resourceName are templated. Removed: the unconfirmed warning that automatic service forwarding "can pick random local ports" beyond what the page states, and the "read the printed lines" tip. Note: the field table says `localPort` defaults to `port`, while the schema description says Skaffold picks a random open port when the port is unavailable; both are consistent with the page text above.
Method: documentation only; no commands were run.
