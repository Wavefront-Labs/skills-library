---
id: computing-software.devops-ci-cd.concourse-ci.credential-caching-and-retries
name: credential-caching-and-retries
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [credentials, caching, secret-cache, retry, secret-retry-attempts, vault, web-node]
level: advanced
status: docs-checked
description: "Reduce load on the credential server with secret caching and tune retries: cache duration, not-found caching, lease interaction, and avoiding duplicate retries with Vault."
sources:
  - https://concourse-ci.org/docs/operation/creds/caching/
  - https://concourse-ci.org/docs/operation/creds/retrying-failed/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default every credential is fetched each time it is used, which with many pipelines means a lot of requests to the credential server. On the web node:

```properties
CONCOURSE_SECRET_CACHE_ENABLED=true
CONCOURSE_SECRET_CACHE_DURATION=5m
CONCOURSE_SECRET_CACHE_DURATION_NOTFOUND=1s
```

Caching applies to credential managers and to var sources. The default duration is one minute. If the manager supplies a lease, such as Vault returning a lease duration, the shorter of the configured duration and the lease is used. The absence of a credential is also cached, by default for 10 seconds, so Concourse does not keep looking for a misconfigured credential; lower it with `CONCOURSE_SECRET_CACHE_DURATION_NOTFOUND`.

**Retries.** When a request to the credential manager fails with an intermittent error such as a timeout or `connection refused`, Concourse retries up to 5 times, then surfaces the error in the UI for the check or build step that made the request.

```properties
CONCOURSE_SECRET_RETRY_ATTEMPTS=5
CONCOURSE_SECRET_RETRY_INTERVAL=10s
```

With the Vault credential manager the Vault API client already retries, so set `CONCOURSE_SECRET_RETRY_ATTEMPTS` to 0 or a small value like 1 or 2 to avoid duplicate retries.

## Checked

2026-11-04. Defaults, variables and the Vault note confirmed on the Caching credentials and Retrying failed fetches pages. Removed the rotation tradeoff remark (not stated on the pages).

Method: documentation only; no commands were run.
