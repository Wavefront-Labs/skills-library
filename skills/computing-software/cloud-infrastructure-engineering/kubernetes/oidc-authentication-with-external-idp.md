---
id: computing-software.cloud-infrastructure-engineering.kubernetes.oidc-authentication-with-external-idp
name: oidc-authentication-with-external-idp
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, authentication, oidc, oidc-issuer, dex, keycloak, kubelogin, sso]
level: advanced
status: docs-checked
description: "Wire kube-apiserver to an OIDC IdP (Keycloak, Entra ID, Okta, or Dex in front of LDAP/GitHub) and give users kubelogin-based kubeconfigs with group-based RBAC."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/authentication/#openid-connect-tokens", "https://github.com/int128/kubelogin", "https://dexidp.io/docs/connectors/github/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC authentication with an external IdP

## Apiserver side (flags; or AuthenticationConfiguration, see sibling skill)
```yaml
# kubeadm ClusterConfiguration apiServer.extraArgs
- {name: oidc-issuer-url, value: "https://keycloak.example.com/realms/k8s"}
- {name: oidc-client-id, value: kubernetes}
- {name: oidc-username-claim, value: email}
- {name: oidc-username-prefix, value: "oidc:"}
- {name: oidc-groups-claim, value: groups}
- {name: oidc-groups-prefix, value: "oidc:"}
# - {name: oidc-ca-file, value: /etc/kubernetes/pki/oidc-ca.crt}  # private CA issuer
```
- The issuer URL must use `https://` and must match the token's `iss` claim.
- The apiserver must reach `<issuer>/.well-known/openid-configuration` and JWKS.
- Prefixes stop an IdP user named `system:admin` from colliding with built-in identities.

## IdP side
- Create a public client (`kubernetes`) with redirect URIs `http://localhost:8000` and
  `http://localhost:18000` (kubelogin uses 18000 when port 8000 is busy); kubelogin uses PKCE
  automatically when the provider supports it.
- Add a **groups** claim to the ID token (see your IdP's documentation for the mapper or claim
  setting, and check whether it carries group names or IDs).
- **Dex** when the source is LDAP/GitHub/SAML: Dex is the OIDC issuer; connectors map
  upstream groups (GitHub `org:team`).

## User kubeconfig (kubelogin)
```bash
kubectl krew install oidc-login
kubectl oidc-login setup --oidc-issuer-url=https://keycloak.example.com/realms/k8s --oidc-client-id=kubernetes
```
```yaml
users:
- name: oidc
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1
      command: kubectl
      args: [oidc-login, get-token, --oidc-issuer-url=https://keycloak.example.com/realms/k8s,
             --oidc-client-id=kubernetes, --oidc-extra-scope=groups, --oidc-extra-scope=email]
      interactiveMode: IfAvailable
```
Kubelogin caches the ID and refresh tokens on disk; run `kubectl oidc-login clean` to force a re-login after group changes.

## RBAC
`kubectl create clusterrolebinding platform-admins --clusterrole=cluster-admin --group=oidc:platform-admins`

## Debugging
```bash
kubectl auth whoami                       # username + groups as the apiserver sees them
kubectl oidc-login setup --oidc-issuer-url=<issuer> --oidc-client-id=<id>   # dumps the ID token claims
```
For `Unauthorized` errors read the kube-apiserver logs and check that the token's `iss` matches
the configured issuer and `aud` matches the client ID.

## Gotchas
- Kubelogin stores an ID token and a refresh token. Group changes only appear after the next
  ID token is issued.
- Managed control planes (EKS, GKE, AKS) have provider-specific identity integrations; check the
  provider documentation before setting apiserver flags.
- Keep a non-OIDC break-glass admin credential offline in case the IdP is down.

## Verify
- [ ] `kubectl auth whoami` shows `oidc:` username and expected groups.
- [ ] A user removed from the IdP group loses access after token expiry.

## Checked

Checked 2026-10-27 against Kubernetes website content (main, v1.38 dev tree) and the v1.37 line (latest release at review time), the kubelogin README and usage docs, and the Dex GitHub connector page.

- `--oidc-*` flag names, prefixes (`oidc:` examples), https-only issuer, `--oidc-ca-file`, and `kubectl auth whoami` confirmed in the authentication page.
- Kubelogin redirect ports 8000 and 18000, automatic PKCE, `--oidc-extra-scope`, `setup` and `clean` subcommands confirmed in the kubelogin docs; exec credential `client.authentication.k8s.io/v1` shown in both docs.
- Dex GitHub group claims formatted as `(org):(team)` confirmed.
- Removed unconfirmed claims: token lifetimes, Keycloak and Entra mapper details, EKS CLI command, literal error strings.

Method: documentation only; no commands were run.
