---
id: computing-software.collaboration-platform-administration.vikunja.hardening-network-and-privilege
name: hardening-network-and-privilege
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, tls-termination, bind-localhost, least-privilege, files-outside-install, security-checklist]
level: advanced
status: docs-checked
description: "Harden a Vikunja deployment's network exposure and privileges: TLS at the proxy, localhost or Unix socket binding, UID 1000, volumes, files and S3 access."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/security-hardening.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The hardening page's settings apply from Vikunja 2.7.0.

TLS and proxy: Vikunja serves plain HTTP by default, so terminate TLS at a reverse proxy. Only the proxy should reach Vikunja: bind to localhost with `service.interface` (default `:3456`), use `service.unixsocket` with `service.unixsocketmode`, or firewall the port. Set `service.publicurl` to the HTTPS URL; it builds email links and is the allowed CORS origin. Set `service.ipextractionmethod: xff` and list other proxies in `service.trustedproxies`; because private addresses are trusted, internal clients must not reach Vikunja directly.

```
service:
  publicurl: "https://tasks.example.org/"
  interface: "127.0.0.1:3456"
  ipextractionmethod: "xff"
  trustedproxies: "203.0.113.10/32"
```

Least privilege:
- Docker: the image is `FROM scratch`, no shell, runs as UID 1000; do not override it with root. Mount `/app/vikunja/files` and, for SQLite, `/db` as volumes owned by 1000.
- deb/rpm: run as a dedicated user with systemd sandboxing.
- Files: keep `files.basepath` outside the install directory, readable only by the Vikunja user. For S3 the bucket need not be public, since Vikunja serves attachments; scope the key to that bucket.

## Checked

2026-11-04. Confirmed against the Vikunja Security hardening page (setup/security-hardening): 2.7.0 availability, TLS and proxy settings and the example, ipextractionmethod and trustedproxies, Docker image facts, deb/rpm advice and the files and S3 guidance. Removed: the rootless Docker exception, which that page does not state.

Method: documentation only; no commands were run.
