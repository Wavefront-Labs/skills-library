---
id: computing-software.devops-ci-cd.tilt.tilt-tutorial-live-update
name: tilt-tutorial-live-update
category: computing-software
field: devops-ci-cd
product: tilt
tags: [tutorial-live-update, tilt, live-update, docker-build]
level: practitioner
status: docs-checked
description: "Tutorial on how docker_build context, only and ignore decide what Tilt watches, then how live_update sync and run steps update a container in place."
sources:
  - "https://docs.tilt.dev/tutorial/4-code-update-repeat.html"
  - "https://docs.tilt.dev/tutorial/5-live-update.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tutorial: code update and Live Update

## What Tilt watches

```python
docker_build(
    'tilt-avatar-web',
    context='.',
    dockerfile='./deploy/web.dockerfile',
    only=['./web/'],
    ignore=['./web/dist/'],
    live_update=[...]
)
```

Paths are relative to the Tiltfile.

- `context`: Tilt watches this directory recursively.
- `dockerfile` (optional): defaults to `./Dockerfile`; a change to it rebuilds the image.
- `only` (optional): restricts the build context and file watching, so a monorepo's unrelated services do not trigger rebuilds.
- `ignore` (optional): excludes paths, in addition to `.dockerignore`.

In the tutorial, an image is attached to a resource because its name appears in YAML loaded with `k8s_yaml` (the page notes this is not the only way). A full update runs: build, push (if the cluster needs it), then deploy via `kubectl`. Tilt tags images `:tilt-<hash>` and rewrites the YAML or Helm chart during deploy, avoiding rolling tags such as `:latest`. It then tracks the pod rollout and streams logs.

## Live Update

In unoptimized Kubernetes development, every change means rebuild, push, apply, and wait for a rollout. Live Update updates the containers in place.

```python
docker_build(
    'tilt-avatar-api',
    context='.',
    dockerfile='./deploy/api.dockerfile',
    only=['./api/'],
    live_update=[
        sync('./api/', '/app/api/'),
        run(
            'pip install -r /app/requirements.txt',
            trigger=['./api/requirements.txt']
        )
    ]
)
```

- `sync(local, remote)`: the local path (relative to the Tiltfile, recursive) is watched; the remote path is an absolute path inside the container. Synced files must match paths already watched for the image.
- `run(cmd, trigger=[...])`: runs a command inside the container when a changed file matches the trigger.

With a hot-reload framework such as the Flask dev server, copying the file is enough. Where the framework cannot reload code, Live Update can restart the process; see the Live Update Reference.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read tutorial step 4 (Code. Update. Repeat.) and step 5 (Smart Rebuilds with Live Update) in full. Confirmed the `docker_build` argument semantics for `context`, `dockerfile`, `only` and `ignore`, how an image is attached to a resource, the three update steps, the `:tilt-<hash>` tag rationale, the `sync` and `run` explanations and the hot-reload note. Qualified or trimmed: "every change" (page says unoptimized development), "because" for image-to-resource attachment (page says not the only way), "only when" for run triggers (not stated on these two pages) and "Webpack needs only the file copy" (the pages confirm this only for Flask). 

Method: documentation only; no commands were run.
