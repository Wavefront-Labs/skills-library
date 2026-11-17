---
id: computing-software.cybersecurity-defensive.authelia.dev-endpoints-and-csp-template
name: dev-endpoints-and-csp-template
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, pprof, expvar, content-security-policy, csp, hardening, buffers, timeouts]
level: advanced
status: docs-checked
description: "Understand Authelia server hardening options: why pprof and expvars stay off, the csp_template header override, and buffer and timeout settings."
sources:
  - https://www.authelia.com/configuration/miscellaneous/server/
  - https://www.authelia.com/configuration/miscellaneous/logging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Several `server` options exist for developers or for rare tuning, and the safe move is usually to leave them alone.

```yaml
server:
  headers:
    csp_template: ''
  buffers:
    read: 4096
    write: 4096
  timeouts:
    read: '6s'
    write: '6s'
    idle: '30s'
  endpoints:
    enable_pprof: false
    enable_expvars: false
```

- `enable_pprof` turns on the Go pprof endpoints and `enable_expvars` turns on the expvar endpoints. The documentation says plainly not to enable either in production.
- Log level `trace` has the same side effect: it exposes `/debug/vars` and `/debug/pprof/`, as well as producing a large volume of log entries. The logging page says these endpoints should not be enabled in production.
- `headers.csp_template` replaces the `Content-Security-Policy` header value. Authelia replaces every `${NONCE}` placeholder in your template with the nonce value of its React bundle. The page calls this a security-critical header that should almost never be customised, and recommends advice from a security professional before changing it.
- `buffers` and `timeouts` tune the HTTP server read and write buffers and the read, write and idle timeouts. The values above are the page's example configuration; the page says the read and write buffer sizes should generally be the same.

Check: after any change, load the portal in a browser with developer tools open and confirm no CSP violations appear and the header matches your template.

## Checked

2026-11-08. Read the full Authelia Server and Log pages. Confirmed enable_pprof and enable_expvars as developer endpoints not for production, the trace level exposing /debug/vars and /debug/pprof/, the csp_template security notice and ${NONCE} placeholder, and the buffer sizing note. Removed an unsourced operational instruction and corrected the claim that the shown buffer and timeout values were defaults.

Method: documentation only; no commands were run.
