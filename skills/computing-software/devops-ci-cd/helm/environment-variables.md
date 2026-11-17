---
id: computing-software.devops-ci-cd.helm.environment-variables
name: environment-variables
category: computing-software
field: devops-ci-cd
product: helm
tags: [environment-variables, helm-debug, helm-namespace, helm-kubecontext, helm-registry-config, kubeconfig, qps, burst-limit]
level: practitioner
status: docs-checked
description: "Environment variables that configure Helm: cache/config/data homes, driver, namespace, kube connection, registry, plugins and rate limits."
sources:
  - "https://helm.sh/docs/helm/helm/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Helm reads these environment variables (names as listed in the `helm` command reference):

- Paths: `HELM_CACHE_HOME`, `HELM_CONFIG_HOME`, `HELM_DATA_HOME`, `HELM_PLUGINS`, `HELM_REGISTRY_CONFIG`, `HELM_REPOSITORY_CACHE`, `HELM_REPOSITORY_CONFIG`.
- Behaviour: `HELM_DEBUG` (indicate debug mode), `HELM_DRIVER` (secret, configmap, memory, sql), `HELM_MAX_HISTORY`, `HELM_NO_PLUGINS` (disable plugins, `HELM_NO_PLUGINS=1`), `HELM_NAMESPACE`, `HELM_COLOR` and `NO_COLOR` for output colouring, `SOURCE_DATE_EPOCH` for reproducible package timestamps.
- Kubernetes connection: `KUBECONFIG`, `HELM_KUBEAPISERVER`, `HELM_KUBECAFILE`, `HELM_KUBECONTEXT`, `HELM_KUBEASGROUPS`, `HELM_KUBEASUSER`, `HELM_KUBETOKEN`, `HELM_KUBEINSECURE_SKIP_TLS_VERIFY`, `HELM_KUBETLS_SERVER_NAME`.
- Client throttling: `HELM_BURST_LIMIT` (default 100) and `HELM_QPS`.

Each corresponds to a global flag (for example `--debug`, `--namespace`, `--kube-context`, `--kubeconfig`, `--registry-config`, `--repository-cache`, `--repository-config`, `--burst-limit`, `--qps`).

Also listed: `HELM_DRIVER_SQL_CONNECTION_STRING` (connection string for the SQL storage driver). `HELM_COLOR` accepts never, always or auto (default never); `NO_COLOR` set to any non-empty value overrides it. `HELM_BURST_LIMIT` is for servers with many CRDs (default 100, -1 to disable). `helm env` is listed as the Helm client environment information command.

## Checked

2026-11-03. Confirmed against the `helm` command reference (https://helm.sh/docs/helm/helm/): the variable names, descriptions, defaults and the HELM_DRIVER values. Removed: the claim that a flag overrides its variable, the `HELM_DEBUG=true` equals `--debug` claim, the CI plugin-pinning and burst-limit advice, and the Windows paths pointer (none are on the page).
Method: documentation only; no commands were run.

