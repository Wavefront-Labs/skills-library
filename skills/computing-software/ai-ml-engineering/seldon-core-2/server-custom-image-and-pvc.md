---
id: computing-software.ai-ml-engineering.seldon-core-2.server-custom-image-and-pvc
name: server-custom-image-and-pvc
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, server, custom-server, pvc, persistent-volume, extracapabilities, mlserver]
level: practitioner
status: docs-checked
description: "Run a Server with a custom MLServer image or a PersistentVolumeClaim mounted into rclone, and target it from a Model via spec.server or an extra capability."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/server.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom image and PVC Servers

## Custom image
Reuse an existing ServerConfig and override the container image. Add an extra capability so models can ask for this version.

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Server
metadata:
  name: mlserver-134
spec:
  serverConfig: mlserver
  extraCapabilities:
  - mlserver-1.3.4
  podSpec:
    containers:
    - image: seldonio/mlserver:1.3.4
      name: mlserver
```

Target it by name from a Model:

```yaml
apiVersion: mlops.seldon.io/v1alpha1
kind: Model
metadata:
  name: iris
spec:
  storageUri: "gs://seldon-models/mlserver/iris"
  server: mlserver-134
```

## Server with a PVC
Add a volume and mount it into the `rclone` container so models load from the persistent volume.

```yaml
spec:
  serverConfig: mlserver
  extraCapabilities:
  - "pvc"
  podSpec:
    volumes:
    - name: models-pvc
      persistentVolumeClaim:
        claimName: ml-models-pvc
    containers:
    - name: rclone
      volumeMounts:
      - name: models-pvc
        mountPath: /var/models
```

The model then uses a path under the mount and requires the extra capability:

```yaml
spec:
  storageUri: "/var/models/iris"
  requirements:
  - sklearn
  - pvc
```

For many servers or standard definitions, create your own ServerConfig instead.

## Checked

Confirmed against the Server resource page (Custom Servers and Server with PVC sections): the mlserver-134 custom image manifest, targeting it with spec.server, the rclone volume mount PVC manifest with the pvc capability and requirement, and the ServerConfig alternative.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb kubernetes/resources/server.md page (raw markdown).
