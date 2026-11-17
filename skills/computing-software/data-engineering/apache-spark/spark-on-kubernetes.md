---
id: computing-software.data-engineering.apache-spark.spark-on-kubernetes
name: spark-on-kubernetes
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-on-kubernetes, kubernetes, spark-operator, sparkapplication, pod-templates, eks, gke, emr-on-eks, cluster-manager]
level: advanced
status: docs-checked
description: "Run Spark on Kubernetes: native spark-submit to k8s://, service accounts/RBAC, images, pod templates, shuffle without external service, and the Kubeflow Spark operator."
sources:
  - https://spark.apache.org/docs/latest/running-on-kubernetes.html
  - https://github.com/kubeflow/spark-operator
  - https://spark.apache.org/docs/latest/configuration.html#dynamic-allocation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark on Kubernetes

**Goal:** run batch Spark jobs as pods with correct permissions, images, resources and shuffle behaviour, either with native spark-submit or the Spark operator.

## Prerequisites
```bash
kubectl create namespace spark-jobs
kubectl -n spark-jobs create serviceaccount spark
kubectl -n spark-jobs create rolebinding spark-edit --clusterrole=edit --serviceaccount=spark-jobs:spark
```
The driver pod always creates executor pods, so its service account needs a Role or ClusterRole that allows that in the namespace; the docs grant the built-in `edit` ClusterRole.

Image: build from the Spark distribution's `bin/docker-image-tool.sh` and add your code and dependencies; the image is set with `spark.kubernetes.container.image`, which is required.

## Native submit
```bash
spark-submit \
  --master k8s://https://<API_SERVER>:6443 --deploy-mode cluster \
  --name orders-daily \
  --conf spark.kubernetes.namespace=spark-jobs \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.kubernetes.container.image=<REGISTRY>/spark-app:1.4.2 \
  --conf spark.executor.instances=10 \
  --conf spark.executor.memory=8g \
  --conf spark.kubernetes.driver.podTemplateFile=driver.yaml \
  --conf spark.kubernetes.executor.podTemplateFile=executor.yaml \
  local:///opt/app/main.py
```
`local://` is a path inside the image. Pod templates (`spark.kubernetes.driver.podTemplateFile`, `spark.kubernetes.executor.podTemplateFile`) customise the pods Spark submits. The master URL must be `k8s://<host>:<port>` with the port always given.

## Spark operator (declarative)
```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata: {name: orders-daily, namespace: spark-jobs}
spec:
  type: Python
  mode: cluster
  image: <REGISTRY>/spark-app:1.4.2
  mainApplicationFile: local:///opt/app/main.py
  sparkVersion: "<SPARK_VERSION>"
  restartPolicy: {type: OnFailure, onFailureRetries: 2}
  driver: {cores: 1, memory: 4g, serviceAccount: spark}
  executor: {instances: 10, cores: 4, memory: 8g}
  dynamicAllocation: {enabled: true, minExecutors: 2, maxExecutors: 40}
```
The operator is the separate kubeflow/spark-operator project (CRDs `SparkApplication`, `ScheduledSparkApplication` and `SparkConnect` in group `sparkoperator.k8s.io`, version `v1beta2`); check its docs for the fields your operator release supports. `kubectl describe sparkapplication orders-daily` shows status and events.

## Shuffle and dynamic allocation
Dynamic allocation needs one of: the external shuffle service, `spark.dynamicAllocation.shuffleTracking.enabled=true`, or shuffle-block decommissioning (`spark.decommission.enabled=true` with `spark.storage.decommission.shuffleBlocks.enabled=true`).

## Gotchas
- `spark.kubernetes.memoryOverheadFactor` is 0.1 for JVM jobs and 0.40 for non-JVM jobs (for example PySpark), unless `spark.driver.memoryOverheadFactor` / `spark.executor.memoryOverheadFactor` is set; a pod killed for memory means raising the overhead.
- When the application completes, executor pods terminate and are cleaned up; the driver pod stays in `Completed` state (keeping its logs, using no resources) until garbage collected or deleted manually. `spark.kubernetes.executor.deleteOnTermination` defaults to true.
- To use a volume for shuffle and spill data, name it with the prefix `spark-local-dir-` (`spark.kubernetes.executor.volumes.*`); persistent volume claims suit large shuffles.
- Event logs need durable storage for a history server because pods are ephemeral.

## Verify
- [ ] The expected number of executor pods are Running (`kubectl -n spark-jobs get pods`).
- [ ] Driver pod ends `Completed`; no executor pods left behind.
- [ ] History server shows the run from the persisted event log.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in running-on-kubernetes.md: serviceAccountName property, rolebinding with the edit ClusterRole, container.image required, local:// scheme, k8s://host:port master with explicit port, pod template properties, memoryOverheadFactor 0.1 (JVM) / 0.40 (non-JVM) and its overrides, driver pod stays Completed while executors are cleaned up, deleteOnTermination true, spark-local-dir- volume prefix. Confirmed in kubeflow/spark-operator CRDs (last commit 2026-10-23): apiVersion v1beta2, SparkApplication/ScheduledSparkApplication/SparkConnect, fields onFailureRetries, dynamicAllocation min/maxExecutors, mainApplicationFile, sparkVersion, driver.serviceAccount. Removed unconfirmed ownerReference, default emptyDir and spark-role label claims, and the pinned 3.5.1 version.

Method: documentation only; no commands were run.
