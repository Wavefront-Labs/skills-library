---
id: computing-software.devops-ci-cd.helm.global-flags-and-kube-connection
name: global-flags-and-kube-connection
category: computing-software
field: devops-ci-cd
product: helm
tags: [global-flags, kube-context, kubeconfig, namespace, debug, burst-limit, qps, kube-as-user, kube-token]
level: practitioner
status: docs-checked
description: "Global flags every helm command takes: namespace, kube-context, kubeconfig, impersonation, TLS settings, registry and cache paths."
sources:
  - "https://helm.sh/docs/helm/helm/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

These flags are accepted by all Helm commands:

- `-n, --namespace`: namespace scope for the request.
- `--kube-context`: kubeconfig context name.
- `--kubeconfig`: path to the kubeconfig file.
- `--kube-apiserver`: address and port of the API server.
- `--kube-token`: bearer token for authentication.
- `--kube-as-user` and `--kube-as-group` (repeatable): impersonate a user or groups.
- `--kube-ca-file`: certificate authority file for the API server connection.
- `--kube-insecure-skip-tls-verify`: skip API server certificate verification (makes HTTPS insecure).
- `--kube-tls-server-name`: server name for certificate validation.
- `--debug`: enable verbose output.
- `--burst-limit` (default 100) and `--qps`: client-side throttling for API calls.
- `--registry-config`: path to the OCI registry config file.
- `--repository-cache` and `--repository-config`: repository cache and repo list file.
- `--content-cache`: path to the directory containing cached content such as charts.
- `--color` (also spelled `--colour`): never, auto or always (default auto).

Examples:

```bash
helm --kube-context prod -n web list
helm --kubeconfig /path/to/kubeconfig status app
```

## Checked

2026-11-03. Confirmed against the inherited-options block of the helm reference pages on helm.sh (flag names, descriptions, `--burst-limit` default 100, `--color` values). Removed: the `--no-color` flag and the `(Helm 4)` label (not listed), and the impersonation and throttling advice.
Method: documentation only; no commands were run.

