---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-bouncers-api-stream-and-query
name: crowdsec-bouncers-api-stream-and-query
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [bouncers-api, decisions-stream, startup, query-mode, x-api-key, custom-bouncer]
level: advanced
status: docs-checked
description: "Write or debug a remediation component against the Local API: API key auth, query mode and the decisions stream with startup."
sources: ["https://raw.githubusercontent.com/crowdsecurity/crowdsec-docs/main/crowdsec-docs/docs/local_api/bouncers-api.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Remediation components authenticate with an API key sent in the `X-Api-Key` header. Create one with `cscli bouncers add MyTestClient` (shown once). A request without a valid key gets 403. Their methods are limited to the `/decisions` path.

```console
curl -H "X-Api-Key: KEY" -I localhost:8080/v1/decisions
```

## Query mode

For bouncers that ask about a specific target:

```console
curl -H "X-Api-Key: KEY" "localhost:8080/v1/decisions?ip=192.168.1.1"
curl -H "X-Api-Key: KEY" "localhost:8080/v1/decisions?range=1.2.3.0/24&contains=false"
curl -H "X-Api-Key: KEY" "localhost:8080/v1/decisions?scope=username&value=myuser"
curl -H "X-Api-Key: KEY" "localhost:8080/v1/decisions?type=enforce_mfa"
```

The docs show range queries with `contains=false` and `contains=true`, which return different results; check the Local API swagger documentation for exact semantics. A decision on `2.2.3.0/24` is returned for a query on an IP inside it.

## Stream mode

Streaming is really polling: the bouncer calls `/v1/decisions/stream` on a schedule. The single `startup` boolean says whether it wants the full current state.

```console
curl -s -H "X-Api-Key: KEY" "localhost:8080/v1/decisions/stream?startup=true"
curl -s -H "X-Api-Key: KEY" "localhost:8080/v1/decisions/stream?startup=false"
```

The first call (`startup=true`) returns the current decisions (local and Central API) plus past deleted ones, so a restarted Local API does not desynchronise bouncers; later calls (`startup=false`) return only changes since the previous pull, so an immediate repeat gives empty results. Test with `cscli decisions add -i 192.168.1.1` and `-r 2.2.3.0/24`.

## Checked
2026-11-08. Confirmed against the page source in the crowdsec-docs repository (the docs.crowdsec.net/docs/local_api/bouncers-api URL returned 404, so the raw source is cited): X-Api-Key auth, the 403 note, query examples for IP, range, scope/value and type, stream mode and the `startup` parameter. Rewrote the `contains` and first-call sentences, which overstated what the page says.
Method: documentation only; no commands were run.
