---
id: computing-software.devops-ci-cd.jenkins.folder-scoped-credentials
name: folder-scoped-credentials
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, credentials, folder-credentials, credential-scope, global-scope, system-scope, cloudbees-folder, folder-credentials-provider, multi-tenant-jenkins, credentials-useitem, authorize-project, least-privilege]
level: advanced
status: docs-checked
description: "Isolate team secrets in Jenkins with folder-scoped credentials: System vs Global scope, folder stores, lookup order, permissions, and authorize-project so jobs can't borrow others' secrets."
sources: ["https://github.com/jenkinsci/credentials-plugin/blob/master/docs/user.adoc", "https://github.com/jenkinsci/authorize-project-plugin", "https://www.jenkins.io/doc/book/pipeline/shared-libraries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Folder-scoped credentials

## Scopes
- **System**: usable for launching agents and some system-wide processes configured under
  Manage Jenkins; not available to jobs. Put agent SSH keys and cloud tokens here.
- **Global**: also available to all jobs running as an authentication that has
  `Credentials/UseItem`. The problem in a shared controller: any Jenkinsfile can bind the prod
  deploy key.
- **Folder store**: credentials defined on a folder (*Folder -> Credentials -> Folder*) are
  visible to the folder's children.

Credentials from parent contexts are available too, and a credential with the same ID in the
current context masks the parent's one (the credentials page greys out masked entries); useful for
per-team overrides, confusing otherwise.

## Multi-team layout
```
/team-payments   (folder creds: payments-prod-kubeconfig, payments-sonar-token)
/team-search     (folder creds: search-prod-kubeconfig)
global           (only truly shared: artifact-repo-readonly)
system           (agent keys, k8s cloud token)
```
The folder credentials store is exposed per folder (*Folder -> Credentials -> Folder*), supports credentials
domains and supports only global scope.
(In a folder store the only scope is global, which exposes the credential to children of the folder.)

## Folders alone are not enough
The Credentials plugin docs recommend putting sensitive credentials in a context that limits their
use (for example a "Deployment" folder with restricted access) and using the Authorize Project
plugin to control the effective permissions of running builds. Close the gap:
1. **Authorize Project** plugin (strategies: run as the user who triggered the build, as
   anonymous, as a specific user, or as SYSTEM; configured under *Manage Jenkins > Security >
   Access Control for Builds*). A job running as a specific user can use a credential only if that
   user has `Credentials/UseOwn` (normally implied by `Item/Build`) or `Credentials/UseItem`
   (normally implied by `Job/Configure`).
2. Authorization strategy: grant each team access to credentials only in its own folder.
3. Shared libraries defined on a folder are untrusted (they run in the Groovy sandbox); only
   global trusted libraries can bypass it.

## Gotchas
- Multibranch and organization folders are folders, so they can hold credentials too; keep
  team credentials on a parent plain folder you control.
- Moving a job to another folder changes which credentials are visible to it; re-test builds.

## Verify
From a job in `/team-search`, `withCredentials([string(credentialsId: 'payments-sonar-token', ...)])`
fails because the credential is not visible to that job; the same job in `/team-payments` succeeds.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the Credentials plugin user guide: System and Global scope behaviour, Folder Credentials Provider (global scope only, `Credentials/UseItem`, `Credentials/UseOwn`), parent-context masking by same ID, Authorize Project guidance; Authorize Project README (strategies and the Access Control for Builds page); Shared Libraries page (folder libraries are untrusted). Removed the Job DSL snippet, role-permission names and error-text examples that no documentation read confirmed.
Method: documentation only; no commands were run.
