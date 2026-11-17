---
id: computing-software.devops-ci-cd.argo-workflows.retry-strategy
name: retry-strategy
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [retry-strategy, retry-policy, on-transient-error, expression, backoff]
level: practitioner
status: docs-checked
description: "Configure retryStrategy with limit, retryPolicy values, a conditional expression over lastRetry variables, and backoff, including how defaults interact."
sources: ["https://argo-workflows.readthedocs.io/en/latest/retries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retry strategy and policies
Set `retryStrategy` on a template: `limit: "10"` caps attempts (it is a quoted string in the examples). `retryPolicy` chooses what to retry:
- `Always`: every failed step.
- `OnFailure`: the main container is marked failed by Kubernetes.
- `OnError`: controller errors, or failures of the init or wait containers.
- `OnTransientError`: errors the controller classes as transient, or matching the `TRANSIENT_ERROR_PATTERN` environment variable.

Defaults: `OnFailure` when only `limit` is given, but `Always` when an `expression` is supplied without a policy (then only the expression decides). If both are given they are ANDed and both must be true. Policy and expression are re-evaluated after every attempt, so with `OnFailure` a second attempt that ends in an error is not retried again.

`expression` is an expr expression that sees the previous attempt:
- `lastRetry.exitCode` (string, "-1" if unavailable), e.g. `asInt(lastRetry.exitCode) > 1`
- `lastRetry.status` (Error or Failed)
- `lastRetry.duration` in seconds
- `lastRetry.message`, e.g. `lastRetry.message matches 'imminent node shutdown|pod deleted'`

A false expression stops retrying. Delay between attempts is set with `backoff` (see examples retry-backoff.yaml). Infrastructure failures before the container starts, such as evictions, belong to automatic pod restarts, not this page.

## Checked

2026-11-08. Read the Argo Workflows retries page in full (raw markdown) and confirmed limit, the four retryPolicy values, the default policy rules and expression interaction, re-evaluation after each attempt, the lastRetry variables, and backoff. Nothing removed.

Method: documentation only; no commands were run.
