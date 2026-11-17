---
id: computing-software.cloud-infrastructure-engineering.kubernetes.configmap-key-projection-and-defaultmode
name: configmap-key-projection-and-defaultmode
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, configmap, defaultmode, key-to-path, volume-mount, secrets]
level: practitioner
status: docs-checked
description: "Project selected ConfigMap or Secret keys to custom paths with items, set file modes with defaultMode and mode, and handle optional and missing keys."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#add-configmap-data-to-a-specific-path-in-the-volume", "https://kubernetes.io/docs/concepts/configuration/secret/#secret-files-permissions", "https://github.com/kubernetes/api/blob/master/core/v1/types.go", "https://kubernetes.io/docs/concepts/configuration/configmap/", "https://kubernetes.io/docs/concepts/configuration/secret/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key projection and file modes

## Select keys and paths
```yaml
volumes:
- name: config
  configMap:
    name: app-config
    items:
    - key: application.yaml
      path: app/application.yaml       # relative path, subdirs allowed
    - key: logback.xml
      path: logback.xml
- name: tls
  secret:
    secretName: web-tls
    defaultMode: 0400                  # octal in YAML; 256 in JSON
    items:
    - key: tls.key
      path: server.key
      mode: 0400
```
With `items`, ONLY the listed keys appear. A listed key that is missing from the ConfigMap makes the
volume setup error unless the volume source is marked `optional`.

## Modes
- `defaultMode` sets the mode bits of the created files (default 0644; directories are not affected). `mode` per item overrides it.
- Valid values are octal 0000-0777 or decimal 0-511; YAML accepts both, JSON manifests need decimal (`256`).
- These settings can conflict with options such as `fsGroup`, so the resulting mode bits can differ.

## Single files and live updates
A `subPath` mount of a ConfigMap does not receive updates. If you need live updates, mount the ConfigMap in a dedicated directory and point the application there.

## Optional
```yaml
configMap:
  name: feature-flags
  optional: true          # pod starts even if the ConfigMap does not exist
```

## Verify
```bash
kubectl exec <pod> -- ls -lL /etc/tls        # -L follows the ..data symlinks to show real modes
```

## Checked
Checked 2026-10-24 against the core/v1 API types (ConfigMapVolumeSource, SecretVolumeSource, KeyToPath: items, defaultMode default 0644, octal 0000-0777 or decimal 0-511, YAML versus JSON, per-item mode, fsGroup conflict, optional, missing-key error) and the ConfigMap, Secret and Configure a Pod to Use a ConfigMap pages (v1.37): subPath mounts receive no updates. Removed the Helm quoting, ownership and mount-hiding remarks.
Method: documentation only; no commands were run.
