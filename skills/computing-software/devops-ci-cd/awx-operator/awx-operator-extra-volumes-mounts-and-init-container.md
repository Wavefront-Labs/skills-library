---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-extra-volumes-mounts-and-init-container
name: awx-operator-extra-volumes-mounts-and-init-container
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, extra-volumes, volume-mounts, init-container, ansible-cfg, configmap, pvc]
level: advanced
status: docs-checked
description: "Add volumes and mounts to the web, task, rsyslog, EE and init containers, such as an ansible.cfg ConfigMap or a shared PVC."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/custom-volume-and-volume-mount-options.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator extra volumes mounts and init container

Fields (default empty): `extra_volumes` (volumes for the application pod), `web_extra_volume_mounts`, `task_extra_volume_mounts`, `rsyslog_extra_volume_mounts`, `ee_extra_volume_mounts`, `init_container_extra_volume_mounts` and `init_container_extra_commands`.

`ee_extra_volume_mounts` and `extra_volumes` only affect the globally available Execution Environments; for custom EEs customize the pod spec in AWX. Volume and volume mount names cannot contain underscores.

```yaml
spec:
  extra_volumes: |
    - name: ansible-cfg
      configMap:
        defaultMode: 420
        items:
          - key: ansible.cfg
            path: ansible.cfg
        name: <resourcename>-extra-config
    - name: shared-volume
      persistentVolumeClaim:
        claimName: my-external-volume-claim
  init_container_extra_volume_mounts: |
    - name: shared-volume
      mountPath: /shared
  init_container_extra_commands: |
    chmod 775 /shared
    chgrp 1000 /shared
  ee_extra_volume_mounts: |
    - name: ansible-cfg
      mountPath: /etc/ansible/ansible.cfg
      subPath: ansible.cfg
```

The ConfigMap `<resourcename>-extra-config` holds an `ansible.cfg` (for example `remote_tmp = /tmp` and SSH args `-C -o ControlMaster=auto -o ControlPersist=60s`). The init commands give the awx user rwx on the shared volume.

Mounting rules recap: volumes are declared once in `extra_volumes` for the application pod, and each container then picks them up with its own `*_extra_volume_mounts` list.

## Checked

2026-11-09. Confirmed field names and defaults, the global execution environment warning, the underscore restriction, and the ConfigMap and spec examples against the AWX Operator custom volume page (read in full). Removed the unsupported subPath explanation.

Method: docs-checked 2026-11-09 against the AWX Operator docs page docs/user-guide/advanced-configuration/custom-volume-and-volume-mount-options.md
