---
id: computing-software.cloud-infrastructure-engineering.kubernetes.encryption-config-automatic-reload
name: encryption-config-automatic-reload
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, secrets-encryption-at-rest, encryption-config-reload, kube-apiserver, key-rotation, health-checks]
level: practitioner
status: docs-checked
description: "Enable --encryption-provider-config-automatic-reload so key rotation needs no apiserver restart, and monitor reload metrics and KMS health endpoints."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/#configure-automatic-reloading", "https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic encryption config reload

```
--encryption-provider-config=/etc/kubernetes/enc/enc.yaml
--encryption-provider-config-automatic-reload=true
```
With automatic reload on, the apiserver re-reads the file when it changes (changes are polled every
minute) and applies the new keys without a restart.

## Rotation with reload on
1. Add the new key as the second entry (readable but not yet used) on every control-plane node.
   Wait for each apiserver to reload.
2. Move the new key to first position on every node; wait for reload.
3. Rewrite Secrets: `kubectl get secrets -A -o json | kubectl replace -f -`.
4. Remove the old key; wait for reload.
Each step must reach all apiservers before the next; otherwise one apiserver writes with a key
another cannot read.

## Monitoring
```promql
increase(apiserver_encryption_config_controller_automatic_reloads_total{status="failure"}[1h]) > 0
apiserver_encryption_config_controller_automatic_reload_last_timestamp_seconds
apiserver_encryption_config_controller_last_config_info
```
`automatic_reloads_total` and the timestamp gauge carry labels `status` (`success` or `failure`) and
`apiserver_id_hash`; `last_config_info` carries the applied config `hash` per apiserver, so you can
compare hashes across control-plane nodes. All three are alpha-stability metrics.

## Health checks change
With automatic reload, there is a single KMS health check endpoint, `/healthz/kms-providers`, in
every configuration (KMS v1, v2, both, or none). Without automatic reload and with KMS v1 the health
checks are per plugin (`/healthz/kms-provider-0`, `/healthz/kms-provider-1`, ...). Update
load-balancer or monitoring probes that used the per-provider paths.

## Verify
Edit the file to add a harmless second key; the reload metric increments and no apiserver
restarts (`crictl ps` container age unchanged).

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes source.
Confirmed: `--encryption-provider-config-automatic-reload=true` flag; one-minute polling; metric names, labels and alpha
stability level (encryptionconfig metrics.go); health check table in the KMS provider doc; rotation order (add second, make
first, replace Secrets, then remove old key). Wrong in the original: "Older releases expose success/failures_total" metric names
and the `/livez` `/readyz` aggregation claim (removed, unconfirmed). Removed the unconfirmed "invalid config keeps previous" claim.
Method: documentation only; no commands were run.
