---
id: computing-software.cloud-infrastructure-engineering.docker.remote-daemon-tls-ssh-and-contexts
name: remote-daemon-tls-ssh-and-contexts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-context, remote-daemon, daemon-tls, docker-host, contexts, ssh, tcp-2376, tlsverify, client-certificates, docker-machine, remote-docker]
level: advanced
status: docs-checked
description: "Driving a remote Docker daemon safely: docker context over SSH (default), TLS client-cert setup on tcp://:2376 when SSH is not an option, DOCKER_HOST precedence, and the never-expose-2375 rule."
sources: ["https://docs.docker.com/engine/security/protect-access/", "https://docs.docker.com/engine/manage-resources/contexts/", "https://docs.docker.com/engine/daemon/remote-access/", "https://docs.docker.com/engine/daemon/troubleshoot/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote daemon access: SSH contexts and TLS

**Goal:** run `docker`/`compose` commands against a server from your laptop or CI without
opening an unauthenticated root-equivalent port to the world.

## Rule zero
A daemon on `tcp://0.0.0.0:2375` with no TLS is unauthenticated root on that host (anyone
who can reach it can `docker run -v /:/host --privileged`). Docker says remote access without TLS is not recommended. Do not do it, not even "temporarily behind a firewall".

## Option 1 (default): SSH context
Needs only: SSH access to a user in the `docker` group, and `docker` installed remotely.
```bash
docker context create prod --docker "host=ssh://deploy@prod.example.com"
docker context use prod
docker ps                               # runs on prod
docker --context prod compose up -d     # per-command override (--context is a global CLI flag)
docker context use default
```
- Nothing to open on the server; auth is your SSH key; the socket is forwarded per command.
- Docker's recommended `~/.ssh/config` lines reuse one SSH connection across `docker` invocations: `ControlMaster auto`, `ControlPath ~/.ssh/control-%C`, `ControlPersist yes`.
- The remote user must be able to talk to the daemon socket without `sudo`, which normally means membership of the `docker` group (root-equivalent; see the Docker post-install notes).
- For a one-off connection without a context, `export DOCKER_HOST=ssh://deploy@prod.example.com`.

## Option 2: TLS on tcp://:2376 (CI runners, Windows hosts without SSH, tooling that needs a URL)
Generate a CA, a server cert (`subjectAltName` = the DNS name or IP clients will use, `extendedKeyUsage = serverAuth`), and a client cert
(`extendedKeyUsage = clientAuth`), following Docker's OpenSSL walkthrough. Then `daemon.json`:
```json
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"],
  "tlsverify": true,
  "tlscacert": "/etc/docker/certs/ca.pem",
  "tlscert": "/etc/docker/certs/server-cert.pem",
  "tlskey": "/etc/docker/certs/server-key.pem"
}
```
On systemd installs, `hosts` in `daemon.json` conflicts with the `-H fd://` in the unit
file (`unable to configure the Docker daemon with file ... hosts: (from flag: [fd://], from
file: [...])`). Fix with a drop-in:
```
# /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd
```
then `systemctl daemon-reload && systemctl restart docker`.

Client:
```bash
docker context create prod-tls --docker \
  "host=tcp://prod.example.com:2376,ca=~/.docker/prod/ca.pem,cert=~/.docker/prod/cert.pem,key=~/.docker/prod/key.pem"
# or the env form (expects ca.pem, cert.pem, key.pem in DOCKER_CERT_PATH):
export DOCKER_HOST=tcp://prod.example.com:2376 DOCKER_TLS_VERIFY=1 DOCKER_CERT_PATH=~/.docker/prod
```
With only `tls`, `tlscert` and `tlskey` (no `tlsverify`) the server does not authenticate clients. Use `tlsverify` with `tlscacert`.

## Precedence
The `--context` flag wins; `-H`/`--host` or `DOCKER_HOST` selects the default context with that host (so it overrides a context set with `docker context use`, and `docker context ls` warns); `--context` together with `--host` is an error. `docker context ls` shows which context is active (`*`); `docker context inspect` shows the endpoint. Contexts are stored in
`~/.docker/contexts/`; `docker context export prod` writes a tar archive of one context, so treat the file as sensitive.

## Verify
```bash
docker --context prod info --format '{{.Name}} {{.ServerVersion}}'   # remote hostname
ss -ltnp | grep 237                       # on the server: 2376 only (never 2375)
curl -sk https://prod.example.com:2376/_ping   # should fail without a client certificate when tlsverify is set
```

## Checked

Checked against docker/docs `engine/security/protect-access.md`, `engine/manage-resources/contexts.md`, `engine/daemon/remote-access.md`, `engine/daemon/troubleshoot.md`, docker/cli `cli/command/cli.go` and `cli/command/context/options.go` (docker/docs latest commit 2026-10-23, Engine 29).

- SSH context creation and use, the recommended `ControlMaster`/`ControlPath`/`ControlPersist` lines, `DOCKER_HOST=ssh://...`.
- TLS combinations for server and client (`tlsverify`, `tlscacert`, `tls`, `tlscert`, `tlskey`), `serverAuth` and `clientAuth` extended key usage, `subjectAltName`, `DOCKER_CERT_PATH` and `DOCKER_TLS_VERIFY`, port 2376.
- Context `--docker` keys `host`, `ca`, `cert`, `key` (and `skip-tls-verify`) exist in the CLI source; the `hosts` conflict and `ExecStart=` override match the troubleshooting page. Precedence per the CLI source.
- Removed as unconfirmed: custom SSH ports, Windows OpenSSH agent notes, remote PATH requirement, the Kubernetes endpoint remark and the Compose/buildx remote-build section.

Method: documentation only; no commands were run.
