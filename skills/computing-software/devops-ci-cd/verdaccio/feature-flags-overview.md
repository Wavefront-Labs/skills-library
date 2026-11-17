---
id: computing-software.devops-ci-cd.verdaccio.feature-flags-overview
name: feature-flags-overview
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [feature-flags, experiments, flags, flags-block, changepassword, weblogin, stage, tfa]
level: intro
status: docs-checked
description: "The flags block (formerly experiments) in Verdaccio: all flags default off, which exist on 6.x and 7.x, and the inert searchRemote flag."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/staged-publishing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
flags:
  changePassword: false
  webLogin: true
```
All flags are off by default and are experimental, including long-lived ones: the flag, its endpoints or behaviour may change in any line.

| Flag | Lines | Enables |
|---|---|---|
| changePassword | 6.x, 7.x | password change in web UI |
| createUser | 6.x, 7.x | user registration in web UI |
| webLogin | 6.x, 7.x | browser-based CLI login |
| stage | 7.x | staged publishing (npm stage) |
| tfa | 7.x | two-factor authentication |

`stage` and `tfa` do not exist on 6.x.

Gotchas:
- `searchRemote` does nothing: 6.x forces it to false and nothing reads it; it is gone from 7.x. Remove it; keeping it only gives a startup warning about enabled experiments.
- Startup warnings about enabled flags disappear only if you comment out the whole `flags` and `experiments` sections.
- The staged publishing page says to restart after enabling its flag because the configuration is read at startup.

See the dedicated skills for each flag.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (Feature Flags) and Staged publishing. Confirmed: the flag table with lines, flags off by default, every flag experimental, the inert searchRemote flag and the warnings behaviour. Removed or corrected: the unsupported claim that every flag change needs a restart; reworded to what the staged publishing page says.

Method: documentation only; no commands were run.
