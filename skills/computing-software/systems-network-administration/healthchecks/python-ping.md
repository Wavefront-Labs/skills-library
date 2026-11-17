---
id: computing-software.systems-network-administration.healthchecks.python-ping
name: python-ping
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, python, requests-library, urllib, post-diagnostics]
level: intro
status: docs-checked
description: "Send Healthchecks pings from Python with requests or the standard library urllib, with timeouts, error handling and a POST body for diagnostics."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/python.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/signaling_failures.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/resources.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With the requests library (10 second timeout, failure printed):

```python
import requests

try:
    requests.get("<ping-url>", timeout=10)
except requests.RequestException as e:
    # Log ping failure here...
    print("Ping failed: %s" % e)
```

With only the standard library:

```python
import socket
import urllib.request

try:
    urllib.request.urlopen("<ping-url>", timeout=10)
except socket.error as e:
    # Log ping failure here...
    print("Ping failed: %s" % e)
```

Diagnostic data goes in a POST body:

```python
import requests
requests.post("<ping-url>", data="temperature=-7")
```

Tips: always set a timeout, and catch ping errors so a monitoring hiccup does not stop the job. For failures, wrap the work in `try` / `finally` and ping the normal URL on success or the `/fail` URL otherwise. For timing, ping `/start` first (see run-time-measurement).

Third-party wrappers exist: healthchecks_wrapper and healthchecks-decorator (context managers), py-healthchecks.io (create and ping, sync and async).

## Checked

2026-11-04: confirmed against the Python page (requests, urllib, POST body), the Signaling failures page (try/finally pattern), the Measuring Script Run Time page (/start) and the Third-Party Resources page (wrappers).
Method: documentation only; no commands were run.
