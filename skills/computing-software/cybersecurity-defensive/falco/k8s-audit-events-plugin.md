---
id: computing-software.cybersecurity-defensive.falco.k8s-audit-events-plugin
name: k8s-audit-events-plugin
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [k8saudit, kubernetes-audit, k8s-audit, webserver, audit-rules]
level: practitioner
status: docs-checked
description: "Receive Kubernetes audit events via the k8saudit plugin web server, and port old rules to list fields, exists and the intersects operator."
sources:
  - https://falco.org/docs/concepts/event-sources/plugins/kubernetes-audit/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Falco 0.32.0 Kubernetes audit support is the k8saudit plugin. The plugin embeds a web server that listens on a configurable port and accepts POST requests on a configurable endpoint; the posted JSON object is the event. It must be configured in the `plugins` section of `falco.yaml` with init config and open parameters (see the plugin README).

Default rules are in the k8saudit plugin rules, and a daemon install places `k8s_audit_rules.yaml` in `/etc/falco/`. They cover privileged pods, sensitive host path mounts, host networking, overly broad grants such as `cluster-admin`, and ConfigMaps holding credentials. A rule looks like:

```yaml
- rule: Configmap contains private credentials
  condition: kevt and configmap and kmodify and contains_private_credentials
  priority: WARNING
  source: k8s_audit
  tags: [k8s]
```

The docs page prints the condition as `... and modify and ...`, but the macro it defines is `kmodify` (`ka.verb in (create,update,patch)`), so use that name. `kevt` selects events whose `jevt.value[/stage]` is in the `k8s_audit_stages` list (`ResponseComplete`), and `configmap` is `ka.target.resource=configmaps`.

Enabling audit logs is done on the cluster: add `--audit-policy-file` and `--audit-webhook-config-file` arguments to `kube-apiserver` with an audit policy and webhook config. Dynamic audit webhooks were removed from Kubernetes; static configuration still works. Managed providers usually have their own mechanism.

Differences from the legacy implementation:
- List fields support only `in` and `intersects`. Replace `ka.req.role.rules.verbs contains create` with `ka.req.role.rules.verbs intersects (create)`.
- Test failed extraction with `exists`, not by comparing with `<NA>`, which is no longer returned. `ka.target.subresource != <NA>` is now always false.
- `/healthz` of Falco cannot bind to the same port as the plugin's audit endpoint, since two independent web servers manage them.
- Syscalls and k8s audit sources on one instance work from Falco 0.33.0 onward; 0.32.x did not allow it.

## Checked

2026-11-08. Read the Kubernetes Audit Events page in full. Fixed the rule example to use the macro name kmodify (the docs page prints modify, which is undefined); added kube-apiserver flags and the removed dynamic webhooks note.

Method: documentation only; no commands were run.
