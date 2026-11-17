---
id: computing-software.cloud-infrastructure-engineering.docker.deploying-distribution-registry-with-tls-auth-and-storage
name: deploying-distribution-registry-with-tls-auth-and-storage
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, private-registry, registry, distribution-deploy, registry-htpasswd, registry-s3-storage, registry-storage-backend, registry-auth]
level: advanced
description: "Run the CNCF distribution registry (registry:2/3) with TLS, htpasswd auth and a filesystem, S3 or GCS storage driver, configured by config.yml or env vars."
sources: ["https://distribution.github.io/distribution/about/deploying/", "https://distribution.github.io/distribution/about/configuration/", "https://distribution.github.io/distribution/storage-drivers/s3/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deploying the distribution registry with TLS, htpasswd and storage

## Minimal secure deployment
```sh
mkdir -p auth certs data
docker run --rm --entrypoint htpasswd httpd:2 -Bbn ci 'S3cret!' > auth/htpasswd   # bcrypt required
# certs/domain.crt (full chain) and certs/domain.key for registry.example.com

docker run -d --name registry --restart unless-stopped -p 443:5000 \
  -v "$PWD/data:/var/lib/registry" -v "$PWD/certs:/certs:ro" -v "$PWD/auth:/auth:ro" \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:5000 \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  -e REGISTRY_AUTH=htpasswd -e REGISTRY_AUTH_HTPASSWD_REALM="Registry" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  -e REGISTRY_STORAGE_DELETE_ENABLED=true \
  registry:3
docker login registry.example.com
```
Any config key maps to an env var: `REGISTRY_` + path upper-cased with `_` separators.
The registry supports htpasswd credentials only in bcrypt format; omitting `-B` makes every authentication attempt fail. Use htpasswd only with TLS.

## config.yml with S3 storage
```yaml
version: 0.1
storage:
  s3:
    region: eu-west-1
    bucket: my-registry
    rootdirectory: /registry
    encrypt: true
  delete: { enabled: true }
  cache: { blobdescriptor: redis }
  redirect: { disable: false }     # default: redirect clients to the backend for blob content
redis: { addr: redis:6379 }
http:
  addr: :5000
  secret: <random, same on all replicas>
  headers: { X-Content-Type-Options: [nosniff] }
auth:
  htpasswd: { realm: Registry, path: /auth/htpasswd }
health:
  storagedriver: { enabled: true, interval: 10s, threshold: 3 }
```
Other drivers: `filesystem` (default, `rootdirectory`), `gcs`, `azure`, `inmemory` (tests).
IAM role / instance profile is used when `accesskey`/`secretkey` are omitted.

## Behind a reverse proxy
Terminate TLS at nginx or another proxy. The nginx recipe sets `client_max_body_size 0;`, a long
`proxy_read_timeout` (900 in the example) and adds the `Docker-Distribution-Api-Version: registry/2.0`
header on every `/v2/` response, including 4xx. Forward `X-Forwarded-Proto`, `X-Forwarded-For` and
`Host` correctly, or the registry redirects to internal hostnames or downgrades https to http.

## Gotchas
- Multiple replicas behind a load balancer MUST share the same `http.secret`. With a local volume each
  replica holds a different data set, so use a distributed driver such as S3 or a single replica.
- Plain HTTP registries require `insecure-registries` on every client daemon - use TLS.
- Deleting tags does not free space until garbage-collect runs.
- Check the release notes before moving between major versions (`registry:2` to `registry:3`).

## Verify
```sh
curl -u ci:'S3cret!' https://registry.example.com/v2/_catalog
docker push registry.example.com/test/alpine:3 && curl -u ci:... https://registry.example.com/v2/test/alpine/tags/list
```

## Checked

2026-10-26. Documentation release: distribution/distribution docs/content at main (registry:3 era), deploying, configuration, nginx recipe and S3 driver pages. Confirmed: htpasswd bcrypt-only rule and -B flag, REGISTRY_AUTH_* / REGISTRY_HTTP_TLS_* env style, registry:3 in the documented run commands, S3 accesskey/secretkey omitted to use IAM roles, s3 encrypt default false, health.storagedriver interval, shared http.secret for load-balanced registries, nginx client_max_body_size 0 and proxy_read_timeout, Docker-Distribution-Api-Version header and X-Forwarded headers. Removed unconfirmed claims: proxy_request_buffering, the silent rejection wording, the list of drivers dropped in v3.

Method: documentation only; no commands were run.
