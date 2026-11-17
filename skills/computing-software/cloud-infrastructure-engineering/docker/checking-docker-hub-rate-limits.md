---
id: computing-software.cloud-infrastructure-engineering.docker.checking-docker-hub-rate-limits
name: checking-docker-hub-rate-limits
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, rate-limit, rate-limits, rate-limit-headers, hub-rate-limit, docker-hub, toomanyrequests]
level: practitioner
description: "Read Docker Hub ratelimit-limit and ratelimit-remaining headers for anonymous or authenticated pulls and stop toomanyrequests failures in CI."
sources: ["https://docs.docker.com/docker-hub/usage/pulls/", "https://docs.docker.com/docker-hub/usage/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checking Docker Hub rate limits

Symptom: HTTP 429 with the body `You have reached your pull rate limit. You may increase the limit by
authenticating and upgrading: https://www.docker.com/increase-rate-limits` in CI, often from a shared NAT IP.
The message appears in the Docker CLI or the Docker Engine logs.

## Check remaining quota

```sh
# anonymous (counted per source IP)
TOKEN=$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
# authenticated (counted per account)
TOKEN=$(curl -s --user "$HUB_USER:$HUB_SECRET" "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
curl -s --head -H "Authorization: Bearer $TOKEN"   https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest | grep -i ratelimit
# ratelimit-limit: 100;w=21600
# ratelimit-remaining: 20;w=21600
# docker-ratelimit-source: 192.0.2.1
```

`w=21600` is the window in seconds (6 hours). The headers come back on both GET and HEAD; GET emulates a real
pull and counts towards the limit, HEAD does not. If you see no `ratelimit` headers, the image or your IP may
be unlimited through a partnership with a publisher, provider or open source organization, or you may be
pulling as a user on a paid subscription; such pulls do not count.

## What counts

- A pull covers both a version check and any download that results; version checks do not count towards usage
  pricing.
- A pull of a normal image is one pull for a single manifest. A pull of a multi-arch image counts as one
  pull for each architecture.
- Limits per 6 hours (Docker Hub usage docs, 2026-10): unauthenticated 100 per IPv4 address or IPv6 /64
  subnet, Personal (authenticated) 200, Pro, Team and Business unlimited, all subject to fair use. Check the
  current table, because it changes.
- `docker-ratelimit-source` shows the IP or account the pull was attributed to.
- Separately, Docker Hub has an abuse rate limit on all requests (in the order of thousands per minute per
  IPv4 address or IPv6 /64) that applies to every account level.

## Fixes, in order

1. **Authenticate** every CI pull: `echo "$HUB_TOKEN" | docker login -u "$HUB_USER" --password-stdin`
   (use a personal or organization access token, not a password).
2. **Mirror / pull-through cache** (a `distribution` registry with `proxy.remoteurl`, Harbor proxy cache
   projects, ECR pull-through cache rules).
3. Copy base images you depend on into your own registry (`crane copy`) and reference those.
4. Cache images on runners (persistent builders).
5. Builds that pull base images need credentials in the environment that runs the build.

## Verify

Rerun the header check before and after a CI job to see consumption; after the fix,
`docker-ratelimit-source` is your account, or no limit headers appear at all.

## Checked

2026-10-26. Documentation release: docker/docs main (Docker Hub pull usage and limits, usage and limits pages), checked 2026-10-26. Confirmed: 6-hour window, 100 unauthenticated per IPv4 or IPv6 /64, 200 Personal, unlimited paid tiers, 429 response body, ratelimitpreview token and HEAD/GET header check and header names, HEAD not counting, absence of headers meaning unlimited or paid, multi-arch counting one pull per architecture, version checks not counted, abuse rate limit. Fixed: the old 429 message text, the claim that layer downloads are counted separately (the documentation defines pulls differently), and `ratelimit-source` (the header is `docker-ratelimit-source`). Removed unconfirmed claims: remote repositories on Artifact Registry, the `--pull missing` hint, and the buildx credential-reading detail.

Method: documentation only; no commands were run.
