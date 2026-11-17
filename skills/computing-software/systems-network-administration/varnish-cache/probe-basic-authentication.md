---
id: computing-software.systems-network-administration.varnish-cache.probe-basic-authentication
name: probe-basic-authentication
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [probe-request, basic-auth, authorization-header, backend-health]
level: practitioner
status: docs-checked
description: "Make health probes pass against a backend that requires basic authentication by replacing .url with a full .request carrying an Authorization header."
sources:
  - https://www.varnish.org/docs/tutorials/vcl-backend-probe-basic-authentication/
  - https://www.varnish.org/docs/reference/vcl-probe/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# probe basic authentication

Symptom: the probe gets `401 Unauthorized`, the log shows the backend as sick and fetches return `503 Backend fetch failed`:

```
varnishlog -g raw -i backend_health
Backend_health - boot.default Still sick ... HTTP/1.1 401 Unauthorized
```

Fix: use `.request` instead of `.url`; each string becomes one header line and the block ends with a blank line.

```vcl
vcl 4.1;
backend default {
    .host = "127.0.0.1";
    .port = "8080";
    .probe = {
        .request =
            "HEAD / HTTP/1.1"
            "Authorization: Basic BASE64_OF_USER_COLON_PASSWORD"
            "Host: localhost"
            "Connection: close"
            "User-Agent: Varnish Health Probe";
        .timeout = 2s;
        .interval = 5s;
        .window = 10;
        .threshold = 5;
    }
}
```

Replace the placeholder with the base64 encoding of `user:password`. `Connection: close` is mandatory in probe requests.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the generic Verify tip.

Method: documentation only; no commands were run.
