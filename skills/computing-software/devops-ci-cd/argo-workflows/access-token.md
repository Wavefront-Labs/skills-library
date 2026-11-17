---
id: computing-software.devops-ci-cd.argo-workflows.access-token
name: access-token
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [access-token, service-account-token, bearer-token, token-revocation, argo-token]
level: practitioner
status: docs-checked
description: "Create a minimal-permission role, service account and service-account-token secret for API or CLI automation, test it, use it from Docker and revoke it."
sources: ["https://argo-workflows.readthedocs.io/en/latest/access-token/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo access tokens
1. Create a minimal role, for example `kubectl create role jenkins --verb=list,update --resource=workflows.argoproj.io -n argo`.
2. Create a service account in the same namespace (`kubectl create sa jenkins -n argo`), one per client.
3. Bind: `kubectl create rolebinding jenkins --role=jenkins --serviceaccount=argo:jenkins -n argo`.
4. Create a Secret of `type: kubernetes.io/service-account-token` with the annotation `kubernetes.io/service-account.name: jenkins`, named like `jenkins.service-account-token`.
5. Wait a few seconds for Kubernetes to fill the token, then:

```bash
ARGO_TOKEN="Bearer $(kubectl get secret jenkins.service-account-token -n argo -o=jsonpath='{.data.token}' | base64 --decode)"
```

The value includes the word `Bearer`. Use it as the header: `curl https://localhost:2746/api/v1/workflows/argo -H "Authorization: $ARGO_TOKEN"` returns 200. Check that disallowed calls fail; the workflow-templates endpoint should give 403. For the CLI, set `ARGO_SERVER` and `ARGO_TOKEN`.

Docker: pass `ARGO_SERVER`, `ARGO_TOKEN`, `ARGO_HTTP=false`, `ARGO_HTTP1=true`, `KUBECONFIG=/dev/null` and `ARGO_NAMESPACE` to `quay.io/argoproj/argocli:latest template list -v -e -k`.

Revoke by deleting the secret; re-create it for a fresh token. One account per client means revoking does not disturb others.

## Checked
2026-11-03. Confirmed against the Argo Workflows Access Token page: role, service account, rolebinding and secret commands, token retrieval, the 200 and 403 test calls, the Docker environment variables and revocation by deleting the secret. Nothing removed.
Method: documentation only; no commands were run.
