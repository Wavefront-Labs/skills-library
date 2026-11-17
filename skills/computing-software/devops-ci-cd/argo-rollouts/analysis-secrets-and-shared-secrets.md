---
id: computing-software.devops-ci-cd.argo-rollouts.analysis-secrets-and-shared-secrets
name: analysis-secrets-and-shared-secrets
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [secretkeyref, sharedsecret, analysis-shared-secret-namespace, secrets, rbac, analysisrun, argo-rollouts]
level: sme
status: docs-checked
description: "Pass credentials to metric providers through secretKeyRef args and know that an AnalysisRun reads only its own namespace."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
AnalysisTemplates and AnalysisRuns can reference Secrets in `.spec.args` to pass credentials such as API tokens to metric providers. An AnalysisRun can only read secrets from its own namespace; AnalysisTemplates themselves do not resolve secrets.

```yaml
spec:
  args:
    - name: api-token
      valueFrom:
        secretKeyRef:
          name: token-secret
          key: apiToken
```

The secret value is then used as `{{ args.api-token }}`, for example in a web metric `Authorization` header. Because an AnalysisRun can only reference secrets in its own namespace, create the Secret in the namespace where the rollout runs.

Verify with a test run and `kubectl describe analysisrun`.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/analysis/.

Removed or corrected: the whole shared-secret section (--analysis-shared-secret-namespace, --analysis-shared-secret-mode, LabelFilter, AllSecrets, the danger warning and the ServiceAccount note), none of which is on the page.

Method: documentation only; no commands were run.
