---
id: computing-software.cloud-infrastructure-engineering.linkerd.tap-access-rbac-and-ignore-headers
name: tap-access-rbac-and-ignore-headers
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, tap, rbac, viz, security]
level: advanced
status: docs-checked
description: "Control who can use Linkerd tap with Kubernetes RBAC and hide sensitive headers with tap.ignoreHeaders."
sources:
  - https://linkerd.io/2.19/tasks/securing-linkerd-tap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tap shows live requests and may expose sensitive data such as request and response headers. Two controls limit that: the `tap.ignoreHeaders` configuration field, which excludes specific headers from capture, and Kubernetes RBAC for access to tap.

Tap is used by `linkerd viz tap`, `linkerd viz top`, `linkerd viz profile --tap` and `linkerd viz dashboard`. Depending on your RBAC setup, users may need extra permissions.

Check whether your user can tap:

```bash
kubectl auth can-i watch pods.tap.linkerd.io --all-namespaces
```

If the check shows you need more access, you can grant it with as much granularity as you choose. The default ClusterRole `linkerd-linkerd-viz-tap-admin` allows `watch` on `*.tap.linkerd.io`; bind it to a user with `kubectl create clusterrolebinding`. The role name includes the Viz namespace, so it varies if Viz is installed in a non-default namespace. Binding `cluster-admin` also works but is not recommended for production. GKE has its own section in the guide because Google Cloud IAM can make `can-i` report access that your RBAC user lacks.

The dashboard has tap privileges by default through the `linkerd-linkerd-viz-web-admin` ClusterRoleBinding. To restrict that, install Viz with `--set dashboard.restrictPrivileges` or delete that ClusterRoleBinding.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/tasks/securing-linkerd-tap/. Purpose of tap.ignoreHeaders, the commands that use tap, the can-i check, the tap-admin ClusterRole and binding, cluster-admin warning, GKE caveat, the dashboard ClusterRoleBinding and restrictPrivileges option.

Removed or reworded: The practice bullets and the closing re-check advice (not on the cited page).

Method: documentation only; no commands were run.
