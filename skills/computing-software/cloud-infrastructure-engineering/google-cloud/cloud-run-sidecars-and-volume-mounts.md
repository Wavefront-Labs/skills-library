---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-run-sidecars-and-volume-mounts
name: cloud-run-sidecars-and-volume-mounts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run, cloud-run-sidecars, multi-container, cloud-run-volume-mounts, gcs-fuse-volume, nfs, in-memory-volume, otel-collector]
level: advanced
status: docs-checked
description: "Run multi-container Cloud Run services (proxy, OpenTelemetry collector sidecars) with startup ordering and shared in-memory volumes, and mount Cloud Storage, NFS and secrets as volumes."
sources: ["https://docs.cloud.google.com/run/docs/deploying#sidecars", "https://docs.cloud.google.com/run/docs/configuring/services/cloud-storage-volume-mounts", "https://docs.cloud.google.com/run/docs/configuring/services/nfs-volume-mounts", "https://docs.cloud.google.com/run/docs/configuring/in-memory-volumes", "https://docs.cloud.google.com/run/docs/reference/yaml/v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Run sidecars and volume mounts

## 1. Multi-container service
One ingress container declares `ports` (there is no default port, and only one container can expose a port); sidecars cannot listen on the ingress port. A service can have up to 10 containers per instance including the ingress container.
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata: {name: api}
spec:
  template:
    spec:
      serviceAccountName: api-run@<P>.iam.gserviceaccount.com
      containers:
      - name: app
        image: <AR>/api@sha256:...
        ports: [{containerPort: 8080}]
        env: [{name: OTEL_EXPORTER_OTLP_ENDPOINT, value: http://localhost:4317}]
        volumeMounts: [{name: shared, mountPath: /shared}]
      - name: collector
        image: <OTEL_COLLECTOR_IMAGE>
        startupProbe: {tcpSocket: {port: 4317}}
        volumeMounts: [{name: shared, mountPath: /shared}]
      volumes:
      - name: shared
        emptyDir: {medium: Memory, sizeLimit: 128Mi}
```
```bash
gcloud run services replace api.yaml --region=<R>
```
Startup order is set with the `run.googleapis.com/container-dependencies` template annotation (see the YAML reference for its format) or the console's container start-up order setting; use health checks on the containers that others depend on. With request-based billing, sidecars get CPU only while a request is processed or the ingress container is starting, so give them a startup probe or use instance-based billing.

## 2. Volumes
```bash
# Cloud Storage (Cloud Storage FUSE)
gcloud run services update api --region=<R> \
  --add-volume=name=models,type=cloud-storage,bucket=<B>,readonly=true \
  --add-volume-mount=volume=models,mount-path=/models
# NFS: the service must be attached to the VPC network of the NFS server (Direct VPC preferred)
gcloud run services update api --region=<R> \
  --add-volume=name=share,type=nfs,location=<NFS_IP>:/<NFS_PATH> --add-volume-mount=volume=share,mount-path=/mnt/share
# in-memory
gcloud run services update api --region=<R> --add-volume=name=tmp,type=in-memory,size-limit=512Mi \
  --add-volume-mount=volume=tmp,mount-path=/scratch
```
Secrets as files: `--set-secrets=/secrets/api-key=api-key:latest`.

## Gotchas
- Cloud Storage FUSE is not fully POSIX-compliant and gives no file locking for concurrent writes to the same file (last write wins).
- In-memory volumes consume the memory configured for your containers; the size limit must be less than the total container memory, and omitting it defaults to half of the combined memory.
- Volume mounts require the second generation execution environment (selected automatically if you do not set one).
- The service identity needs `roles/storage.objectViewer` (read) or `roles/storage.objectUser` (write) on the mounted bucket.

## Verify
- [ ] `gcloud run services describe api --region=<R> --format=yaml(spec.template.spec)` shows both containers and volumes.
- [ ] `/models` lists the bucket objects inside the app container.

## Checked

2026-10-24, Cloud Run deploying (sidecars), Cloud Storage volume mount, NFS volume mount, in-memory volume and YAML reference pages on docs.cloud.google.com. Confirmed: one ingress container, 10-container limit, `--add-volume` and `--add-volume-mount` grammar for `cloud-storage`, `nfs` (`location=IP:PATH`) and `in-memory`, `emptyDir` with `medium: Memory`, IAM roles on the bucket, gen2 requirement, the `run.googleapis.com/container-dependencies` annotation name. Removed the unconfirmed annotation value, collector image path, sidecar-crash behaviour and billing-sum claims.

Method: documentation only; no commands were run.
