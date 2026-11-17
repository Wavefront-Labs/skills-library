---
id: computing-software.cloud-infrastructure-engineering.docker.highly-available-private-registry
name: highly-available-private-registry
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, private-registry, registry-ha, registry-redis-cache, load-balancer, object-storage, distribution]
level: advanced
status: docs-checked
description: "Run several distribution registry replicas behind a load balancer: shared object storage, common http.secret, redis blob cache, health checks, and GC without downtime."
sources: ["https://distribution.github.io/distribution/about/deploying/#load-balancing-considerations", "https://distribution.github.io/distribution/about/configuration/#redis", "https://distribution.github.io/distribution/about/garbage-collection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Highly available private registry

The registry is stateless if its storage is shared. HA = N replicas, one object store,
identical config.

## Requirements (from the distribution load-balancing notes)
- Same `storage` backend for all replicas. The deploying guide notes that with a distributed driver such
  as S3 every worker can write without conflicts, while local volumes give each replica its own data set.
- Same `http.secret` everywhere: it signs state stored with the client, and registries behind a load balancer MUST share it.
- Same auth configuration (htpasswd file or token issuer and its certs).
- Optional shared `redis` for the blob descriptor cache (`storage.cache.blobdescriptor: redis`);
  `inmemory` is the alternative.

## Layout
```text
clients -> L7/L4 load balancer (TLS) -> registry x3 -> S3 bucket
                                     \-> redis (blobdescriptor cache)
```
Load balancer settings:
- Health check: with auth enabled, treat a 401 from `/v2/` as healthy and anything else as down, so a
  misconfigured auth setup cannot expose an open registry. If the balancer cannot do that, check `/`, which
  always returns 200.
- No request body size limit and long timeouts for large layers: the nginx recipe uses
  `client_max_body_size 0;` and `proxy_read_timeout 900;`.
- Send correct `X-Forwarded-Proto`, `X-Forwarded-For` and `Host` headers, and set `http.host` to the
  externally reachable URL. Responses under `/v2/` must carry `Docker-Distribution-Api-Version: registry/2.0`.

## Compose/Swarm sketch
```yaml
services:
  registry:
    image: registry:3
    environment:
      REGISTRY_HTTP_SECRET: <same-random-value-on-all-replicas>
    configs:
      - source: registry_config
        target: /etc/distribution/config.yml   # storage.s3, storage.cache.blobdescriptor: redis, redis.addr
    deploy: { replicas: 3, update_config: { order: start-first } }
  redis:
    image: redis:7-alpine
```
Keep the storage, cache and redis settings in the mounted `config.yml` (see the distribution config skill)
rather than overriding whole sections with environment variables, which the documentation discourages.

## Garbage collection
`registry garbage-collect` must not run while pushes happen (it can delete blobs of
in-flight uploads). Set `storage.maintenance.readonly.enabled: true` and restart the replicas, run GC from
one instance, then re-enable writes. Schedule it in a maintenance window.

## Alternatives
For replication across sites, RBAC, scanning and quotas, Harbor (which wraps distribution) or
a cloud registry is usually cheaper than building it yourself.

## Verify
```bash
for i in 1 2 3; do curl -s -o /dev/null -w '%{http_code}\n' https://registry.example.com/v2/; done
docker push registry.example.com/test/alpine:ha && docker pull registry.example.com/test/alpine:ha
```

## Checked

2026-10-26. Documentation release: distribution/distribution docs/content at main (deploying, configuration, garbage-collection, nginx recipe). Confirmed: shared-storage guidance for replicated services, MUST-share http.secret for load-balanced registries, blobdescriptor redis/inmemory, health-check advice (401 healthy, "/" returns 200), nginx client_max_body_size 0 and proxy_read_timeout 900, X-Forwarded headers and Docker-Distribution-Api-Version header, maintenance readonly setting, GC stop-the-world warning. Removed unconfirmed claims: NFS as weakest option, proxy_request_buffering, sticky sessions not needed, REGISTRY_STORAGE and *_FILE environment forms, and the JSON-valued readonly env override.

Method: documentation only; no commands were run.
