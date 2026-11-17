---
id: computing-software.cloud-infrastructure-engineering.docker.docker-socket-root-equivalence
name: docker-socket-root-equivalence
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-socket, docker-sock-ro, docker-sock-permissions, docker-group, privilege-escalation, socket-exposure]
level: advanced
status: docs-checked
description: "Why access to docker.sock (or the docker group) equals root on the host, why mounting it :ro does not help, and the real mitigations: proxies, rootless, authz, no socket at all."
sources: ["https://docs.docker.com/engine/install/linux-postinstall/", "https://docs.docker.com/reference/cli/dockerd/", "https://docs.docker.com/engine/security/", "https://docs.docker.com/engine/security/protect-access/", "https://docs.docker.com/engine/security/rootless/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docker.sock is root

## Why it is root
The Docker daemon always runs as root, and the Docker security page notes it allows sharing a host
directory with a container without limiting the container's access. The `dockerd` reference and the
protect-access page both warn that access to the daemon gives root access to the host. No exploit is
involved; it is the API working as designed.

## Who has that access
- Members of the `docker` group: the daemon creates a Unix socket accessible by that group, and Docker's
  post-install docs warn that the group grants root-level privileges.
- Every container that bind-mounts the daemon socket (for example
  `-v /var/run/docker.sock:/var/run/docker.sock`), such as CI agents and management tools.
- Anyone reaching a TCP API without TLS client authentication.

## Mitigations
| Mitigation | Effect |
|---|---|
| Do not mount the socket | Prefer tools that have a non-socket mode |
| Rootless Docker | The daemon runs as an unprivileged user, so socket access is not host root |
| Authorization plugin (OPA) | Deny privileged, host mounts, host namespaces per request (see `docker-authorization-plugins-with-opa`) |
| TLS client authentication on any TCP API | Only holders of a trusted client certificate can connect |
| Separate daemon / VM for CI builds | Blast radius limited to a disposable host |

## Group hygiene
The post-install page offers password-protected, on-demand access to the `docker` group instead of
permanent membership, and notes that a group password reduces ambient access to the socket but does not
reduce the root-level privileges granted once access is authorized. Review who is in the group regularly.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main) post-install Linux page, `dockerd` reference, Docker security page, protect-access page, Rootless page.
- Confirmed the Docker daemon always runs as root, the `docker` group warning ("grants root-level privileges"), the `dockerd` and protect-access warnings that daemon access means root access on the host, the security page statement about sharing a host directory without limiting access, Rootless mode as the documented alternative, TLS client authentication for the TCP API, and authorization plugins.
- Removed the container-escape one-liner, the read-only socket mount claim (no checked source covers it), named third-party tools and proxy settings, `gpasswd`/`getent` commands and the Desktop and Podman remarks.
Method: documentation only; no commands were run.
