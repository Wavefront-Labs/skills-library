---
id: computing-software.devops-ci-cd.argocd-image-updater.application-label-selectors
name: application-label-selectors
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, label-selectors, application-selection, matchlabels, matchexpressions, application-refs, namepattern]
level: practitioner
status: docs-checked
description: "Select Argo CD applications by labels with labelSelectors matchLabels and matchExpressions, optionally combined with namePattern for precise targeting."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/applications.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Label selectors for application selection

Use `labelSelectors` in an applicationRef (standard Kubernetes label selector syntax):

```yaml
spec:
  applicationRefs:
    - namePattern: "*"
      labelSelectors:
        matchLabels:
          app.kubernetes.io/part-of: "my-project"
        matchExpressions:
          - key: "environment"
            operator: In
            values: [ "production", "staging" ]
      images:
        - alias: "app"
          imageName: "myregistry/myapp:stable"
```

`namePattern` is required, so use `"*"` to select on labels alone.

Combine both for precision:

```yaml
- namePattern: "web-*"
  labelSelectors:
    matchLabels:
      tier: "frontend"
```

Label selectors raise a rule's specificity, so a `app-*` rule with `matchLabels` (`environment: production`, `tier: frontend`) outranks a plain `app-*` rule.

Selection only applies to Applications in the CR's `metadata.namespace`. With `useAnnotations: true`, `namePattern: "*"` and no `labelSelectors`, the updater tries to process every Application in that namespace, which the docs say can cause performance issues, so they strongly recommend `labelSelectors` to limit scope.

Check what matched: `kubectl get imageupdater -n argocd` prints an `APPS` column; the status field `applicationsMatched` is the number of Applications matched by the CR's selectors.

## Checked

2026-11-04. Confirmed against the applications.md docs page (Label-based selection, Combining selection criteria, Label Selector Impact, performance warning for useAnnotations, Monitoring status). Reworded the annotation-mode sentence to match the page.

Method: documentation only; no commands were run.
