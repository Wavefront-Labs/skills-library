---
id: computing-software.rpa-and-low-code.n8n.http-request-common-issues
name: http-request-common-issues
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, http-request, docker-networking, rate-limits, batching, multipart]
level: practitioner
status: docs-checked
description: "Fix n8n HTTP Request node errors: 400, 404, ECONNREFUSED in Docker, invalid JSON, 403, 429 batching and retry, wrong upload file name and 415 multipart uploads."
sources:
  - https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/common-issues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: diagnose HTTP Request node failures.

- **400 Bad request**: invalid Query Parameter name or value; for arrays try the **Array Format in Query Parameters** option.
- **404 resource not found**: wrong or deprecated URL.
- **ECONNREFUSED**: a reachable host with no listener. In Docker, `localhost` and `127.0.0.1` mean the n8n container. For a host service use `http://host.docker.internal:<port>` (Docker Desktop); on Linux add `--add-host=host.docker.internal:host-gateway` or Compose `extra_hosts: - "host.docker.internal:host-gateway"`. For another Compose service use its service name and internal port, not the published mapping. On Node.js 17+ `localhost` may resolve to `::1`; use `http://127.0.0.1:<port>` when the target binds IPv4 only. Test with `docker exec -it n8n wget -qO- http://host.docker.internal:5000/health`. On n8n Cloud there is no path to localhost: use a tunnel.
- **JSON parameter must be valid JSON**: validate it; if you use an expression wrap the whole object in double curly braces.
- **403 Forbidden**: check credentials, scopes and permissions; regenerate the key.
- **429**: add **Add Option > Batching** (**Items per Batch**, **Batch Interval (ms)**, for example `1000` for one request per second) or in **Settings** enable **Retry on Fail** with **Max Tries** and **Wait Between Tries (ms)**.

## File uploads
- Wrong file name: with **Form-Data**, the part's file name comes from the binary data, not **Name** (which is only the field name); with none, n8n sends `file`. Set it in Convert to File (**File Name** option) or in a Code node:
```javascript
for (const item of $input.all()) {
	item.binary.data.fileName = 'index.html';
}
return $input.all();
```
The binary MIME type is copied into the part's `Content-Type`.
- 415 Unsupported media type: **n8n Binary File** as body sends the raw file with no multipart envelope. For multipart set **Body Content Type** to **Form-Data**, add a Body Parameter of type **n8n Binary File**, **Name** = the API's field name, **Input Data Field Name** = the binary property (such as `data`).

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/common-issues

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
