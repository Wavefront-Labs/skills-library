---
id: computing-software.cloud-infrastructure-engineering.kubernetes.expired-control-plane-certificates
name: expired-control-plane-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, control-plane-troubleshooting, x509-certificate-expired, kubeadm-certs-renew, check-expiration]
level: practitioner
status: docs-checked
description: "Recover a kubeadm cluster whose control-plane certificates expired: confirm with openssl, kubeadm certs renew all, restart static pods and refresh kubeconfigs."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/#kubelet-client-cert"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expired control-plane certificates

## Symptoms
- kubectl or components fail TLS or authentication because a client or serving certificate
  has expired; the `admin.conf` client certificate can expire too.
- Usually about one year after install or after the last control-plane upgrade (kubeadm leaf
  certificates default to 1 year and are renewed during control-plane upgrades).

## Confirm
```bash
sudo kubeadm certs check-expiration
sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -enddate
date -u                                       # rule out clock skew first
```

## Renew (on each control-plane node)
```bash
sudo cp -a /etc/kubernetes /root/kubernetes-backup-$(date +%F)
sudo kubeadm certs renew all
```
Renews leaf certificates and the client certificates embedded in admin.conf, super-admin.conf,
controller-manager.conf and scheduler.conf, using the existing CAs. It does not renew the CAs, and
the kubelet's own client certificate is handled by kubelet rotation.

## Restart static pods to load new certs
kubectl cannot restart static pods. For each of kube-apiserver, kube-controller-manager,
kube-scheduler and etcd in turn, move its manifest out of `/etc/kubernetes/manifests/`, wait
about 20 seconds (the kubelet `fileCheckFrequency`) until the pod stops, then move it back and
wait again.

## Refresh client kubeconfigs
```bash
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## Kubelets
If a node's `kubelet-client-current.pem` also expired (for example the node was off for a long
time) the kubelet cannot rotate by itself. The kubeadm troubleshooting guide's repair: back up and
delete `/etc/kubernetes/kubelet.conf` and `/var/lib/kubelet/pki/kubelet-client*` on that node;
on a control-plane node with `ca.key` run
`kubeadm kubeconfig user --org system:nodes --client-name system:node:$NODE > kubelet.conf`,
adjust the cluster name and server endpoint in it, copy it to `/etc/kubernetes/kubelet.conf`
on the node, restart the kubelet so `kubelet-client-current.pem` is recreated, then edit
`kubelet.conf` to reference that rotated file. Follow the guide for the exact steps.

## Prevent
Upgrade at least yearly (kubeadm renews during control-plane upgrades), or schedule
`kubeadm certs renew all` plus the restarts, and alert well before expiry.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: kubeadm-certs task page (check-expiration, renew all on every control-plane node, static-pod restart through manifest move with 20-second fileCheckFrequency, copying admin.conf), kubeadm certs reference (renew subcommands for admin.conf, super-admin.conf, controller-manager.conf, scheduler.conf) and the kubeadm troubleshooting page (kubelet client certificate repair with kubeadm kubeconfig user). Replaced unconfirmed error strings and the unconfirmed kubeadm join phase path.

Method: documentation only; no commands were run.
