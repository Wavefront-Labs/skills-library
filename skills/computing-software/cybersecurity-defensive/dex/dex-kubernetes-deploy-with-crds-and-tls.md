---
id: computing-software.cybersecurity-defensive.dex.dex-kubernetes-deploy-with-crds-and-tls
name: dex-kubernetes-deploy-with-crds-and-tls
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [kubernetes, deployment, tls, secrets]
level: practitioner
status: docs-checked
description: "Deploy Dex on Kubernetes using CRD storage: generate TLS assets, mount the CA for the API server, create secrets and apply dex.yaml."
sources:
  - https://dexidp.io/docs/guides/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Dex repo contains scripts to run Dex on a Kubernetes cluster with GitHub authentication, exposed as a NodePort on 32000. Because Dex uses CRDs for state, no external database is needed.

Steps:

1. Generate TLS assets from `examples/k8s`:

```bash
cd examples/k8s
./gencert.sh
```

This creates files under `ssl`, mainly `cert.pem`, `key.pem` and `ca.pem`, for `dex.example.com` unless you edit the script.

2. Make the CA readable by the API server. If it runs as a container, a `hostPath` volume mounting the cert directory is the easiest way. The docs rename `ca.pem` to `openid-ca.pem` to keep it apart from other CAs. Configure the API server flags as in the OIDC flags skill.

3. Create secrets:

```bash
kubectl -n dex create secret tls dex.example.com.tls --cert=ssl/cert.pem --key=ssl/key.pem
kubectl -n dex create secret generic github-client   --from-literal=client-id=$GITHUB_CLIENT_ID   --from-literal=client-secret=$GITHUB_CLIENT_SECRET
```

4. Deploy the deployment, configmap and NodePort service, which also creates the RBAC bindings Dex needs to manage CRDs:

```bash
kubectl create -f dex.yaml
```

Test with `example-app --issuer https://dex.example.com:32000 --issuer-root-ca examples/k8s/ssl/ca.pem`.

## Checked
2026-11-09: read the Dex Kubernetes Authentication guide in full; NodePort 32000, CRD storage, `gencert.sh` outputs, hostPath CA mount, secrets, `dex.yaml` and example-app command all match.
Method: documentation only; no commands were run.
