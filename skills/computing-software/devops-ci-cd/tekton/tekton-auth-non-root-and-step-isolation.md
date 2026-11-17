---
id: computing-software.devops-ci-cd.tekton.tekton-auth-non-root-and-step-isolation
name: tekton-auth-non-root-and-step-isolation
category: computing-software
field: devops-ci-cd
product: tekton
tags: [authentication, non-root, securitycontext, secrets]
level: advanced
status: docs-checked
description: "Handle Tekton credential secrets for non-root steps, restrict secret access to specific steps, and troubleshoot unsuccessful cred copy warnings."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Non-root runs (randomised UIDs, step or task `securityContext`) need care:
- Git `ssh-auth` needs the user to have a valid home directory in `/etc/passwd`; a UID without one fails authentication.
- SSH ignores `$HOME`, so move or symlink the Secret files from Tekton's home (`/tekton/home`) to the real home of the non-root user.

By default Tekton makes supported Secrets available to all steps of a Task. To limit a Secret to some steps, define a `Volume` from the Secret and `VolumeMount` it only in the steps that need it, instead of using the built-in mechanism.

The docs describe an "unsuccessful cred copy" warning, with causes such as steps with varying UIDs, a workspace or volume also mounted for the same credentials, a read-only `$HOME`, `$HOME` contents `chown`ed to another user, or a step named `image-digest-exporter`.

To turn the built-in handling off (it can be hard to debug, supports few credential types and breaks when steps with different UIDs share credentials), set `disable-creds-init` to `"true"` in the feature flags ConfigMap in the `tekton-pipelines` namespace (the auth page names it `feature-flag`; check the actual name in your install). Credentials must then be passed explicitly: workspaces, `envFrom` from a Secret, or a custom volume and volumeMount.

## Checked

Checked 2026-11-08 against docs/auth.md in tektoncd/pipeline (main), read in full. Confirmed the non-root considerations, step-limited Secret mounting, the unsuccessful cred copy causes, and the disable-creds-init procedure and effects. The page names the ConfigMap feature-flag, so the skill now says to check the actual name.

Method: documentation only; no commands were run.
