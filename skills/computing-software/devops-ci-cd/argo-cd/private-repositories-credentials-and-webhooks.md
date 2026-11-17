---
id: computing-software.devops-ci-cd.argo-cd.private-repositories-credentials-and-webhooks
name: private-repositories-credentials-and-webhooks
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, repo-credentials, private-repos, credential-templates, repo-creds, repository-secret, ssh-known-hosts, argocd-ssh-known-hosts-cm, tls-certs, argocd-tls-certs-cm, github-app-credentials, deploy-key, oci-helm-repo, helm-repo-credentials, git-credentials-rotation, argocd-webhook, github-webhook, gitlab-webhook, webhook-secret, api-webhook, gpg-signature-verification, project-source-repos, repo-connection-failed, gitops, kubernetes]
level: practitioner
status: docs-checked
description: "Connect Argo CD to private Git/Helm/OCI sources: repository and repo-creds Secrets (SSH, HTTPS, GitHub App), known_hosts and custom CAs, and webhooks that end polling."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/", "https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/webhook/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private repositories, credentials and webhooks

**Goal:** every source Argo CD reads is declared as a Secret you can rotate from a vault,
hosts are verified, and a push shows up in Argo quickly instead of waiting for the three-minute poll.

## 1. Repository vs credential-template Secrets
```yaml
# one repo, SSH deploy key
apiVersion: v1
kind: Secret
metadata:
  name: repo-apps
  namespace: argocd
  labels: { argocd.argoproj.io/secret-type: repository }
stringData:
  type: git
  url: git@github.com:example/k8s-apps.git
  sshPrivateKey: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    …
---
# credential template: applies to every repo URL with this prefix (no need for one Secret per repo)
apiVersion: v1
kind: Secret
metadata:
  name: creds-github-org
  namespace: argocd
  labels: { argocd.argoproj.io/secret-type: repo-creds }
stringData:
  type: git
  url: https://github.com/example
  githubAppID: "123456"
  githubAppInstallationID: "7891011"
  githubAppPrivateKey: |
    -----BEGIN RSA PRIVATE KEY-----
    …
```
Matching: a credential template URL must be a prefix of the repo URL; the longest (best)
match wins, and a repository with its own credentials does not use a template. HTTPS access token: any non-empty
username plus the token as password (some services want your account name; Bitbucket needs `x-token-auth`).
GitHub App credentials (`githubAppID`, `githubAppInstallationID`, `githubAppPrivateKey`,
`githubAppEnterpriseBaseUrl` for GitHub Enterprise) avoid personal tokens. Azure workload identity uses
`useAzureWorkloadIdentity: "true"`; Google Cloud Source uses `gcpServiceAccountKey`.

Helm/OCI:
```yaml
stringData:
  type: helm
  url: https://charts.example.com          # or oci://ghcr.io/example/charts with enableOCI: "true"
  name: example-charts
  username: …
  password: …
  enableOCI: "true"
```

Manage with ESO (`ExternalSecret` → this Secret shape) or SOPS; the Secrets are plain
Kubernetes objects. CLI equivalents:
`argocd repo add … --ssh-private-key-path`, `argocd repo add … --github-app-id … --github-app-installation-id … --github-app-private-key-path …`.

## 2. Host keys and TLS
- SSH: the `ssh_known_hosts` entry of `argocd-ssh-known-hosts-cm` holds host keys (the docs example covers
  bitbucket.org, github.com, gitlab.com, ssh.dev.azure.com and vs-ssh.visualstudio.com). For self-hosted Git add the
  host with `ssh-keyscan server.example.com | argocd cert add-ssh --batch` (hostnames must not be hashed).
  `--insecure-skip-server-verification` skips host key checks: non-production only.
- HTTPS with a private CA: `argocd cert add-tls git.example.com --from ca.pem` (recommended for production;
  `--upsert` replaces; stored in `argocd-tls-certs-cm`). The same flag on `repo add` skips certificate
  verification: non-production only.
- Proxy: `proxy` and `noProxy` fields on the repository Secret; otherwise the repo-server's standard proxy
  environment variables apply.

## 3. Webhooks (stop polling)
Argo CD polls Git/OCI/Helm repositories every three minutes. Point the Git provider's webhook at
`https://argocd.example.com/api/webhook` (GitHub content type must be `application/json`).
Supported: GitHub, GitLab, Bitbucket, Bitbucket Server, Azure DevOps, Gogs. The shared secret is optional but
recommended if Argo CD is public; set `webhook.maxPayloadSizeMB` in `argocd-cm` to cap payloads (default 50MB):
```yaml
# argocd-secret
stringData:
  webhook.github.secret: <random>
  webhook.gitlab.secret: <random>
  webhook.bitbucket.uuid: <uuid>
  webhook.bitbucketserver.secret: <random>
  webhook.gogs.secret: <random>
  webhook.azuredevops.username: <user>     # basic auth
  webhook.azuredevops.password: <pass>
```
Webhook payloads are untrusted and only trigger a refresh of related apps. The handler does not tell branch
events from tag events of the same name. Bitbucket Cloud does not send changed files, so the Manifest Paths
annotation needs the `webhook.bitbucket.uuid` callback mechanism. OCI registry webhooks (GHCR package events)
use the same `webhook.github.secret`. ApplicationSets use a separate webhook configuration.

## 4. Project source allowlists
`AppProject.spec.sourceRepos` lists the repositories apps in the project may pull manifests from; keep push
access to those repos limited to admins.

## Checked
2026-10-31. Confirmed against the Argo CD Declarative Setup, Private Repositories and Webhook Configuration pages: Secret labels and fields, GitHub App fields, longest-prefix matching, known-hosts and TLS ConfigMaps, `cert add-tls`/`add-ssh`, proxy fields, webhook secret keys, three-minute poll, payload cap. Removed: GPG verification section (page not readable), version gates, `x-access-token`/`oauth2`/Azure username advice, `insecure` and `enableLfs` Secret keys, error-message table, log lines, ingress and reconciliation tuning, ApplicationSet port.
Method: documentation only; no commands were run.

## Verify
- [ ] `argocd repo list` shows a successful connection for every source; `argocd repocreds list` covers all org prefixes.
- [ ] Pushing to a repo refreshes the app without waiting for the poll.
- [ ] Deleting the credential Secret breaks fetch (proves it was the one in use), restoring from ESO fixes it.
