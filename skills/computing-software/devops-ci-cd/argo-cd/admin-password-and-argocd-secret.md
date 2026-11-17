---
id: computing-software.devops-ci-cd.argo-cd.admin-password-and-argocd-secret
name: admin-password-and-argocd-secret
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, admin-password, admin-password-reset, argocd-secret, disable-admin-user, server-secretkey]
level: practitioner
status: docs-checked
description: "Manage the Argo CD admin account and argocd-secret: initial password, resetting a lost password with a bcrypt hash, disabling admin after SSO, and webhook secret keys."
sources: ["https://argo-cd.readthedocs.io/en/stable/getting_started/", "https://argo-cd.readthedocs.io/en/stable/faq/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/webhook/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admin password and argocd-secret

## 1. Initial password
```bash
argocd admin initial-password -n argocd          # reads argocd-initial-admin-secret
argocd login argocd.example.com --username admin
argocd account update-password
kubectl -n argocd delete secret argocd-initial-admin-secret    # it is only for bootstrap
```

## 2. Reset a lost password
```bash
HASH=$(argocd account bcrypt --password 'N3w-Strong-Pass!')
kubectl -n argocd patch secret argocd-secret -p "{\"stringData\": {
  \"admin.password\": \"$HASH\",
  \"admin.passwordMtime\": \"$(date -u +%FT%TZ)\" }}"
```
Alternative from the FAQ: delete both `admin.password` and `admin.passwordMtime` and restart
argocd-server; a new password is generated as per the getting started guide.

## 3. Disable admin once SSO works
```yaml
# argocd-cm
data:
  admin.enabled: "false"
```
Keep a break-glass path, for example a local account with a password in your vault.

## 4. What else lives in argocd-secret
- `webhook.github.secret`, `webhook.gitlab.secret`, `webhook.bitbucket.uuid` (and `webhook.bitbucketserver.secret`) — webhook validation.
- Dex client secrets can be referenced from argocd-cm with `$dex.oidc.clientSecret`-style references.

## Verify
- [ ] Admin login fails after disabling; SSO login works; `argocd-initial-admin-secret` no longer exists.

## Checked
2026-10-31. Confirmed on the getting-started guide (`argocd admin initial-password -n argocd`, `argocd-initial-admin-secret`, delete after changing), the FAQ (`argocd account bcrypt`, `admin.password`, `admin.passwordMtime`, delete-both-keys alternative), user management (`admin.enabled: "false"` in argocd-cm, `$dex.oidc.clientSecret`) and the webhook page (secret key names). Removed unconfirmed claims: session invalidation by `passwordMtime`, `server.secretkey` behaviour and rotation, merge-versus-replace advice for argocd-secret, and the cluster-admin break-glass note.
Method: documentation only; no commands were run.
