---
id: computing-software.systems-network-administration.kopia.kopia-docker-and-installation
name: kopia-docker-and-installation
category: computing-software
field: systems-network-administration
product: kopia
tags: [docker, installation, kopia-ui, apt, rpm, homebrew, container]
level: practitioner
status: docs-checked
description: "Install Kopia on common platforms and run it in Docker, including mounts, tags and server mode."
sources: ["https://kopia.io/docs/installation/", "https://kopia.io/docs/faqs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kopia has two variants, the CLI and KopiaUI (GUI), and is available for Windows, macOS (Homebrew or installer), Debian and Ubuntu (APT), Red Hat family (RPM), Arch (AUR), OpenBSD and FreeBSD ports, Docker, or by compiling from source. Release packages can be verified with the integrity instructions on the page.

## Docker

Images exist for amd64, arm64 and arm with tags `latest` (stable), `testing` (stable or pre-release), `unstable` (nightly), `major.minor` and `major.minor.patch`.

A container needs:

- the repository password in the `KOPIA_PASSWORD` environment variable
- `/app/config` mounted, where `repository.config` lives
- `/app/cache` mounted (recommended) for the cache
- `/app/logs` mounted (optional)
- `/app/rclone` mounted only when using the rclone provider, holding `rclone.conf`
- any directory used by a local repository
- `/tmp` mounted with the `:shared` property to browse mounted snapshots from the host

```console
docker run -e KOPIA_PASSWORD -v /path/to/config/dir:/app/config -v /path/to/cache/dir:/app/cache -v /path/to/logs/dir:/app/logs -v /path/to/repository/dir:/repository -v /path/to/tmp/dir:/tmp:shared kopia/kopia:latest
```

For the web interface run it in server mode, for example with Compose command arguments `server start --address=0.0.0.0:51515 --server-username=USERNAME --server-password=SECRET`, then browse port 51515. Behind nginx use `grpc_pass grpcs://container_ip:container_port` instead of `proxy_pass`.

## KopiaUI configs

KopiaUI reads every `*.config` file in Kopia's config directory and tries to connect to all of them. It always looks for `repository.config`. Rename test configs to a different extension so they are ignored.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Installation (platform list, Docker tags and architectures, required mounts, KOPIA_PASSWORD, :shared /tmp, grpc_pass note, compose server command) and FAQ (KopiaUI reads every *.config file, always looks for repository.config).
Method: documentation only; no commands were run.
