---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-backup-automation-to-object-storage
name: etcd-backup-automation-to-object-storage
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, etcd-backup, etcd-backup-automation, scheduled-etcd-snapshot, cronjob, systemd-timer, s3, object-storage, retention, etcdctl, snapshot-save]
level: practitioner
status: docs-checked
description: "Automate etcdctl snapshot save on a schedule (CronJob with hostNetwork+PKI mount, or a systemd timer), ship to S3/GCS with retention, and alert when a backup is missing."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://etcd.io/docs/v3.6/op-guide/recovery/", "https://etcd.io/docs/v3.6/tasks/operator/how-to-save-database/", "https://github.com/aws/aws-cli/blob/develop/awscli/customizations/s3/subcommands.py", "https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd backup automation to object storage

**Goal:** a snapshot every N hours, off the node, with retention, and an alert when it stops
happening. Manual `etcdctl snapshot save` is a DR plan only until the person who knew the
command leaves.

## Option A — Kubernetes CronJob on the control plane (stacked etcd)
```yaml
apiVersion: batch/v1
kind: CronJob
metadata: {name: etcd-backup, namespace: kube-system}
spec:
  schedule: "0 */6 * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        spec:
          hostNetwork: true
          nodeSelector: {node-role.kubernetes.io/control-plane: ""}
          tolerations: [{key: node-role.kubernetes.io/control-plane, operator: Exists, effect: NoSchedule}]
          restartPolicy: Never
          containers:
          - name: backup
            image: <registry>/etcd-backup:<tag>     # your image: etcdctl and etcdutl matching the cluster's etcd version, plus the upload CLI
            command: ["/bin/sh", "-c"]
            args:
              - |
                set -e
                TS=$(date -u +%Y%m%dT%H%M%SZ)
                etcdctl --endpoints=https://127.0.0.1:2379 \
                  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
                  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
                  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key \
                  snapshot save /backup/etcd-$TS.db
                etcdutl snapshot status /backup/etcd-$TS.db -w table
                aws s3 cp /backup/etcd-$TS.db s3://<bucket>/etcd/$(hostname)/etcd-$TS.db --sse aws:kms
                rm -f /backup/etcd-$TS.db
            env: [{name: ETCDCTL_API, value: "3"}]
            volumeMounts:
              - {name: pki, mountPath: /etc/kubernetes/pki/etcd, readOnly: true}
              - {name: backup, mountPath: /backup}
          volumes:
            - {name: pki, hostPath: {path: /etc/kubernetes/pki/etcd, type: Directory}}
            - {name: backup, emptyDir: {}}
```
Match the etcd image tag to the running etcd (`kubectl -n kube-system get pod etcd-<node> -o jsonpath='{.spec.containers[0].image}'`)
so `etcdctl`/`etcdutl` versions line up. Cloud credentials: IRSA/Workload Identity on the
ServiceAccount; never a static key in the pod.

## Option B — systemd timer on each control-plane/etcd host (works when the API server is down)
```ini
# /etc/systemd/system/etcd-backup.service
[Service]
Type=oneshot
ExecStart=/usr/local/bin/etcd-backup.sh
# /etc/systemd/system/etcd-backup.timer
[Timer]
OnCalendar=*-*-* 00/6:00:00
Persistent=true
[Install]
WantedBy=timers.target
```
`systemctl enable --now etcd-backup.timer`. The script is the same etcdctl + upload. Prefer this
for external etcd and for the "cluster is already broken" case — a CronJob cannot run when the
scheduler is gone.

## Retention and layout
- Bucket lifecycle rule: choose a daily, weekly and monthly retention that matches your recovery needs (for example 7 daily, 4 weekly, 3 monthly).
- Per-host prefix so you can tell which member the snapshot came from; any member's snapshot is
  a full copy — one host per schedule is enough, but take from two hosts on alternating hours
  to survive a single-host failure.
- Enable the object store's versioning and immutability (object lock or retention) feature if ransomware is in the threat model.
- Encrypt: snapshots contain every Secret in cleartext unless encryption-at-rest is on.

## Alerting
Backups fail silently. Push a heartbeat (`curl https://<healthcheck>/ping/<id>`) at the end
of the script, or alert in Prometheus on
`time() - kube_cronjob_status_last_successful_time{cronjob="etcd-backup"} > 8*3600`.

## Gotchas
- `--endpoints=https://127.0.0.1:2379` + `hostNetwork: true` is required; the etcd client port
  is not exposed as a Service.
- The certificate, key and CA paths come from the etcd pod description (Kubernetes docs); a kubeadm
  control plane keeps them under `/etc/kubernetes/pki/etcd`. Use a client certificate the etcd CA trusts.
- Snapshot size ≈ DB size (grows with the keyspace) — `emptyDir` on a root disk that is nearly
  full is a classic failure; set `sizeLimit` or use a hostPath scratch dir.

## Verify
- [ ] `kubectl -n kube-system get jobs | grep etcd-backup` shows recent Complete jobs; bucket shows new objects at the schedule cadence.
- [ ] `etcdutl snapshot status <downloaded.db>` reports a sane revision/total keys and the hash matches.
- [ ] A quarterly restore drill into a scratch cluster succeeds (see etcd-snapshot-verification-and-restore-drills).

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master).

Confirmed: `etcdctl snapshot save` plus `etcdutl snapshot status -w table`; kubeadm certificate paths and the `node-role.kubernetes.io/control-plane` label and taint key (kubeadm source constants); the AWS CLI `s3 cp` options `--sse aws:kms` (valid values AES256 and aws:kms); systemd calendar repeat syntax. Removed as unconfirmed: the claim that the healthcheck-client certificate is the least-privileged certificate that can snapshot, the NOSPACE-alarm snapshot behaviour, and object-lock mode names. Retention counts and the alert threshold are suggestions, not documented defaults.

Method: documentation only; no commands were run.
