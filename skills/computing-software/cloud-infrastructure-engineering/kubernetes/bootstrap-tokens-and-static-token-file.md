---
id: computing-software.cloud-infrastructure-engineering.kubernetes.bootstrap-tokens-and-static-token-file
name: bootstrap-tokens-and-static-token-file
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, authentication, bootstrap-token-auth, token-auth-file, kubeadm-token, tls-bootstrapping]
level: practitioner
status: docs-checked
description: "Create, scope, inspect and clean up bootstrap tokens for node joins, and know why the static --token-auth-file should not be used for people."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/bootstrap-tokens/", "https://kubernetes.io/docs/reference/access-authn-authz/authentication/#static-token-file", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-token/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bootstrap tokens and static token files

## Bootstrap tokens
Format `[a-z0-9]{6}.[a-z0-9]{16}` (`<id>.<secret>`), stored as Secret
`kube-system/bootstrap-token-<id>` of type `bootstrap.kubernetes.io/token`. Enabled by
`--enable-bootstrap-token-auth` on the apiserver; users authenticate as
`system:bootstrap:<id>` in group `system:bootstrappers`.

```bash
kubeadm token create --ttl 2h --description "join rack 4" --print-join-command
kubeadm token list
kubeadm token delete <id>
kubectl -n kube-system get secret bootstrap-token-<id> -o yaml
```
Secret fields: `token-id`, `token-secret`, optional `description`, optional `expiration` (absolute
RFC 3339 UTC time), `usage-bootstrap-authentication` and `usage-bootstrap-signing` (must be `"true"`
to enable), and `auth-extra-groups` (comma-separated, each must start with `system:bootstrappers:`,
for example `system:bootstrappers:kubeadm:default-node-token`).
The `tokencleaner` controller deletes expired tokens; the `bootstrapsigner` signs the
`cluster-info` ConfigMap so joiners can verify the CA with the token.

## Keep them tight
- Short TTL; never `--ttl 0` (no expiry) outside labs.
- RBAC for the bootstrap group should allow only what node bootstrapping needs (creating
  client CSRs and their approval); review the bindings your installer created.
- Join commands in Terraform state or CI logs are credentials; rotate after exposure.

## Static token file
```
--token-auth-file=/etc/kubernetes/tokens.csv
# token,user,uid,"group1,group2"
```
Tokens last indefinitely, and the token list cannot be changed without restarting the apiserver;
the file is plain text on disk. Use OIDC, a webhook token authenticator or ServiceAccount tokens
instead where prompt rotation matters. The CSV has at least three columns (token, user name, uid)
followed by optional group names; multiple groups must be double-quoted.

## Verify
`kubectl auth whoami --token <id>.<secret>` should report `system:bootstrap:<id>` while the token is
valid, and fail after expiry (expired tokens are rejected for authentication).

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubeadm source.
Confirmed: token regex and Secret name/type/namespace; `--enable-bootstrap-token-auth`; username and group; Secret keys and
`auth-extra-groups` prefix rule; `tokencleaner` and `bootstrapsigner` controllers and the `cluster-info` ConfigMap in `kube-public`;
`kubeadm token create` flags `--ttl`, `--description`, `--print-join-command` (and `--ttl 0` means never expires); static token
file flag and format and lifetime; `kubectl auth whoami` exists. Removed the unconfirmed "CIS benchmarks flag it" and kubeadm-RBAC remarks.
Method: documentation only; no commands were run.
