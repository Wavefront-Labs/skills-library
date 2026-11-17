---
id: computing-software.cloud-infrastructure-engineering.zot.docker-client-mixed-access
name: docker-client-mixed-access
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, docker-login, mixed-access, anonymous-policy, www-authenticate, zot-docker-proxy]
level: advanced
status: docs-checked
description: "Why Docker clients must log in when a Zot has both anonymous and authenticated repositories, and the four workarounds the docs recommend."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
How Docker decides: a `200 OK` on `/v2/` means send no credentials; a `401` with `WWW-Authenticate` means send stored credentials from a prior `docker login`.

With basic auth (htpasswd or LDAP) enabled, Zot detects Docker via `Docker-Client` in the `User-Agent`:
- Mixed access control (at least one anonymous repository policy plus authenticated-only rules): `/v2/` returns `401` with `WWW-Authenticate: Basic`, so Docker users must `docker login` even for public repos.
- Anonymous-only: `/v2/` returns `200` without credentials.
- Podman and other OCI clients are unaffected.

Workarounds:
1. `docker login` with an API key (recommended): `echo "<api-key>" | docker login myreg.example.com -u <username> --password-stdin`
2. Use Podman or skopeo, for example `skopeo copy docker://myreg.example.com/public-repo/image:tag dir:/tmp/image`.
3. Put the zot-docker-proxy project in front of Zot.
4. Avoid mixed policies: no `anonymousPolicy`, or separate public and private Zot instances.

Docker also needs HTTPS for remote registries; `insecure-registries` in `/etc/docker/daemon.json` is for local testing only.

## Checked

2026-11-04. Read against the zot Docker users guide and authn-authz article; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
