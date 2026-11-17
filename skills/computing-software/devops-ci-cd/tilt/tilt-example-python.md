---
id: computing-software.devops-ci-cd.tilt.tilt-example-python
name: tilt-example-python
category: computing-software
field: devops-ci-cd
product: tilt
tags: [example-python, tilt, flask, live-update]
level: practitioner
status: docs-checked
description: "Speed up the Tilt feedback loop for a Python Flask server: pip layer caching, then live_update with sync and run steps and Flask debug reload."
sources:
  - "https://docs.tilt.dev/example_python.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python (Flask) with Tilt

Goal: shorten code-change-to-new-process time for a Flask server (example repo: tilt-example-python).

## Step 0: simplest deployment

```python
docker_build('example-python-image', '.')
k8s_yaml('kubernetes.yaml')
k8s_resource('example-python', port_forwards=8000)
```

The image name must match the Deployment's container `image`; the resource name must match `metadata.name`. Server at `localhost:8000`.

## Step 1: measure

```python
local_resource(
  'deploy',
  'date +%s > start-time.txt'
)
k8s_resource('example-python', port_forwards=8000,
             resource_deps=['deploy'])
```

The app reads `/app/start-time.txt` at startup and shows elapsed time. Naive: 10-11s, with `pip install` running on every build.

## Step 2: Dockerfile caching (2.5-3.1s)

Install requirements before copying the rest of the code:

```
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .
```

## Step 3: live update (1-2s)

```python
docker_build('example-python-image', '.', build_args={'flask_debug': 'True'},
    live_update=[
        sync('.', '/app'),
        run('cd /app && pip install -r requirements.txt',
            trigger='./requirements.txt'),
        run('touch /app/app.py', trigger='./start-time.txt'),
    ])
```

On a live update Tilt syncs `.` to `/app`, runs `pip install` only if `requirements.txt` changed, and touches `app.py` so Flask reloads.

`build_args` pairs with this Dockerfile change, which makes Flask run in development mode (it watches files and reloads):

```
ARG flask_debug=False
ENV FLASK_DEBUG $flask_debug
```

## CI

Run `tilt ci` against a `ctlptl` single-use cluster.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/example_python.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed. The skill omits the guide's final demo `sed` step.

Method: documentation only; no commands were run.
