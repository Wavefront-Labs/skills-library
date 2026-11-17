---
id: computing-software.devops-ci-cd.argocd-image-updater.write-back-methods-overview
name: write-back-methods-overview
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, write-back, write-back-method, argocd-method, git-method, write-back-config, plugin-env]
level: intro
status: docs-checked
description: "Choose between the argocd and git write-back methods in an ImageUpdater CR, global or per application, and know argocd is pseudo-persistent."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/applications.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Write-back methods overview

Image Updater never edits your manifests. It re-configures the Application's sources and hands control to Argo CD. The way it records the new tag is the write-back method:

- `argocd` (default): modifies the Argo CD `Application` resource through the Kubernetes API, like `argocd app set --parameter ...`
- `git`: commits the new image information to the Application's Git repository

Set it in the CR at two levels; the application level wins:

```yaml
spec:
  writeBackConfig:
    method: "argocd"          # global
  applicationRefs:
    - namePattern: "web-*"
      writeBackConfig:
        method: "git"         # per application
```

The method is chosen per Application, not per image. Rule of thumb: if Applications themselves are managed in Git (app-of-apps), choose `git`.

The `argocd` method is pseudo-persistent: deleting and recreating the Application, or syncing a Git-stored Application manifest over it, discards the changes. It suits Applications created imperatively through the UI or CLI. For plugin applications using `manifestTargets.plugin` it sets env vars in `spec.source.plugin.env`.

Allowed values of `method`: `argocd`, `git`, or `git:<secret_ref>`. `gitConfig` can only be used with `git`.

## Checked

2026-11-08. Read in full: docs/configuration/applications.md and docs/configuration/images.md (appendix tables). Read the first 170 lines of docs/basics/update-methods.md plus its plugin passages; the rest covers Git write-back details this skill does not cite. Confirmed the two methods, the default, the two override levels, per-application scope, the app-of-apps rule of thumb, pseudo-persistence, the plugin env behaviour and the allowed method values. Nothing removed.

Method: documentation only; no commands were run.
