---
id: computing-software.devops-ci-cd.tilt.tilt-debuggers-python
name: tilt-debuggers-python
category: computing-software
field: devops-ci-cd
product: tilt
tags: [debuggers-python, tilt]
level: practitioner
status: docs-checked
description: "Connect a remote Python debugger such as remote-pdb to a container in a Tilt environment by exposing a container port and forwarding it."
sources:
  - "https://docs.tilt.dev/debuggers_python.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging Python in Tilt

Goal: attach a debugger to an app running in Kubernetes through Tilt's port forwarding. The example uses `remote-pdb`; most of the steps apply to any remote debugger, and only the end varies by tool. Tilt has no debugger-specific code.

## Set-up

1. Decide the debugger port (the example uses `5555`).
2. Add your debugger to requirements.txt.
3. Expose the port as a `containerPort` in the Deployment or Pod YAML, alongside your normal ports:

```yaml
kind: Deployment
...
spec:
    spec:
      containers:
        - name: example-python
          image: example-python-image
          ports:
            - containerPort: 8000  # the app itself
            - containerPort: 5555  # debugger
```

4. In the Tiltfile, forward that port too:

```python
k8s_resource('example-python', port_forwards=[
    8000,  # app
    5555,  # debugger
])
```

## Debug with remote-pdb

1. Insert the breakpoint:

```python
from remote_pdb import RemotePdb
RemotePdb('127.0.0.1', 5555).set_trace()
```

2. Trip the breakpoint (in the example, hit `localhost:8000`). The request hanging is expected: execution paused at the breakpoint.
3. Connect, e.g. with Netcat: `nc 127.0.0.1 5555`

The debugger does not start until the first `set_trace` call, so do not connect before then or you will see errors. The log line showing it is active is `RemotePdb session open at 127.0.0.1:5555, waiting for connection ...`

## Other debuggers

For a debugger not listed, use `local_resource` to spin it up, and consider packaging it as a Tilt extension. A `web-pdb` example offers a browser instead of a terminal.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/debuggers_python.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
