---
id: computing-software.cloud-infrastructure-engineering.google-cloud.apigee-hybrid-install-and-overrides
name: apigee-hybrid-install-and-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, apigee, apigee-hybrid-install, apigee-hybrid-overrides, kubernetes, helm-charts, api-management]
level: practitioner
status: docs-checked
description: "Install Apigee hybrid runtime on Kubernetes with Helm: overrides.yaml properties, chart install order, service account paths, ingress virtual hosts and dry runs."
sources: ["https://cloud.google.com/apigee/docs/hybrid/latest/install-before-begin", "https://cloud.google.com/apigee/docs/hybrid/latest/install-helm-charts", "https://cloud.google.com/apigee/docs/hybrid/latest/config-prop-ref"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Apigee hybrid: install and overrides

Apigee hybrid keeps the management plane in Google Cloud and runs the runtime plane on your own
Kubernetes cluster. The organization is hybrid-enabled and provisioned for you during the hybrid
installation; follow the install-before-begin page for the project, API and org steps for your version.

## overrides.yaml (excerpt)
Property names below are from the configuration property reference.
```yaml
instanceID: "<INSTANCE_ID>"          # unique per installation, letters and digits, up to 63 characters
namespace: apigee                    # default
gcp: {projectID: <P>, region: <REGION>, workloadIdentity: {enabled: true}}
k8sCluster: {name: <CLUSTER>, region: <REGION>}
org: <ORG_NAME>
envs:
- name: <ENV_NAME>
  serviceAccountPaths: {synchronizer: ..., runtime: ...}
cassandra: {hostNetwork: false, replicaCount: 3, storage: {storageSize: 100Gi}}
ingressGateways:
- name: ingress-1
  replicaCountMin: 2
  replicaCountMax: 10
virtualhosts:
- name: <ENV_GROUP>
  selector: {app: apigee-ingressgateway}
  sslCertPath: ./certs/<CERT>.pem
  sslKeyPath: ./certs/<KEY>.key
```
- `cassandra.replicaCount` defaults to 1, acceptable only for demo or test.
- `cassandra.storage.capacity` is deprecated from v1.12; use `storage.storageSize`.
- `cassandra.hostNetwork` (default false) is used in multi-region installs.
- `gcp.workloadIdentity.enabled` (default false, since 1.10) uses Workload Identity Federation for GKE.
- `virtualhosts[]`: either `sslCertPath` and `sslKeyPath` or `sslSecret` is required.
- `ingressGateways[].replicaCountMin` defaults to 2 and `replicaCountMax` to 10.

## Helm install order
Charts: `apigee-operator`, `apigee-datastore`, `apigee-telemetry`, `apigee-redis`,
`apigee-ingress-manager`, `apigee-org`, then per environment `apigee-env`, then per environment
group `apigee-virtualhost`. Each uses the same shape; run a server-side dry run first
(`--dry-run=server`) and the operator step needs elevated cluster permissions:
```bash
helm upgrade operator apigee-operator/ --install --namespace <APIGEE_NAMESPACE> --atomic -f overrides.yaml --dry-run=server
helm upgrade operator apigee-operator/ --install --namespace <APIGEE_NAMESPACE> --atomic -f overrides.yaml
```

## Verify
- [ ] A deployed proxy responds through the ingress hostname; all Apigee pods are Running.

## Checked
Date: 2026-10-31. Confirmed in the Apigee hybrid install-helm-charts and config-prop-ref pages: chart names
and order, `helm upgrade ... --install --atomic -f overrides.yaml`, `--dry-run=server`, elevated-permission
note, and each property, default and deprecation listed above. Removed unconfirmed claims: control-plane
`curl` call and org fields, supported Kubernetes platforms, cert-manager and node-label prerequisites,
`setSyncAuthorization`, upgrade and backup advice, Spot and egress gotchas, and custom resource names.
Method: documentation only; no commands were run.
