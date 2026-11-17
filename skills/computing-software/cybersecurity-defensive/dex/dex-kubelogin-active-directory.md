---
id: computing-software.cybersecurity-defensive.dex.dex-kubelogin-active-directory
name: dex-kubelogin-active-directory
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [kubelogin, kubectl, active-directory, ldap]
level: practitioner
status: docs-checked
description: "Log in to Kubernetes with kubelogin through Dex and Active Directory: kubeconfig exec credentials and required API server flags."
sources:
  - https://dexidp.io/docs/guides/kubelogin-activedirectory/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
kubelogin is a helper that makes kubectl log in to an OpenID provider. The docs integrate it with Dex backed by Active Directory (or an AD compatible LDAP such as Samba AD). Ensure TLS is enabled on the directory.

Sample config: `examples/config-ad-kubelogin.yaml` has an `ldap` connector; change `host`, `bindDN` and `bindPW`. Run Dex with:

```bash
bin/dex serve examples/config-ad-kubelogin.yaml
```

Copy the CA to the master node as `/etc/ssl/certs/openid-ca.pem` and point the API servers at Dex:

```
--oidc-issuer-url=https://dex.example.com:32000/dex
--oidc-client-id=kubernetes
--oidc-ca-file=/etc/ssl/certs/openid-ca.pem
--oidc-username-claim=email
--oidc-groups-claim=groups
```

Add a kubeconfig user:

```bash
kubectl config set-credentials oidc   --exec-api-version=client.authentication.k8s.io/v1beta1   --exec-command=kubectl   --exec-arg=oidc-login   --exec-arg=get-token   --exec-arg=--oidc-issuer-url=https://dex.example.com:32000/dex   --exec-arg=--oidc-client-id=kubernetes   --exec-arg=--oidc-extra-scope=groups   --exec-arg=--certificate-authority-data=$(base64 -w 0 openid-ca.pem)
```

Also pass `--oidc-client-secret` with the secret from the Dex config, and extra scopes `profile` and `email`.

Run `kubectl --user=oidc cluster-info`; a browser opens at `http://localhost:8000` for the AD login. Restart the API servers after changing flags.

To make Dex authentication the default, switch the context with `kubectl config set-context --current --user=oidc`.

## Checked
2026-11-09: read the Dex kubelogin and Active Directory guide in full; the sample config name, connector fields, API server flags, kubeconfig exec arguments, `http://localhost:8000` login and context switch all match.
Method: documentation only; no commands were run.
