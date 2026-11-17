---
id: computing-software.systems-network-administration.immich.system-requirements
name: system-requirements
category: computing-software
field: systems-network-administration
product: immich
tags: [requirements, ram, docker-compose, ssd, wsl]
level: intro
status: docs-checked
description: "Hardware and software requirements for Immich: RAM, CPU, storage, Postgres on local SSD, Docker Compose plugin, and Windows database storage caveats."
sources:
  - https://docs.immich.app/install/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: size and prepare a host for Immich.

Hardware:

- OS: 64-bit Linux or similar recommended. Windows needs Docker Desktop or WSL 2, macOS needs Docker Desktop; both get weaker support. A full virtual machine works well; Docker inside LXC containers is not recommended.
- RAM: minimum 6GB, recommended 8GB. With only 4GB, run with machine learning disabled.
- CPU: minimum 2 cores, recommended 4. Platforms `amd64` and `arm64`. The machine learning container on `amd64` needs the `x86-64-v2` microarchitecture or newer (since v3); in a VM select a supported CPU type. The last version supporting x86-64-v1 is v2.7.5, which is no longer supported.
- Storage: a Unix-compatible filesystem (EXT4, ZFS, APFS) with user/group ownership. Thumbnails and transcoded video add about 10-20% to library size.

Postgres: files are typically 1-3 GB. Put `DB_DATA_LOCATION` on local SSD, never a network share. If Docker resource limits are set, give the database at least 2GB RAM.

Software: Docker Engine or Docker Desktop with the Compose plugin. The command must be `docker compose`; `docker-compose` is not supported.

Windows: the database location must be on a filesystem with Unix ownership and permissions. NTFS and FAT variants do not work, nor does a WSL-mounted host directory under `/mnt`. Switch to a Docker volume:

```diff
- DB_DATA_LOCATION=./postgres
+ DB_DATA_LOCATION=pgdata
```

and add `pgdata:` under `volumes:` at the bottom of `docker-compose.yml`, next to `model-cache:`.

## Checked

2026-11-09: read https://docs.immich.app/install/requirements in full; hardware, Postgres, software and Windows sections match. Added the page's v3 and v2.7.5 note on x86-64-v2.

Method: documentation only; no commands were run.
