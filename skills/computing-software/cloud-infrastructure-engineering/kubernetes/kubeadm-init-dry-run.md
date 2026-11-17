---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-init-dry-run
name: kubeadm-init-dry-run
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, kubeadm-dry-run, dry-run, static-pod-manifests, cluster-bootstrap]
level: practitioner
status: docs-checked
description: "Use kubeadm init, join and upgrade --dry-run to render certificates, kubeconfigs and static pod manifests for review before touching a node."
sources: ["https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/implementation-details/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/util/dryrun/dryrun.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeadm --dry-run

## Render without changing the node
```bash
sudo kubeadm init --config kubeadm.yaml --dry-run | tee init-dryrun.log
sudo kubeadm upgrade apply v1.31.4 --dry-run
sudo kubeadm join <endpoint>:6443 --token ... --discovery-token-ca-cert-hash sha256:... --dry-run
```
Dry run writes everything to a temporary directory, printed near the top of the output:
```
[dryrun] Wrote certificates, kubeconfig files and control plane manifests to the
"/etc/kubernetes/tmp/kubeadm-init-dryrun123456" directory
```
kubeadm also has `kubeadm upgrade diff`, which shows the differences that would be applied to the existing static pod manifests.

## What to review
```bash
D=/etc/kubernetes/tmp/kubeadm-init-dryrun123456
ls $D
grep -A40 'command:' $D/kube-apiserver.yaml        # flags from extraArgs land here
openssl x509 -in $D/apiserver.crt -noout -text        # check the Subject Alternative Name list
diff <(sudo cat /etc/kubernetes/manifests/kube-apiserver.yaml) $D/kube-apiserver.yaml   # upgrades
```
Check: apiserver SANs include the load-balancer name and IP, `--service-cluster-ip-range` and
pod CIDR match the network plan, image tags match the target version, extra volumes are mounted.

## Gotchas
- A dry run does not prove reachability of the control-plane endpoint or registry; run
  `kubeadm config images pull --config kubeadm.yaml` separately.
- Delete the temp directory afterwards: it holds the generated private keys and certificates.

## Verify
The rendered manifests contain every intended flag, and the SAN list is complete, before the
real `kubeadm init` runs.

## Checked

Date: 2026-10-26. Documentation release: Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm source (kubernetes/kubernetes master).

Confirmed: `--dry-run` exists on `kubeadm init`, `join` and `upgrade apply`/`upgrade node`; in dry-run mode certificates, kubeconfig files and static pod manifests are written to a temporary folder (kubeadm implementation details); the folder is created under `/etc/kubernetes/tmp` with the prefix `kubeadm-init-dryrun` and kubeadm prints `[dryrun] Wrote certificates, kubeconfig files and control plane manifests to the "<dir>" directory` (kubeadm source); `kubeadm upgrade diff` shows the differences that would be applied to static pod manifests; `kubeadm config images pull --config`. Removed as unconfirmed: the printed `Would perform action` line, the claim that preflight checks still run, `openssl -ext`, and the statement that the temporary directory holds a CA key (it holds the generated keys and certificates).

Method: documentation only; no commands were run.
