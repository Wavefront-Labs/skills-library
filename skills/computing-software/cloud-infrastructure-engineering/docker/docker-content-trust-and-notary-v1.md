---
id: computing-software.cloud-infrastructure-engineering.docker.docker-content-trust-and-notary-v1
name: docker-content-trust-and-notary-v1
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, content-trust, dct, docker-content-trust-env, notary-v1, docker-trust, image-signing]
level: advanced
description: "Use or retire Docker Content Trust: DOCKER_CONTENT_TRUST=1, docker trust sign and key roles in Notary v1, its limitations, and migrating to cosign or Notation."
sources: ["https://docs.docker.com/engine/security/trust/", "https://docs.docker.com/reference/cli/docker/trust/sign/", "https://docs.docker.com/engine/security/trust/trust_key_mng/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker Content Trust (DCT) and Notary v1

DCT signs **tags** using The Update Framework via a Notary v1 server. It is legacy: Docker
Docker is retiring it: the Notary v1 service at `notary.docker.io` shuts down completely on
December 8, 2026. Know DCT to operate existing setups and to migrate to Cosign or Notation.

## Client-side enforcement
```sh
export DOCKER_CONTENT_TRUST=1
docker pull nginx:1.27            # fails if the tag has no trust data
docker build .                    # FROM lines must be signed too
export DOCKER_CONTENT_TRUST_SERVER=https://notary.example.com:4443
```
DCT is off by default in the Docker client. With it on, the commands that operate on tagged images
(`push`, `build`, `create`, `pull`, `run`) need signed content; `docker push` signs, and
`--disable-content-trust` bypasses it per command. A pull by explicit digest always succeeds if the digest
exists. Enforcement is **client-side**: a host without the env var is not restricted.

## Signing
```sh
docker trust key generate alice                     # delegation key -> alice.pub
docker trust signer add --key alice.pub alice registry.example.com/app
docker trust sign registry.example.com/app:1.4.0
docker trust inspect --pretty registry.example.com/app:1.4.0
docker trust revoke registry.example.com/app:1.4.0
```
Key roles: **root** (offline key, created once), **targets** (repository key, signs tags and manages
delegations), **snapshot**, **timestamp** (generated at first push and held in the signing server), and
optional **delegation** keys. Local keys are kept under `~/.docker/trust/private`. The root key, once
lost, is not recoverable.
Passphrases via `DOCKER_CONTENT_TRUST_ROOT_PASSPHRASE` / `DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE`.

## Daemon-side enforcement
Enforcement is a client setting (`DOCKER_CONTENT_TRUST=1` in the CLI environment), not a daemon policy.
For cluster-wide enforcement use an admission controller with Cosign or Notation verification.

## Limitations driving migration
- Signs tags (DCT is associated with the tag portion of an image), and a registry needs an attached
  Notary server.
- Modern replacements named by Docker: **Sigstore/Cosign** and **Notation** (Notary Project; X.509).
  Both store signatures as OCI artifacts next to the image.

## Migration outline
1. Start signing with cosign/Notation in CI alongside DCT.
2. Move enforcement to an admission controller that verifies Cosign or Notation signatures.
3. Remove `DOCKER_CONTENT_TRUST=1` from CI once new verification is enforced; archive root keys.

## Verify
`docker trust inspect` lists signers for current tags; with `DOCKER_CONTENT_TRUST=1`, pulling
an unsigned tag fails with `remote trust data does not exist for <repository>`.

## Checked

2026-10-26. Documentation release: docker/docs main (engine/security/trust pages and manuals/retired.md), checked 2026-10-26. Confirmed: retirement notice and the December 8, 2026 shutdown of notary.docker.io, DCT disabled by default, the five commands that use DCT, digest pulls bypass trust data, key roles and the unrecoverable root key, DOCKER_CONTENT_TRUST_SERVER, DOCKER_CONTENT_TRUST_ROOT_PASSPHRASE and DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE, the docker trust key generate / signer add / inspect flow, --disable-content-trust on pull and push, trust keys under ~/.docker/trust/private, and the documented pull error text. Removed unconfirmed claims: Swarm having no enforcement option, named admission projects, the `No valid trust data` message, and the OCI-native criticisms.

Method: documentation only; no commands were run.
