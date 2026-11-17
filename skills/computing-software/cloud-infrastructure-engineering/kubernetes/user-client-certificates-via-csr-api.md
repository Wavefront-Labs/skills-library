---
id: computing-software.cloud-infrastructure-engineering.kubernetes.user-client-certificates-via-csr-api
name: user-client-certificates-via-csr-api
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, user-certificate, x509-client-cert, client-certificate-authentication, kubeconfig-generation, certificatesigningrequest, cka, authentication]
level: practitioner
status: docs-checked
description: "Issue a user X.509 client cert through the CertificateSigningRequest API (CN=user, O=groups), build a kubeconfig for it, and know why certs cannot be revoked."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/#normal-user", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/#x509-client-certificates", "https://kubernetes.io/docs/tasks/tls/certificate-issue-client-csr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User client certificates via the CSR API

## How X.509 auth maps identity
The apiserver (`--client-ca-file`) accepts any cert signed by that CA. **CN = username**,
each **O = a group** (repeat O for several groups). The `system:masters` group is bound to the
`cluster-admin` role by the default bindings — never issue it to people. The
`CertificateSubjectRestriction` admission plugin, enabled by default, blocks CSRs that request it.

## Issue a cert (CKA task)
```bash
openssl genrsa -out jane.key 2048
openssl req -new -key jane.key -out jane.csr -subj "/CN=jane/O=dev-team"
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata: {name: jane}
spec:
  request: $(base64 -w0 < jane.csr)
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400          # 1 day; honoured since 1.22
  usages: [client auth]
EOF
kubectl certificate approve jane
kubectl get csr jane -o jsonpath='{.status.certificate}' | base64 -d > jane.crt
openssl x509 -in jane.crt -noout -subject -enddate
```
`kubectl get csr` shows `Approved,Issued`. If it stays `Approved` without `Issued`, check the
kube-controller-manager logs: signing failures are reported only there, and the signer needs the
cluster CA key. Without `expirationSeconds` the lifetime is the controller-manager's
`--cluster-signing-duration` (default 1 year); with it the shorter of the two applies, and the minimum
accepted value is 600 seconds.

## Build the kubeconfig
```bash
kubectl config set-cluster prod --server=https://<api>:6443 \
  --certificate-authority=/etc/kubernetes/pki/ca.crt --embed-certs --kubeconfig=jane.kubeconfig
kubectl config set-credentials jane --client-certificate=jane.crt --client-key=jane.key \
  --embed-certs --kubeconfig=jane.kubeconfig
kubectl config set-context jane@prod --cluster=prod --user=jane --namespace=dev --kubeconfig=jane.kubeconfig
kubectl config use-context jane@prod --kubeconfig=jane.kubeconfig
kubectl create rolebinding jane-edit --clusterrole=edit --user=jane -n dev
kubectl auth can-i create deploy -n dev --as=jane --as-group=dev-team
```

## Gotchas
- **No revocation.** Kubernetes does not support certificate revocation; a leaked cert is valid until
  expiry unless you rotate the CA. Keep `expirationSeconds` short and prefer OIDC for humans.
- Removing RBAC bindings is the only quick mitigation — so bind to the user, and audit
  `O=` groups you hand out.
- Approving requires `approve` on the `signers` resource for that signerName; automate
  approval only with a strict controller that checks CN/O.
- CSRs are garbage-collected: approved, denied and failed ones after 1 hour, pending ones after 24
  hours, and all of them once the issued certificate has expired — fetch the cert promptly.

## Verify
- [ ] `kubectl --kubeconfig=jane.kubeconfig auth whoami` (1.28+) shows `jane` and groups.
- [ ] Cert expiry matches policy; user has no `system:masters` group.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37).
Confirmed: CN as username and O as group; `signerName: kubernetes.io/kube-apiserver-client` with `usages: [client auth]`;
`spec.expirationSeconds` since v1.22 with a 600 s minimum and the min-of-both rule with `--cluster-signing-duration`; approve via
`kubectl certificate approve` and the `approve` verb on `signers`; CSR garbage-collection intervals; no revocation support;
`CertificateSubjectRestriction` for `system:masters`; `kubectl auth whoami`. Wrong in the original: `O=system:masters` "bypasses RBAC
entirely" (docs only say it is bound to cluster-admin), and the cause given for an Approved-but-not-Issued CSR (flags unconfirmed,
replaced with the documented log location).
Method: documentation only; no commands were run.
