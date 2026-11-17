---
id: computing-software.devops-ci-cd.tilt.tilt-example-static-html
name: tilt-example-static-html
category: computing-software
field: devops-ci-cd
product: tilt
tags: [example-static-html, tilt, live-update, benchmark]
level: intro
status: docs-checked
description: "Minimal Tilt example: deploy a busybox static HTML server, benchmark updates with a local_resource, and cut deploy time with live_update."
sources:
  - "https://docs.tilt.dev/example_static_html.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static HTML with Tilt

Goal: confirm Tilt works in your environment with the simplest possible server, then measure and shorten the update loop (example repo: tilt-example-html).

## Step 0: simplest deployment

The server is a two-line shell script (`echo "Serving files on port 8000"` then `busybox httpd -f -p 8000`). You need a Dockerfile, a Kubernetes Deployment, and a Tiltfile:

```python
docker_build('example-html-image', '.')
k8s_yaml('kubernetes.yaml')
k8s_resource('example-html', port_forwards=8000)
```

The `docker_build` image name must match the container `image` in the `example-html` Deployment. The `k8s_resource` name must match `metadata.name`. Server at `localhost:8000`.

```
git clone https://github.com/tilt-dev/tilt-example-html
cd tilt-example-html/0-base
tilt up
```

Tilt opens the web UI; the status icon turns green and the log shows "Serving files on port 8000."

## Step 1: measure

```python
k8s_resource('example-html', port_forwards=8000, resource_deps=['deploy'])

local_resource(
  'deploy',
  'date +%s > start-time.txt')
```

`local_resource` runs a command on your machine and appears in the sidebar; clicking the button on `deploy` triggers an update. The server reads the start time and prints elapsed time. Naive: 1-2s. The elapsed time in the Tilt sidebar differs from the app's benchmark; both are useful.

## Step 2: live update (0-1s)

Instead of building an image, deploying configs and waiting for scheduling, update the pod in place:

```python
docker_build('example-html-image', '.', live_update=[
  sync('.', '/app'),
  run('./report-deployment-time.sh'),
  run('sed -i "s/Hello cats/Congratulations, you set up live_update/g" index.html'),
])
```

Step one syncs the current directory to `/app` in the container; step two runs the script that reports deployment time; step three edits the page text.

## CI

Run `tilt ci` against a `ctlptl` single-use cluster; it deploys all services and exits successfully if they are healthy.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/example_static_html.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
