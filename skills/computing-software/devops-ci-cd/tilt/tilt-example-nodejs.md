---
id: computing-software.devops-ci-cd.tilt.tilt-example-nodejs
name: tilt-example-nodejs
category: computing-software
field: devops-ci-cd
product: tilt
tags: [example-nodejs, tilt, nodejs, live-update]
level: practitioner
status: docs-checked
description: "Speed up the Tilt feedback loop for a Node.js Express server: Dockerfile layer caching, then live_update with sync, run and nodemon."
sources:
  - "https://docs.tilt.dev/example_nodejs.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js with Tilt

Goal: shorten code-change-to-new-process time for an Express server (example repo: tilt-example-nodejs).

## Step 0: simplest deployment

```python
docker_build('example-nodejs-image', '.')
k8s_yaml('kubernetes.yaml')
k8s_resource('example-nodejs', port_forwards=8000)
```

The image name must match the Deployment's container `image`; the resource name must match `metadata.name`. Server at `localhost:8000`.

## Step 1: measure

```python
local_resource(
  'deploy',
  'date +%s > start-time.txt'
)
k8s_resource('example-nodejs', port_forwards=8000,
    resource_deps=['deploy']
)
```

The server reads `start-time.txt` and shows elapsed time. Naive: 11.31-14.21s, partly because `yarn install` ran on every build.

## Step 2: Dockerfile caching (3.25-4.12s)

Add dependency files and install before copying the rest:

```
FROM node:10
WORKDIR /app
ADD package.json .
ADD yarn.lock .
RUN yarn install
ADD . .
ENTRYPOINT [ "node", "/app/index.js" ]
```

## Step 3: live update (1.1-1.8s)

Run the app under nodemon (added with `yarn add --dev nodemon`):

```python
docker_build('example-nodejs-image', '.',
    build_args={'node_env': 'development'},
    entrypoint='yarn run nodemon /app/index.js',
    live_update=[
        sync('.', '/app'),
        run('cd /app && yarn install', trigger=['./package.json', './yarn.lock']),
        run('touch /app/index.js', trigger='./start-time.txt'),
    ])
```

- `entrypoint` overrides the Dockerfile `ENTRYPOINT`.
- `build_args` pairs with `ARG node_env=production` and `ENV NODE_ENV $node_env` in the Dockerfile, so `yarn install` installs dev dependencies.
- On a live update Tilt syncs `.` to `/app`, runs `yarn install` only if `package.json` or `yarn.lock` changed, and touches `index.js` so nodemon reloads.

## CI

Run `tilt ci` against a `ctlptl` single-use cluster.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/example_nodejs.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed. The skill omits the guide's final demo `sed` step.

Method: documentation only; no commands were run.
