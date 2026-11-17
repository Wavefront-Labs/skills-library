---
id: computing-software.cloud-infrastructure-engineering.podman.system-service-api-security
name: system-service-api-security
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [system-service, api-security, mutual-tls, tls-client-ca, cors, unix-socket, ssh-forwarding]
level: advanced
status: docs-checked
description: "Secure the Podman API socket: code-execution risk, file permissions, TLS client certificates, --cors, SSH forwarding and in-container access."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-system-service.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose the API without handing out root-equivalent access.

The API grants full access to all Podman functionality and so allows arbitrary code execution as the user running it, with no ability to limit or audit. Its security model relies on a Unix socket restricted by standard file permissions so only the service's user can reach it.

TLS can secure it by requiring client certificates signed by a trusted CA and letting clients verify the server: `--tls-cert=path` (PEM certificate, requires `--tls-key`), `--tls-key=path` (matching private key, requires `--tls-cert`), and `--tls-client-ca=path` (PEM bundle to validate clients; connections with no certificate or one not signed by the bundle are rejected).

The page strongly recommends against exposing the socket over the network (a `tcp` URL) without mutual TLS, and warns that even localhost carries risk because anyone with access to the system can reach the API. If remote access is needed, forward the socket over SSH and limit access on the remote machine. If a `tcp` URL must be used without TLS, `--cors` is recommended; it sets CORS headers on responses (empty by default, which disables them).

To reach the socket inside a container, mount it as a volume and run the container with `--security-opt label=disable`. The default timeout can be changed with `service_timeout=VALUE` in containers.conf.

## Checked
2026-11-09: read the podman-system-service man page in full and confirmed the Security section, the --tls-cert, --tls-key, --tls-client-ca and --cors descriptions, the in-container access steps and the service_timeout setting. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
