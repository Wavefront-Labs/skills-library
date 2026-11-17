---
id: computing-software.cloud-infrastructure-engineering.docker.distribution-registry-config-yml
name: distribution-registry-config-yml
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, private-registry, registry-config-yml, distribution, registry-storage-backend, registry-middleware, redirect]
level: advanced
status: docs-checked
description: "Configure the CNCF distribution registry via config.yml: http, storage (delete, redirect, maintenance), auth, middleware, health, and REGISTRY_* env overrides."
sources: ["https://distribution.github.io/distribution/about/configuration/", "https://distribution.github.io/distribution/about/deploying/", "https://distribution.github.io/distribution/storage-drivers/s3/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# distribution registry config.yml

The configuration reference documents mounting a file at `/etc/distribution/config.yml` in the
`registry:3` container. Every key can be overridden by an environment variable:
`REGISTRY_` plus the key path upper-cased with `_` separators, so `storage.s3.bucket` becomes
`REGISTRY_STORAGE_S3_BUCKET`. The documentation recommends env overrides for individual values
only, not for whole sections.

## Production-shaped config
```yaml
version: 0.1
log:
  level: info
  formatter: json
  accesslog: { disabled: false }
http:
  addr: :5000
  host: https://registry.example.com      # externally reachable URL, used when generating URLs
  secret: <random-shared-secret>          # signs client-held state; same on all replicas
  relativeurls: false
  headers:
    X-Content-Type-Options: [nosniff]
  debug:
    addr: localhost:5001                  # debug server; Prometheus metrics are served here
    prometheus: { enabled: true, path: /metrics }
storage:
  s3:
    region: eu-west-1
    bucket: example-registry
    rootdirectory: /registry
    encrypt: true
  delete:
    enabled: true                         # allow manifest DELETE (needed for cleanup + GC)
  redirect:
    disable: false                        # clients fetch blobs straight from S3 presigned URLs
  maintenance:
    uploadpurging: { enabled: true, age: 168h, interval: 24h, dryrun: false }
  cache:
    blobdescriptor: redis
redis:
  addr: redis:6379
auth:
  htpasswd:
    realm: Registry
    path: /auth/htpasswd
health:
  storagedriver: { enabled: true, interval: 10s, threshold: 3 }
```

## Key decisions
- **redirect**: enabled by default for backends that support it, so clients are redirected to the
  backend for blob content; set `disable: true` to route all data through the registry (for example
  when the backend is not co-located or clients cannot reach it).
- **delete.enabled**: off by default; without it nothing can ever be cleaned up.
- **http.secret**: random data that signs state stored with the client. If you omit it the registry
  generates one at start, so registries behind a load balancer MUST share the same value.
- **TLS**: terminate at the registry (`http.tls.certificate/key`) or at a proxy; with a proxy
  send correct `X-Forwarded-Proto`, `X-Forwarded-For` and `Host` headers and set `http.host`,
  otherwise redirects can point at internal hostnames or downgrade to http.
- **middleware.storage: cloudfront** to serve blobs through a CDN.

## Run
```bash
docker run -d --name registry -p 5000:5000 \
  -v $PWD/config.yml:/etc/distribution/config.yml:ro \
  -v $PWD/auth:/auth:ro \
  -e REGISTRY_STORAGE_S3_ACCESSKEY -e REGISTRY_STORAGE_S3_SECRETKEY \
  registry:3
```

## Verify
```bash
curl -s -u user:pass https://registry.example.com/v2/_catalog
curl -s localhost:5001/metrics | head
docker logs registry
```

## Gotchas
- Changing `rootdirectory` after data exists makes the registry look empty.

## Checked

2026-10-26. Documentation release: distribution/distribution docs/content at main (registry:3 era), configuration, deploying and S3 driver pages. Confirmed: mount path /etc/distribution/config.yml, REGISTRY_ env override rule and its caution, http.secret and http.host semantics, X-Forwarded headers advice, redirect default and the disable flag, delete.enabled default false, uploadpurging defaults (enabled, 168h, 24h, dryrun false), cache.blobdescriptor values, prometheus enabled/path under http.debug, health.storagedriver interval default 10s. Removed unconfirmed claims: registry:2 default config path, the `blob upload invalid` error text, a specific metric name, a jq log filter, and pprof on the debug port.

Method: documentation only; no commands were run.
