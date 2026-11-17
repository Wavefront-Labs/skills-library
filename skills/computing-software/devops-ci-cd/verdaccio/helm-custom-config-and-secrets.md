---
id: computing-software.devops-ci-cd.verdaccio.helm-custom-config-and-secrets
name: helm-custom-config-and-secrets
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [configmap, secretenvvars, helm-values, existingconfigmap, ingress-body-size, uplink-secret]
level: advanced
status: docs-checked
description: "Supply your own config.yaml to the Verdaccio Helm chart via a ConfigMap, inject uplink tokens with secretEnvVars, and raise the NGINX ingress body-size limit."
sources:
  - https://verdaccio.org/docs/kubernetes/
  - https://verdaccio.org/docs/uplinks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Custom configuration with a ConfigMap:
```
wget https://raw.githubusercontent.com/verdaccio/verdaccio/master/packages/config/src/conf/docker.yaml -O config.yaml
kubectl create configmap verdaccio-config --from-file ./config.yaml
helm install npm --set existingConfigMap=verdaccio-config verdaccio/verdaccio
```
Keep storage on the persistent path in your file:
```yaml
storage: /verdaccio/storage/data
auth:
  htpasswd:
    file: /verdaccio/storage/htpasswd
```
Private upstream tokens (chart 4.8.0+) go in a Kubernetes Secret through `secretEnvVars`:
```yaml
# values.yaml
secretEnvVars:
  FOO_TOKEN: superSecretBarToken
```
or `--set secretEnvVars.FOO_TOKEN=...`; then reference it in the uplink as `auth: { type: bearer, token_env: FOO_TOKEN }`.

Large publishes: the standard Kubernetes NGINX ingress allows 1MB bodies; add the annotation `kubernetes.io/proxy-body-size: 20m` (as shown on the docs page) to the ingress.

Health probes hit `/-/ping`; set `server.hidePingLogs: true` (7.x) to keep logs quiet.

Verify: `<ingress-url>/-/ping` answers and a large publish no longer fails with 413.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Kubernetes, Uplinks and Configuration (hiding ping logs). Confirmed: the ConfigMap steps, the storage and htpasswd paths, secretEnvVars from chart 4.8.0, the uplink auth with token_env, the proxy-body-size annotation and server.hidePingLogs on 7.x. Removed or corrected: the curl wording in the verify line.

Method: documentation only; no commands were run.
