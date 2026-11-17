---
id: computing-software.devops-ci-cd.argocd-image-updater.migration-v1-4-crd-upgrade-notes
name: migration-v1-4-crd-upgrade-notes
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, migration, crd-upgrade, common-update-settings, namespace-field-removal, inheritance, v1-4]
level: sme
status: docs-checked
description: "Handle upgrade traps: persisted updateStrategy and forceUpdate defaults that block inheritance before v1.4.0 CRDs, and the removed spec.namespace field that now fails validation."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CRD upgrade notes: v1.4.0 defaults and spec.namespace

Stored defaults. In v1.0.0 to v1.3.x the ImageUpdater CRD defaulted and stored `updateStrategy: semver` and `forceUpdate: false` whenever they were omitted from existing `commonUpdateSettings`. Stored values block inheritance from `spec.commonUpdateSettings` to `spec.applicationRefs[].commonUpdateSettings` and `.images[].commonUpdateSettings`, and from application-level to image-level settings.

Resources created with v1.4.0 CRDs or later can therefore behave differently from older ones. Upgrading the CRDs alone does not fix existing resources. After upgrading:

- manually remove unintended `forceUpdate` and `updateStrategy` values, or
- delete and recreate the affected `ImageUpdater` resources

Removed `spec.namespace`. The field no longer exists; a CR containing it fails validation at admission and cannot be created or updated. The controller only searches for Applications in the CR's own `metadata.namespace`.

```yaml
metadata:
  name: my-updater
  namespace: production   # same namespace as the Applications
spec:
  applicationRefs:
    - namePattern: "my-app"
```

Steps:

1. find `ImageUpdater` resources that include `spec.namespace`
2. delete the field from each
3. verify Applications are found and updated

If you relied on a different namespace in `spec.namespace`, you must place the CR in that namespace instead.

The images configuration page's field appendix still lists `namespace` as deprecated and ignored, which contradicts this overview page; treat the overview page as current and do not set the field.

## Checked

2026-11-04. Confirmed against the docs index page (v1.4.0 CRD warning, spec.namespace removal, impact, examples, migration steps); noted the conflicting wording in images.md.

Method: documentation only; no commands were run.
