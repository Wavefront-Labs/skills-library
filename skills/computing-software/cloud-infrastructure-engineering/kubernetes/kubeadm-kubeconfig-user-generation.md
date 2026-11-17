---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-kubeconfig-user-generation
name: kubeadm-kubeconfig-user-generation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, kubeadm-kubeconfig-user, kubeconfig-generation, certificates]
level: practitioner
status: docs-checked
description: "Generate per-user or break-glass kubeconfigs with kubeadm kubeconfig user, choose org/group mapping and validity, and avoid sharing admin.conf."
sources: ["https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-kubeconfig/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeadm kubeconfig user

On a control-plane node (needs the CA key at `/etc/kubernetes/pki/ca.key`):
```bash
cat > cc.yaml <<'EOF'
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
clusterName: prod
controlPlaneEndpoint: k8s-api.example.internal:6443
certificatesDir: /etc/kubernetes/pki
EOF
sudo kubeadm kubeconfig user --config cc.yaml --client-name alice --org dev-team \
  --validity-period 720h > alice.kubeconfig
```
- `--client-name` becomes the certificate CN (the Kubernetes username).
- `--org` (repeatable) becomes O fields, i.e. groups. Bind RBAC to the group, not the user.
- `--validity-period` sets the certificate lifetime (default `8760h0m0s`, one year).
- `--token` produces a token-based kubeconfig instead of a client cert.

## Why this matters
Kubernetes does not support certificate revocation (authentication docs): a leaked cert is valid until
it expires. So:
- Keep user certs short (hours to days) or prefer OIDC for humans.
- Never hand out `admin.conf` or `super-admin.conf` (kubeadm docs). `admin.conf` is in the
  `kubeadm:cluster-admins` group (bound to cluster-admin); `super-admin.conf` is in `system:masters`,
  a break-glass group that bypasses authorization (RBAC) entirely. Keep `super-admin.conf` somewhere safe.
- Never use `--org system:masters` for anything except break-glass.

## Bind permissions
```bash
kubectl create rolebinding dev-edit --clusterrole=edit --group=dev-team -n dev
```

## Verify
```bash
KUBECONFIG=alice.kubeconfig kubectl auth whoami
KUBECONFIG=alice.kubeconfig kubectl auth can-i create deployments -n dev
openssl x509 -noout -subject -enddate <<<"$(kubectl config view --raw --kubeconfig alice.kubeconfig \
  -o jsonpath='{.users[0].user.client-certificate-data}' | base64 -d)"
```

## Checked

Date: 2026-10-26. Documentation release: Kubernetes website docs (kubernetes/website main, 2026-10-26).

Fixed: `--validity-period` defaults to 8760h (one year) per the flag reference, not "the cluster's cert validity". Confirmed: `kubeadm kubeconfig user` flags `--client-name`, `--config`, `--org` (list), `--token`, `--validity-period`, output to stdout; the example ClusterConfiguration fields `clusterName`, `controlPlaneEndpoint`, `certificatesDir` and that the cluster CA key is loaded from that directory; `super-admin.conf` is signed with `O = system:masters` (bypasses authorization) and `admin.conf` with `O = kubeadm:cluster-admins` bound to the cluster-admin ClusterRole; docs say to avoid sharing either file; Kubernetes does not support certificate revocation; `kubectl auth whoami` (SelfSubjectReview, stable in 1.28). Removed as unconfirmed: the "since 1.29" version gate and the offline-storage instruction beyond keeping the file safe.

Method: documentation only; no commands were run.
