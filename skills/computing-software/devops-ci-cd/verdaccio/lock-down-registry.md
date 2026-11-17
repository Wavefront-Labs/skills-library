---
id: computing-software.devops-ci-cd.verdaccio.lock-down-registry
name: lock-down-registry
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [lockdown, anonymous-publish, authenticated-access, access-authenticated, eneedauth, hardening]
level: advanced
status: docs-checked
description: "Make every package require login with access $authenticated, allow anonymous publish on a pattern, and why npm still needs a token (ENEEDAUTH)."
sources:
  - https://verdaccio.org/docs/best/
  - https://verdaccio.org/docs/authentication/
  - https://verdaccio.org/docs/setup-npm/
  - https://verdaccio.org/docs/e2e/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default access is public. To require login for everything (private packages also disappear from the web UI for outsiders):

```yaml
packages:
  '@my-company/*':
    access: $authenticated
    publish: $authenticated
  '@*/*':
    access: $authenticated
    publish: $authenticated
  '**':
    access: $authenticated
    publish: $authenticated
```
Combine with HTTPS, JWT expiry and rate limits (see related skills); the best practices page also covers staged publishing and two-factor as experimental extras.

Anonymous publish:
```yaml
'my-company-*':
  access: $anonymous
  publish: $anonymous
  proxy: npmjs
```
Allowing it is not enough: npm refuses to publish when logged out (`ENEEDAUTH`) on current npm (still true on 11). The authentication page says to run `npm adduser` first, but the npm setup page says that since npm 9 `adduser` creates a user without logging in and npm 12 removed it, so use `npm login` for an existing user; or for a throwaway registry write any string as `//localhost:4873/:_authToken=...` (the token is not validated).

Self-registration: the default htpasswd plugin lets anyone register; set `max_users: -1`.

Verify: without credentials the registry refuses access ("nobody can access your registry unless they are authorized").

## Checked

2026-11-04. Read the Verdaccio documentation pages: Best Practices, Authentication, Setup npm and End to End testing. Confirmed: the all-$authenticated config and web UI hiding, the anonymous publish config, ENEEDAUTH on npm 11, max_users: -1 and the dummy _authToken. Removed or corrected: the verify command; the pages disagree on npm adduser (noted in the skill).

Method: documentation only; no commands were run.
