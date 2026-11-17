---
id: computing-software.cloud-infrastructure-engineering.docker.swarm-raft-backup-autolock-and-ca-rotation
name: swarm-raft-backup-autolock-and-ca-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm, swarm-backup, raft-backup, force-new-cluster, autolock, unlock-key, ca-rotate, swarm-ca, disaster-recovery]
level: sme
description: "Back up and restore Swarm Raft state, recover from quorum loss with --force-new-cluster, protect keys with autolock, and rotate the Swarm root CA."
sources: ["https://docs.docker.com/engine/swarm/admin_guide/", "https://docs.docker.com/engine/swarm/swarm_manager_locking/", "https://docs.docker.com/engine/swarm/how-swarm-mode-works/pki/", "https://docs.docker.com/reference/cli/docker/swarm/ca/", "https://docs.docker.com/reference/cli/docker/swarm/unlock-key/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Swarm Raft backup, autolock and CA rotation

## Backup
State (services, secrets, configs, networks, node identities) lives in
`/var/lib/docker/swarm/` on every manager.
```sh
# on any manager; while it is stopped the swarm is more exposed to losing quorum (docs suggest 5 managers if you back up regularly)
docker swarm unlock-key -q > /secure/unlock-key   # if autolock is on - backup is useless without it
sudo systemctl stop docker
sudo tar -czpf /backup/swarm-$(hostname)-$(date +%F).tgz -C /var/lib/docker swarm
sudo systemctl start docker
```
The directory holds the keys that encrypt the Raft logs (without them the swarm cannot be restored) - store backups like secrets.

## Restore / disaster recovery
Quorum lost permanently (e.g. 2 of 3 managers gone):
```sh
# on a surviving manager
docker swarm init --force-new-cluster --advertise-addr 10.0.1.11
```
Keeps services/secrets/workers, makes this the sole manager; then promote new managers.
From backup onto a fresh host: stop docker, replace the contents of `/var/lib/docker/swarm` with the backup,
start docker, unlock the swarm if needed, `docker swarm init --force-new-cluster`. With autolock, rotate the unlock key afterwards.
Remove stale managers with `docker node demote/rm`.

## Autolock
```sh
docker swarm update --autolock=true      # prints SWMKEY-1-... - store it in a vault
docker swarm init --autolock             # at creation
docker swarm unlock                      # after a manager restart, prompts for the key
docker swarm unlock-key --rotate         # rotate; a manager that was down during rotation may need the previous key
```
Encrypts the Raft log and TLS keys at rest with the unlock key; a restarted manager stays
locked until someone unlocks it. Trade-off: automation must handle unlocks.

## CA rotation
```sh
docker swarm ca --rotate                              # new self-generated root CA
docker swarm ca --rotate --ca-cert new-ca.pem --ca-key new-ca-key.pem   # bring your own
docker swarm ca --rotate --external-ca protocol=cfssl,url=https://ca.example.com --ca-cert root.pem
docker swarm update --cert-expiry 720h                # node cert lifetime (default 90 days)
```
Rotation generates a cross-signed intermediate, tells every node to renew its certificate (this can take several minutes), then makes all nodes trust only the new CA. Rotate when the CA key may be compromised or a
manager backup leaked. The previous join tokens stop working - update automation.

## Verify
`docker swarm ca --rotate` prints the desired root digest and progress; `docker node ls`
all Ready after rotation; a locked manager answers `Swarm is encrypted and needs to be unlocked before it can be used`.

## Checked
2026-10-25, against docker/docs engine/swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: swarm state and Raft keys live in `/var/lib/docker/swarm/`; backup steps (stop Docker, copy the directory, restart) from any manager; restore steps and `--force-new-cluster`; autolock via `docker swarm init --autolock` and `docker swarm update --autolock=true`, `docker swarm unlock`, `docker swarm unlock-key -q/--rotate`; `docker swarm ca --rotate` with `--ca-cert`, `--ca-key`, `--external-ca` (only `cfssl` protocol) and `--cert-expiry` (default 2160h0m0s = 90 days); rotation steps and invalidated join tokens. Removed: engine-version match, node-ID retention, no-scheduling-while-locked wording, TLSInfo format string.
Method: documentation only; no commands were run.
