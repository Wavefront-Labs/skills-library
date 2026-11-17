---
id: computing-software.cloud-infrastructure-engineering.kubernetes.anonymous-requests-and-system-groups
name: anonymous-requests-and-system-groups
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, authentication, anonymous-requests, system-anonymous, anonymous-auth, rbac]
level: practitioner
status: docs-checked
description: "Control anonymous API requests: what system:anonymous can reach by default, restricting anonymous auth to health endpoints, and auditing system groups."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/authentication/#anonymous-requests", "https://kubernetes.io/docs/reference/access-authn-authz/rbac/#discovery-roles", "https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anonymous requests and system groups

## How it works
Anonymous access is enabled by default when the authorization mode is not `AlwaysAllow`
(disable with `--anonymous-auth=false`). Requests that no authenticator accepts become user
`system:anonymous`, group `system:unauthenticated`. Authenticated users all get
`system:authenticated`. RBAC then decides.

Default bindings that touch these groups:
- `system:public-info-viewer` (ClusterRole) to `system:authenticated` and
  `system:unauthenticated`: `/healthz`, `/livez`, `/readyz`, `/version`, `/version/`.
- `system:discovery`, `system:basic-user` to `system:authenticated` only.
- kubeadm: `kubeadm:bootstrap-signer-clusterinfo` lets anonymous read `cluster-info` in
  `kube-public` (needed for `kubeadm join` discovery).

## Find dangerous bindings
```bash
kubectl get clusterrolebindings,rolebindings -A -o json | jq -r '.items[]
 | select(any(.subjects[]?; .name=="system:anonymous" or .name=="system:unauthenticated"))
 | "\(.kind) \(.metadata.namespace // "-") \(.metadata.name) -> \(.roleRef.name)"'
```
Anything beyond the defaults above is a finding.

## Restrict anonymous to health endpoints
Structured AuthenticationConfiguration (the `anonymous` field is gated by
`AnonymousAuthConfigurableEndpoints`: alpha 1.31, beta on by default 1.32, stable 1.34 and locked on):
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AuthenticationConfiguration
anonymous:
  enabled: true
  conditions:
  - path: /livez
  - path: /readyz
  - path: /healthz
```
Pass with `--authentication-config`; if the `anonymous` field is set in that file you cannot also
set `--anonymous-auth`. This keeps LB health checks working while every other endpoint is not
reachable anonymously, even if authorization would allow it.

`--anonymous-auth=false` alone breaks unauthenticated health probes and kubeadm join discovery.

## Kubelet
Separate setting: `authentication.anonymous.enabled: false` in KubeletConfiguration (or
`--anonymous-auth=false`). The kubelet's own default is anonymous enabled with authorization mode
`AlwaysAllow`; kubeadm defaults anonymous to false. Anonymous kubelet access with
`authorization.mode: AlwaysAllow` means remote exec.

## Verify
```bash
curl -k https://<api>:6443/api/v1/namespaces          # expect 401 or 403, never 200
curl -k https://<api>:6443/readyz                     # expect ok
kubectl auth can-i --list --as=system:anonymous
```

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes source.
Confirmed: anonymous default and `--anonymous-auth` interaction with `--authentication-config`; AuthenticationConfiguration
`apiserver.config.k8s.io/v1` anonymous conditions; feature gate stages; default ClusterRoles and bindings (policy.go);
`kubeadm:bootstrap-signer-clusterinfo` name (kubeadm source); kubelet anonymous defaults (kubelet authn doc, kubeadm componentconfig).
Method: documentation only; no commands were run.
