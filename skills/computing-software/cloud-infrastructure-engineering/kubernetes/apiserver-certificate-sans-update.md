---
id: computing-software.cloud-infrastructure-engineering.kubernetes.apiserver-certificate-sans-update
name: apiserver-certificate-sans-update
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, control-plane-ha, apiserver-cert-sans, controlplaneendpoint-change, certificates, kubeadm]
level: practitioner
status: docs-checked
description: "Add SANs to the kube-apiserver serving cert on a live kubeadm cluster without downtime, node by node, using the kubeadm-config ConfigMap and kubeadm init phase certs."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-reconfigure/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/reference/using-api/health-checks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Updating apiserver certificate SANs

Symptom that sends you here: an `x509: certificate is valid for ..., not <new-name>` error when
reaching the API through a new DNS name or load balancer address.

The kubeadm "Reconfiguring a kubeadm cluster" page says that `*SANs` options in `ClusterConfiguration`
require writing new certificates with the updated Subject Alternative Names, and that you should back up
`/etc/kubernetes/` first.

## 1. Update the stored ClusterConfiguration
```bash
kubectl edit cm -n kube-system kubeadm-config
# the configuration is under data.ClusterConfiguration; add under apiServer:
#   certSANs: [k8s-api.example.com, 10.0.0.100]
```
kubeadm keeps its `ClusterConfiguration` in the `kubeadm-config` ConfigMap in `kube-system`, and the page
notes that no validation is done on edits (it is stored as a YAML string), and that changes must then be
reflected on node components manually. Joins and upgrades read this ConfigMap, so editing only a file on
disk would be undone later.

## 2. Regenerate the serving cert on each control-plane node
Write the new certificate with `kubeadm init phase certs apiserver --config <config-file>`, where the
config file's contents must match the updated `ClusterConfiguration`. kubeadm does not overwrite a
certificate and key pair that already exists (per the kubeadm certificates page), so move the old
`apiserver.crt` and `apiserver.key` out of `/etc/kubernetes/pki/` first (keep them as a backup):
```bash
kubectl get cm -n kube-system kubeadm-config -o jsonpath='{.data.ClusterConfiguration}' > cc.yaml
sudo mkdir -p /root/pki-backup
sudo mv /etc/kubernetes/pki/apiserver.crt /etc/kubernetes/pki/apiserver.key /root/pki-backup/
sudo kubeadm init phase certs apiserver --config cc.yaml
```
Then make sure the running apiserver serves the new certificate (see Verify). For kubeadm static pods,
the kubelet restarts the pod when its manifest in `/etc/kubernetes/manifests` is updated, which
`kubeadm init phase control-plane apiserver --config cc.yaml` does; if the manifest is unchanged,
restart the apiserver static pod another way, such as temporarily moving its manifest out of the
directory and back. The reconfigure page advises making these changes one node at a time to avoid
downtime.

## 3. Changing controlPlaneEndpoint itself
Changing `controlPlaneEndpoint` is not covered by the kubeadm reconfiguration documentation, which
documents SAN changes, component flags and the kubelet and kube-proxy configuration ConfigMaps. Treat
an endpoint change as a separate procedure to plan and rehearse on a spare cluster. A safe preparation
that is covered above: add the new name as a SAN first so both names work while you migrate clients.

## Verify
```bash
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text     # check the "Subject Alternative Name" block
curl --cacert /etc/kubernetes/pki/ca.crt https://k8s-api.example.com:6443/readyz
```
`/readyz` is one of the API server's health endpoints (`healthz` is deprecated since v1.16).

## Checked
Checked 2026-10-24 against the kubernetes/website kubeadm "Reconfiguring a kubeadm cluster" page
(`kubeadm-config` ConfigMap and `data.ClusterConfiguration`, `*SANs` need new certificates,
`kubeadm init phase certs` and `kubeadm init phase control-plane` with `--config`, back up
`/etc/kubernetes/`, one node at a time, static pod restart on manifest change), the kubeadm
certificates page (existing cert and key pairs are not overwritten) and the API server health checks
page (`readyz`; `healthz` deprecated since v1.16). Removed: the step-by-step endpoint migration
(kubeconfig, `cluster-info`, kube-proxy edits) and `crictl` commands, which no checked documentation covers.
Method: documentation only; no commands were run.
