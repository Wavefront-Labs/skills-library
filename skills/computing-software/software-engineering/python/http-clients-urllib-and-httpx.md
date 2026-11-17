---
id: computing-software.software-engineering.python.http-clients-urllib-and-httpx
name: http-clients-urllib-and-httpx
category: computing-software
field: software-engineering
product: python
tags: [python, urllib, httpx, requests, http-client, timeouts, retries]
level: practitioner
status: verified
description: "Make HTTP calls from Python correctly: stdlib urllib.request for zero-dependency scripts, httpx/requests with clients, timeouts, retries, and streaming large downloads."
sources: ["https://docs.python.org/3/library/urllib.request.html", "https://www.python-httpx.org/advanced/clients/", "https://www.python-httpx.org/advanced/timeouts/", "https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP clients: urllib and httpx

**Goal:** HTTP calls that time out, reuse connections, retry only what is safe, and
don't load 2 GB into memory.

## Stdlib only (scripts, bootstrap tools)
```python
import json, urllib.request, urllib.error
req = urllib.request.Request(
    "https://api.example.org/v1/items",
    data=json.dumps({"name": "x"}).encode(),
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:     # timeout is NOT default
        body = json.load(resp)
except urllib.error.HTTPError as e:      # 4xx/5xx raise; e.read() has the body
    detail = e.read().decode(errors="replace")
except urllib.error.URLError as e:       # DNS, refused, TLS
    ...
```
No connection pooling, no retries; fine for a handful of calls.

## httpx (sync + async, HTTP/2) or requests
```python
import httpx
client = httpx.Client(
    base_url="https://api.example.org",
    timeout=httpx.Timeout(10.0, connect=3.0),
    headers={"User-Agent": "mytool/1.4"},
    transport=httpx.HTTPTransport(retries=2),     # retries connection failures only
)
r = client.get("/v1/items", params={"page": 2})
r.raise_for_status()
items = r.json()
client.close()       # or `with httpx.Client(...) as client:`
```
- Create one client per app/target and reuse it: per-call `httpx.get()` opens a new TCP+TLS
  connection each time.
- httpx has no default infinite timeout (5 s default); `requests` has **none** - always pass
  `timeout=`.

## Retries for HTTP status codes
Retry idempotent requests on 429/502/503/504 with backoff, honouring `Retry-After`:
```python
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
s = requests.Session()
s.mount("https://", HTTPAdapter(max_retries=Retry(total=5, backoff_factor=0.5,
        status_forcelist=[429, 502, 503, 504], allowed_methods=["GET", "PUT", "DELETE"])))
```
For httpx use `tenacity` around calls or a retrying transport. Never blindly retry POST
without an idempotency key.

## Streaming large bodies
```python
with client.stream("GET", url) as r:
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_bytes(chunk_size=1 << 20):
            f.write(chunk)
```

## Gotchas
- TLS errors behind corporate proxies: point `verify=` at the CA bundle (or use `truststore`),
  don't disable verification.
- `HTTPS_PROXY`/`NO_PROXY` env vars are honoured by default (`trust_env=True`).
- Log method, URL (minus secrets), status and elapsed (`r.elapsed`) for every call.

## Verify
- [ ] grep: every `requests.`/`httpx.` call path has a timeout; clients are reused.
- [ ] Retries limited to idempotent methods and retryable statuses.

## Checked
- Python 3.14.0 against a local `http.server` (httpx, requests, urllib3 current pip releases): urllib POST with JSON and headers worked, `HTTPError` carried 404 body, default socket timeout is None; httpx default `Timeout(timeout=5.0)`; a reused `httpx.Client` used 1 TCP connection for 3 calls while `httpx.get` used 3; `HTTPTransport(retries=2)` retried connection errors but returned a 503 without retry; `ReadTimeout` raised; `stream`/`iter_bytes` read 3 MB; `trust_env` True; requests `Retry` with status_forcelist retried 503 twice, honouring `Retry-After` (about 2 s), `respect_retry_after_header` True; requests `timeout` defaults to None; `http2=True` works only with `h2` installed. Corporate proxy/truststore advice was not run.
