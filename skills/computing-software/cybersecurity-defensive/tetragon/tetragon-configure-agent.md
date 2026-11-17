---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-configure-agent
name: tetragon-configure-agent
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [agent-configuration]
level: practitioner
status: docs-checked
description: "Change Tetragon agent settings on Kubernetes, Docker or systemd, enable process credentials and run the operator as non-root."
sources:
  - "https://tetragon.io/docs/installation/configuration/"
  - "https://tetragon.io/docs/reference/daemon-configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure the Tetragon agent

Goal: change an agent setting for your deployment mode, then restart.

## Change a setting

- Kubernetes: `kubectl edit cm -n kube-system tetragon-config`, edit, save, then `kubectl rollout restart -n kube-system ds/tetragon`.
- Docker or systemd: each setting is a file under `/etc/tetragon/tetragon.conf.d/` whose name is the setting and whose content is the value. For example, export events to a file:

```shell
echo "/var/log/tetragon/tetragon.log" > /etc/tetragon/tetragon.conf.d/export-file
systemctl restart tetragon
```

For Docker, bind mount `/etc/tetragon`, `/sys/kernel` and `/var/log/tetragon`, and run `/usr/bin/tetragon` in the `quay.io/cilium/tetragon:<version>` image with `--pid=host --cgroupns=host --privileged`.

References: the Helm chart reference (Kubernetes), the daemon configuration reference (container or systemd), and the gRPC TLS page.

## Enable process credentials

Set `enable-process-cred` to `true` (default `false`) to get `process_credentials` in events:

```shell
echo "true" > /etc/tetragon/tetragon.conf.d/enable-process-cred
systemctl restart tetragon
```

On Kubernetes change `enable-process-cred` from "false" to "true" in the ConfigMap and restart the daemonset.

## Operator as non-root

Since 1.6.0 the operator runs non-root by default:

```yaml
tetragonOperator:
  containerSecurityContext:
    runAsUser: 65532
    runAsGroup: 65532
    runAsNonRoot: true
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - "ALL"
```

Override these values (for example `runAsUser: 1001`, plus `readOnlyRootFilesystem: true`) in a values file and install with `helm install tetragon cilium/tetragon --namespace kube-system --values custom-values.yaml`. Running as root (`runAsUser: 0`, `runAsNonRoot: false`) is not recommended. Check the result with:

```shell
kubectl get pod -n kube-system -l app.kubernetes.io/name=tetragon-operator -o jsonpath='{.items[0].spec.containers[0].securityContext}' | jq
```

## Flag defaults

Selected defaults from the daemon configuration reference (each setting is a drop-in file name): `bpf-lib: /var/lib/tetragon/`, `event-queue-size: 10000`, `export-file-max-backups: 5`, `export-file-max-size-mb: 10`, `export-rate-limit: -1`, `log-format: text`, `log-level: info`, `process-cache-size: 65536`, `procfs: /proc/`. `server-address` defaults to `localhost:54321` (an empty address disables the gRPC server). Drop-ins are recommended over editing `/etc/tetragon/tetragon.yaml`; deleting that file and all drop-ins restores defaults.

## Checked

Date: 2026-11-07

Configuration page read in full. The flag defaults are not on that page, so the daemon configuration reference was read in full and added to sources; the server-address default was corrected to localhost:54321.

Method: documentation only; no commands were run.
