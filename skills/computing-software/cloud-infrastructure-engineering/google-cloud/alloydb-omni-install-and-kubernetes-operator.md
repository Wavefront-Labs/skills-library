---
id: computing-software.cloud-infrastructure-engineering.google-cloud.alloydb-omni-install-and-kubernetes-operator
name: alloydb-omni-install-and-kubernetes-operator
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, alloydb, alloydb-omni-install, alloydb-omni-kubernetes-operator, alloydb-omni, postgresql, hybrid-cloud]
level: practitioner
status: gated
description: "Run AlloyDB Omni outside Google Cloud: container install on a Linux host, the Kubernetes operator with DBCluster resources, HA and backups, and the columnar engine settings."
sources: ["https://cloud.google.com/alloydb/omni/docs/overview", "https://cloud.google.com/alloydb/omni/docs/quickstart", "https://cloud.google.com/alloydb/omni/docs/deploy-kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AlloyDB Omni: install and Kubernetes operator

AlloyDB Omni is the AlloyDB PostgreSQL engine (columnar engine, adaptive autovacuum, AI features)
packaged to run anywhere: on-prem, other clouds, laptops. Licensed per vCPU (developer edition free).

## Single host (container)
```bash
docker run -d --name alloydb-omni \
  -e POSTGRES_PASSWORD='<PW>' -p 5432:5432 \
  -v /data/alloydb:/var/lib/postgresql/data \
  google/alloydbomni:<VERSION>
psql -h 127.0.0.1 -U postgres -c "SELECT version();"
```
Host prep: Linux with cgroup v2, sufficient shared memory, disable transparent huge pages per docs for best performance.

## Kubernetes operator
```bash
helm install alloydbomni-operator oci://europe-docker.pkg.dev/alloydb-omni/charts/alloydbomni-operator \
  --version <OPERATOR_VERSION> --create-namespace --namespace alloydb-omni-system --atomic
```
(cert-manager is a prerequisite.)
```yaml
apiVersion: v1
kind: Secret
metadata: {name: db-pw-orders}
type: Opaque
data: {orders: <BASE64_PW>}
---
apiVersion: alloydbomni.dbadmin.goog/v1
kind: DBCluster
metadata: {name: orders}
spec:
  databaseVersion: "16.3.0"
  primarySpec:
    adminUser: {passwordRef: {name: db-pw-orders}}
    resources:
      cpu: 4
      memory: 16Gi
      disks:
      - {name: DataDisk, size: 100Gi, storageClass: premium-rwo}
  availability:
    numberOfStandbys: 1
```
Operator also provides `BackupPlan`/`Backup`/`Restore` CRDs (pgBackRest to GCS/S3/local),
`Switchover`/failover, and read pools (`DBInstance` (gated: unconfirmed, source is paywalled or blocked)).

## Columnar engine
```sql
ALTER SYSTEM SET google_columnar_engine.enabled = on;  -- restart
SELECT google_columnar_engine_add('sales');            -- or rely on auto-columnarization
```
Size memory with `google_columnar_engine.memory_size_in_mb`.

## Gotchas
- Not managed: you own upgrades, OS patching, monitoring (Prometheus exporter available) and backups.
- Versions: match operator and database versions per release notes.

## Verify
- [ ] `kubectl get dbclusters` shows `DBClusterReady` (gated: unconfirmed, source is paywalled or blocked); failover test promotes the standby.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: nothing removed. Gated: the DBInstance kind and DBClusterReady condition names were not found in the fetched pages (DBCluster was confirmed).

Method: documentation only; no commands were run.
