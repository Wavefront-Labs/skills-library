---
id: computing-software.systems-network-administration.apache-guacamole.kubernetes-connection
name: kubernetes-connection
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, kubernetes, kubernetes-parameters, exec-command, namespace, pod, container, client-cert, ca-cert, kubectl-attach]
level: practitioner
status: docs-checked
description: "Connect Guacamole to a Kubernetes pod console: hostname, port 8080, namespace, pod, container, exec-command vs attach, TLS parameters."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes connections

Parameters:
| Parameter | Default / notes |
|---|---|
| `hostname` | required (API server) |
| `port` | 8080 |
| `namespace` | `default` |
| `pod` | required |
| `container` | first container in the pod |
| `exec-command` | with it: like `kubectl exec`; without: like `kubectl attach` |
| `use-ssl` | disabled |
| `client-cert`, `client-key` | PEM files for client authentication |
| `ca-cert` | PEM CA; without it only system CAs are trusted |
| `ignore-cert` | `false` |

Notes:
- Kubernetes uses the terminal engine, so font, colour scheme, scrollback, typescript recording and clipboard options apply (apache-guacamole.clipboard-and-terminal-display).
- Enable `use-ssl` for any API server that is not plain HTTP and supply `ca-cert`; use `ignore-cert=true` only for testing.

Example connection: `protocol=kubernetes`, `hostname`, `pod`.

Verify: the connection opens a shell (exec-command like `/bin/sh`) or attaches to the running process.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Partial read of the Guacamole manual Configuring Guacamole page: the whole Kubernetes section was read; other sections were not. Confirmed: hostname, port 8080, namespace default, pod, container defaulting to the first, exec-command versus kubectl exec and attach, use-ssl, client-cert, client-key, ca-cert, ignore-cert, the terminal engine and the shared feature list, and the example connection. Removed the Pango build claim, which this page does not state.
