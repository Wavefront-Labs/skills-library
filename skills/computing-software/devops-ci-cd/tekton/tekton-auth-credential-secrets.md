---
id: computing-software.devops-ci-cd.tekton.tekton-auth-credential-secrets
name: tekton-auth-credential-secrets
category: computing-software
field: devops-ci-cd
product: tekton
tags: [authentication, secrets, serviceaccount, git, docker]
level: practitioner
status: docs-checked
description: "Give Tekton runs Git and Docker credentials through annotated Kubernetes Secrets attached to a ServiceAccount, and how credential selection by annotation works."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tekton supports these first-class Secret types: for Git `kubernetes.io/basic-auth` and `kubernetes.io/ssh-auth`; for Docker `kubernetes.io/basic-auth`, `kubernetes.io/dockercfg` and `kubernetes.io/dockerconfigjson`. A run gets access via its `ServiceAccount`. Each Secret needs a Tekton annotation, and Tekton ignores any Secret that is not annotated.

Annotation keys start with `tekton.dev/git-` or `tekton.dev/docker-` and the value is the host URL the credential is for:

```yaml
apiVersion: v1
kind: Secret
metadata:
  annotations:
    tekton.dev/git-0: https://github.com
    tekton.dev/git-1: https://gitlab.com
    tekton.dev/docker-0: https://gcr.io
type: kubernetes.io/basic-auth
stringData:
  username: <cleartext username>
  password: <cleartext password>
```

Credential initialization runs in every pod before any step: Tekton aggregates the associated Secrets into `/tekton/creds`, then copies or symlinks files into the user's `$HOME`, producing `~/.gitconfig` or `~/.ssh` for Git and `~/.docker/config.json` for Docker. For SSH, supplying a known-hosts value is encouraged; omitting it means the server public key is blindly accepted.

## Checked

Checked 2026-11-08 against docs/auth.md in tektoncd/pipeline (main), read in full. Confirmed the supported Secret types, the annotation requirement and key prefixes, the example, /tekton/creds aggregation, the generated files and the known_hosts guidance. No changes needed to claims.

Method: documentation only; no commands were run.
