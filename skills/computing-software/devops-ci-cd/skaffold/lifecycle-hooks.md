---
id: computing-software.devops-ci-cd.skaffold.lifecycle-hooks
name: lifecycle-hooks
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [hooks, before, after, build, sync, deploy]
level: advanced
status: docs-checked
description: "Run commands before or after build, sync and deploy on the host or in containers, with the environment variables provided."
sources:
  - "https://skaffold.dev/docs/lifecycle-hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Skaffold has three phases: `build`, `sync` and `deploy`. A hook can run `before` or `after` each phase. Hooks are either `host` hooks (run on the runner) or `container` hooks (run in a target container).

Where each hook is configured and what it can do:

- Build (host only): `hooks` on the artifact, with `before` and `after` lists whose entries are written directly as `command` and optional `os` (no `host:` wrapper).
- Sync (host or container): `sync.hooks` on the artifact, entries wrapped as `host:` or `container:`.
- Deploy (host or container): `hooks` under the deployer (the page shows `deploy.kubectl.hooks`), entries wrapped as `host:` or `container:`.

```yaml
build:
  artifacts:
  - image: hooks-example
    hooks:
      before:
      - command: ["sh", "-c", "./hook.sh"]
        os: [darwin, linux]
      - command: ["cmd.exe", "/C", "hook.bat"]
        os: [windows]
    sync:
      auto: {}
      hooks:
        after:
        - container:
            command: ["sh", "-c", "echo after sync hook"]
deploy:
  kubectl:
    hooks:
      after:
      - host:
          command: ["sh", "-c", "echo post-deploy"]
      - container:
          command: ["sh", "-c", "echo post-deploy in container"]
          containerName: hooks-example*
          podName: hooks-example-deployment*
```

Build hooks run before and after each artifact is built. When the image comes from the Skaffold image cache, the build hooks do not run; use `--cache-artifacts=false` to force them.

Container hooks: for sync, the target is the container of the artifact image. For deploy, Skaffold cannot determine the target from the config, so `podName` and `containerName` are needed, and glob prefixes work (for deployments, stateful sets and so on). A `before` deploy container hook only runs when a matching container exists from a previous deploy iteration, as in `skaffold dev`. `after` deploy container hooks run only after the deployment status checks complete.

Host hook environment variables (availability in brackets): `SKAFFOLD_IMAGE` (build, sync), `SKAFFOLD_PUSH_IMAGE`, `SKAFFOLD_IMAGE_REPO`, `SKAFFOLD_IMAGE_TAG` and `SKAFFOLD_BUILD_CONTEXT` (build), `SKAFFOLD_FILES_ADDED_OR_MODIFIED` and `SKAFFOLD_FILES_DELETED` (sync, semi-colon delimited absolute paths), `SKAFFOLD_RUN_ID` (deploy), `SKAFFOLD_KUBE_CONTEXT` and `SKAFFOLD_NAMESPACES` (sync, deploy; namespaces are comma separated), and for all phases `SKAFFOLD_DEFAULT_REPO`, `SKAFFOLD_RPC_PORT`, `SKAFFOLD_HTTP_PORT`, `SKAFFOLD_MULTI_LEVEL_REPO`, `SKAFFOLD_WORK_DIR` plus the local environment.

## Checked

2026-11-04. Read the whole Skaffold Lifecycle Hooks page. Confirmed phases, host and container hook shapes, build cache behaviour, the variable table with availability, and the deploy container targeting rules. Removed: the claim that a failing hook stops its phase, the advice to keep hooks idempotent and to put heavy logic in custom actions, and the earlier claim that only sync and deploy hooks need `host:` (build hooks have no wrapper). Corrected the variable availability, which was missing for several entries.
Method: documentation only; no commands were run.
