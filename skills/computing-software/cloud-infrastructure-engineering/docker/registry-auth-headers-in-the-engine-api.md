---
id: computing-software.cloud-infrastructure-engineering.docker.registry-auth-headers-in-the-engine-api
name: registry-auth-headers-in-the-engine-api
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-api, x-registry-auth, x-registry-config, image-pull, curl-unix-socket, docker-sdk]
level: advanced
status: docs-checked
description: "Authenticate Engine API pulls, pushes and builds: X-Registry-Auth base64url JSON, identity tokens from POST /auth, X-Registry-Config for builds, and SDK equivalents."
sources: ["https://docs.docker.com/reference/api/engine/#authentication", "https://docs.docker.com/reference/api/engine/version/v1.47/#tag/Image/operation/ImageCreate", "https://docker-py.readthedocs.io/en/stable/images.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry auth headers in the Engine API

The daemon does not read your `~/.docker/config.json` for API calls; the client must send
credentials with each request that talks to a registry.

## X-Registry-Auth
Base64url-encoded JSON (RFC 4648 section 5), accepted on `POST /images/create` (pull),
`POST /images/{name}/push`, `POST /services/create`, `POST /services/{id}/update` and the plugin pull and
upgrade endpoints. `serveraddress` is a domain or IP without a protocol:
```bash
AUTH=$(printf '{"username":"%s","password":"%s","serveraddress":"%s"}' \
  "$REG_USER" "$REG_TOKEN" "reg.example.com" | base64 -w0 | tr '+/' '-_')
curl -s --unix-socket /var/run/docker.sock -H "X-Registry-Auth: $AUTH" \
  -X POST "http://localhost/v1.47/images/create?fromImage=reg.example.com/team/app&tag=1.4"
curl -s --unix-socket /var/run/docker.sock -H "X-Registry-Auth: $AUTH" \
  -X POST "http://localhost/v1.47/images/reg.example.com/team/app/push?tag=1.4"
```
If you already have an identity token from `POST /auth`, send `{"identitytoken":"<token>"}` in the same
header instead of username and password. For services, `registryAuthFrom` (`spec` or `previous-spec`) says
where to find credentials when `X-Registry-Auth` is not sent.

## X-Registry-Config (builds)
`POST /build` takes a base64-encoded JSON object of auth configurations for the registries a build may
refer to, keyed by registry URL:
```json
{ "reg.example.com": { "username": "u", "password": "p" },
  "https://index.docker.io/v1/": { "username": "u2", "password": "p2" } }
```
sent in the `X-Registry-Config` header.

## SDKs
```python
import docker
c = docker.from_env()
c.login(username="u", password=token, registry="reg.example.com")
c.images.pull("reg.example.com/team/app", tag="1.4", auth_config={"username": "u", "password": token})
c.images.push("reg.example.com/team/app", tag="1.4", auth_config={"username": "u", "password": token})
```
Go (moby client module): `client.ImagePullOptions{RegistryAuth: ...}` takes the base64 string, which
`authconfig.Encode(registry.AuthConfig{...})` produces (packages `github.com/moby/moby/api/pkg/authconfig`
and `github.com/moby/moby/api/types/registry`).

## Gotchas
- The header is base64url, not standard base64 (the shell example swaps `+/` for `-_`).
- Authentication for registries is handled client side: the daemon does not read `~/.docker/config.json`
  for API calls, so automation must fetch the secret itself.
- Never log request headers; they contain the password in reversible encoding.

## Checked

2026-10-26. Documentation release: moby/moby api/swagger.yaml (Engine API 1.57) and Go sources, docker/docker-py main, checked 2026-10-26. Confirmed: client-side registry authentication, X-Registry-Auth as base64url JSON with username, password and serveraddress (no protocol), identitytoken alternative, the endpoints taking the header (images/create, push, services create/update, plugins pull/upgrade), registryAuthFrom values, X-Registry-Config for builds, docker-py auth_config parameters and urlsafe encoding, Go client ImagePullOptions.RegistryAuth and authconfig.Encode. Removed unconfirmed claims: errors appearing inside HTTP 200 streams, some daemon versions rejecting standard base64, the login being cached on the SDK object, and the old Go helper name. The shell examples use API version v1.47 in the URL; the current specification is 1.57.

Method: documentation only; no commands were run.
