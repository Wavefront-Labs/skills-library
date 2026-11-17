---
id: computing-software.devops-ci-cd.verdaccio.user-rate-limit
name: user-rate-limit
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [rate-limit, user-rate-limit, brute-force, userratelimit, windowms, ddos]
level: practitioner
status: docs-checked
description: "Tune rate limits on user endpoints (npm login, token, profile, web login) with userRateLimit, and the separate web UI data endpoint limit."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/best/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rate limits protect brute-forceable endpoints. Default for user endpoints (npm token, npm login/adduser, npm profile, the website `/sec/login`): 100 requests per 15 minutes.

```yaml
userRateLimit:
  windowMs: 50000      # minutes * 60 * 1000
  max: 1000            # requests per window
```
Website data endpoints (search, packages, sidebar, detail) default to 5000 requests per 2 minutes and are set under `web.rateLimit` (`max: 5000`, `windowMs: 120000`); prefer `userRateLimit`. CSS and JS are not counted. The CLI endpoints used by `npm install` are not limited.

Behind a proxy, set `server.trustProxy`, otherwise all users share the proxy's address and are throttled together.

The best practices page recommends tuning both values to your needs to guard the critical endpoints against brute-force or DDoS attacks.

## Checked

2026-11-04. Confirmed against the Configuration, Best Practices and Web UI pages (user endpoint list, 100 per 15 minutes, windowMs and max, web rateLimit 5000 per 120000 ms, CSS/JS not counted, CLI endpoints not limited, trustProxy and its rate-limit effect). Removed: the middleware feature-flag aside and the closing Verify tip.
Method: documentation only; no commands were run.
