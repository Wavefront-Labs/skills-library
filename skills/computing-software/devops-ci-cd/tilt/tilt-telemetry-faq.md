---
id: computing-software.devops-ci-cd.tilt.tilt-telemetry-faq
name: tilt-telemetry-faq
category: computing-software
field: devops-ci-cd
product: tilt
tags: [telemetry-faq, tilt, analytics, privacy]
level: intro
status: docs-checked
description: "What anonymized analytics Tilt sends and how to opt in or out with tilt analytics, environment variables or the Tiltfile."
sources:
  - "https://docs.tilt.dev/telemetry_faq.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tilt telemetry and analytics

Goal: know what Tilt sends and control whether it does.

## What and where

Tilt sends anonymized data about how you use it. The first time you visit the web UI it nudges you to opt in or out explicitly. Data goes to an in-house ingestion server at `events.windmill.build` and may be stored in managed database or analytics services. The page says it will not be resold or given to advertisers.

If you opt in, Tilt records aggregate usage: which Tiltfile built-ins are used and which parts of the web UI are touched. Strings that may reveal your project (repo, service and directory names) are hashed where possible. Hashing is not foolproof: snippets such as a service name or a parse-error message could be included, and the page says you should probably not opt in on a classified project.

Example event for `tilt up`: fields `watch`, `version`, `user`, `os`, `name` (`tilt.cmd.up`), `mode`, `machine`, `git.origin`. A Tiltfile load event (`tilt.tiltfile.loaded`) adds counters such as `tiltfile.invoked.docker_build` and `tiltfile.invoked.docker_build.arg.context`.

## Controls

```bash
tilt analytics opt in
tilt analytics opt out    # then restart Tilt
```

Disable for the current environment:

```bash
export TILT_DISABLE_ANALYTICS="true"
export DO_NOT_TRACK="1"    # also respected
```

Enable from the Tiltfile (meant for devtools teams opting in all users):

```python
analytics_settings(enable=True)
```

Precedence: the Tiltfile setting overrides user preferences; the environment setting overrides both the Tiltfile and user preferences.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the What does Tilt send? page in full. Confirmed the opt-in and opt-out commands, the ingestion host, the hashing caveat, both example events, `TILT_DISABLE_ANALYTICS`, `DO_NOT_TRACK`, `analytics_settings(enable=True)` and the stated precedence. Softened: the classified-project advice, which the page words as "probably". 

Method: documentation only; no commands were run.
