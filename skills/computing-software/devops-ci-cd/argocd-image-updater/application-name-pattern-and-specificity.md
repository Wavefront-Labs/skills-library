---
id: computing-software.devops-ci-cd.argocd-image-updater.application-name-pattern-and-specificity
name: application-name-pattern-and-specificity
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, application-selection, name-pattern, specificity, glob-pattern, multiple-crs, application-refs]
level: practitioner
status: docs-checked
description: "Select applications by namePattern globs, understand how the most specific rule wins, and avoid thrashing when two ImageUpdater CRs match the same application."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/applications.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Selecting applications by namePattern

`applicationRefs[].namePattern` is a glob matched against Application names in the CR's namespace:

```yaml
spec:
  applicationRefs:
    - namePattern: "frontend-*"
    - namePattern: "backend"       # exact match
```

When several rules could match the same Application, the most specific rule is used. Specificity scoring: exact matches rank highest (1,000,000+), then literal characters count (`app-prod-*` about 9, `app-*` about 4, `app-?` about 4, `app-[1234567]` about 4), and label selectors add significant bonus points.

Process per reconciliation:

1. list all Applications in the CR's namespace once
2. sort applicationRefs by specificity, most specific first
3. for each Application, take the first matching rule and stop

So `app-1` uses its exact rule, `app-prod-*` beats `app-*`.

Conflict warning: conflicts between different CRs are not handled. If CR-A has `namePattern: "app-1"` with `nginx:1.20` and CR-B has `app-*` with `nginx:1.21`, both manage `app-1` and it flips between versions every cycle. Ensure each Application is targeted by only one ImageUpdater CR, or make patterns non-overlapping.

An Application must be of type Helm, Kustomize or Plugin, live in the CR's namespace, and match at least one applicationRef.

## Checked

2026-11-04. Confirmed against the applications.md docs page (Name pattern matching, NamePattern Specificity Rules and example scores, Application Selection Process, Multiple ImageUpdater Resources Conflict warning, Application requirements).

Method: documentation only; no commands were run.
