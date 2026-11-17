---
id: computing-software.ai-ml-engineering.kserve.kserve-storage-git
name: kserve-storage-git
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [git, git-username, git-password, https-only, secretkeyref]
level: practitioner
status: docs-checked
description: "Pull a model from a Git repository over HTTPS: URL form, GIT_USERNAME in env or URL (URL wins), GIT_PASSWORD from a Secret via env, and the no-branches limit."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/storage/providers/git.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Git model storage

Git download supports the `https` protocol only and does not support selecting branches. Set `storageUri` to the repository URL, for example `https://github.com/kserve/kserve.git`.

Credentials:
- Username via the `GIT_USERNAME` env var or in the URL (`https://username@github.com/kserve/kserve.git`). If both are present the URL username takes precedence.
- Password only via the `GIT_PASSWORD` env var. A password embedded in the URL is ignored.

Keep the password in a Secret and reference it from the model container env:

```bash
kubectl create secret generic git-secret --from-literal=GIT_PASSWORD='<password>'
```

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
spec:
  predictor:
    model:
      env:
        - name: GIT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: git-secret
              key: GIT_PASSWORD
              optional: false
```

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited KServe Git storage page in full; every claim matches it. No content removed.
