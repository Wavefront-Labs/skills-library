---
id: computing-software.devops-ci-cd.argocd-image-updater.cr-structure-aliases-and-hierarchy
name: cr-structure-aliases-and-hierarchy
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, imageupdater-cr, alias, image-name, common-update-settings, hierarchical-config, crd, application-refs]
level: intro
status: docs-checked
description: "Write an ImageUpdater CR: applicationRefs, images with alias and imageName, and commonUpdateSettings inherited global to application to image, with alias naming rules."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/applications.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ImageUpdater CR structure and hierarchy

```yaml
apiVersion: argocd-image-updater.argoproj.io/v1alpha1
kind: ImageUpdater
metadata:
  name: my-image-updater
  namespace: argocd
spec:
  applicationRefs:
    - namePattern: "my-app-*"
      images:
        - alias: "nginx"
          imageName: "nginx:1.20"
```

Each image needs `alias` (unique within the applicationRef; alphanumerical characters advised) and `imageName` (registry, repository and initial tag or constraint). A `/` in an alias is allowed but must be written `_` in annotation keys, so `argoproj/argocd` becomes `argoproj_argocd`.

Top-level `spec` fields: `applicationRefs` (required), `commonUpdateSettings`, `writeBackConfig`, `imagesVerification`. `commonUpdateSettings` holds `updateStrategy` (default `semver`), `forceUpdate` (`false`), `allowTags`, `ignoreTags`, `pullSecret`, `platforms`.

Hierarchy, highest precedence first: image (`applicationRefs[].images[]`), application (`applicationRefs[]`), global (`spec`). Example: global `semver`, image-level `newest-build` gives that image `newest-build`. Application and global levels also carry `writeBackConfig`; verification can be set at all three.

Applications must be of type Helm, Kustomize or Plugin and in the CR's `metadata.namespace`. Do not set `spec.namespace`: the docs disagree on its status (the overview page says it is removed and a CR containing it fails validation; the images appendix says it is deprecated and ignored). Either way the controller uses the CR's `metadata.namespace`.

Without a version constraint, `imageName: "nginx"` updates to the newest version, which may be a breaking major.

## Checked

2026-11-04. Confirmed against images.md (image specification format, alias rules, field tables, configuration hierarchy) and applications.md (hierarchical configuration, application requirements). The spec.namespace statement now notes that the overview page (removed, fails validation) and the images appendix (deprecated, ignored) disagree.

Method: documentation only; no commands were run.
