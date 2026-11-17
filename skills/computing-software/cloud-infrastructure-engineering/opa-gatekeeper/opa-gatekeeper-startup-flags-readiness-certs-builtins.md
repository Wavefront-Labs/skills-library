---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-startup-flags-readiness-certs-builtins
name: opa-gatekeeper-startup-flags-readiness-certs-builtins
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, startup, flags, readiness-retries, cert-rotation, disable-opa-builtin, http-send, pprof]
level: advanced
status: docs-checked
description: "Configure Gatekeeper startup behaviour: readiness-retries, disabling cert rotation, disabling OPA built-ins such as http.send, and enabling pprof."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/customize-startup.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper startup flags readiness certs builtins

Startup flags worth knowing:
- `--readiness-retries`: webhook servers stay unavailable during bootstrapping until the initial set of constraints, templates and synced objects is ingested, so the webhook never validates against an incomplete policy set. This flag sets how many retries an object (for example a Constraint) gets to be added to OPA. Default `0`; `-1` retries forever, which guarantees complete enforcement but can block the webhook indefinitely.
- `--disable-cert-rotation`: by default Gatekeeper uses `open-policy-agent/cert-controller` to generate and rotate the webhook certificate. Pass this flag to use a third-party solution instead.
- `--disable-opa-builtin`: disables named OPA built-ins. Since v3.8.0 `http.send` is disabled by default (see the external data guide for the safer alternative).
- `--enable-pprof`: serves Go pprof profiling over HTTP, on `localhost:6060` by default; change with `--pprof-port`.

For the full flag list of your version, run the binary with `--help`, using an image tag that matches the Gatekeeper version you run, for example `docker run openpolicyagent/gatekeeper:v3.10.0-beta.0 --help`.

## Checked

2026-11-04. Confirmed against customize-startup.md. Removed or corrected: nothing.

Method: documentation only; no commands were run.
