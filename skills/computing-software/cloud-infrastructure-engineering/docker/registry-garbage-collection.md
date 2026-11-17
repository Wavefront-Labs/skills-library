---
id: computing-software.cloud-infrastructure-engineering.docker.registry-garbage-collection
name: registry-garbage-collection
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, garbage-collection, registry-garbage-collect, delete-untagged, private-registry, image-lifecycle, retention]
level: advanced
description: "Free storage in a self-hosted distribution registry: delete manifests via the API, then run registry garbage-collect --delete-untagged in read-only mode."
sources: ["https://distribution.github.io/distribution/about/garbage-collection/", "https://distribution.github.io/distribution/spec/api/#deleting-an-image", "https://goharbor.io/docs/main/administration/garbage-collection/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Registry garbage collection

Deleting a tag in a registry frees nothing: blobs remain until a GC pass finds them
unreferenced.

## 1. Delete manifests
Requires `storage.delete.enabled: true`. Deletion is by **digest**:
```sh
REG=https://registry.example.com; REPO=team/api; TAG=old
DIGEST=$(curl -sI -u ci:pass \
  -H 'Accept: application/vnd.oci.image.index.v1+json, application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.list.v2+json, application/vnd.docker.distribution.manifest.v2+json' \
  "$REG/v2/$REPO/manifests/$TAG" | awk -F': ' 'tolower($1)=="docker-content-digest"{print $2}' | tr -d '\r')
curl -u ci:pass -X DELETE "$REG/v2/$REPO/manifests/$DIGEST"      # 202 Accepted
# or: crane delete registry.example.com/team/api@$DIGEST
```
Send an `Accept` header listing the manifest types you expect; the `Docker-Content-Digest` header carries the digest.
Deleting a digest removes **every tag** pointing to it.

## 2. Garbage collect
```sh
# stop writes first: set storage.maintenance.readonly.enabled to true and restart the registry, or stop it
# usage: registry garbage-collect [--dry-run] [--delete-untagged] [--quiet] /path/to/config.yml
docker exec registry registry garbage-collect --dry-run /etc/distribution/config.yml
docker exec registry registry garbage-collect --delete-untagged /etc/distribution/config.yml
```
- `--delete-untagged` deletes manifests that are not referenced by a tag; `--quiet` suppresses output.
- GC is stop-the-world mark and sweep: uploading an image while it runs risks deleting its layers and
  corrupting the image. Run with the registry read-only or stopped. The `readonly` maintenance
  setting exists for this purpose.

## Untagged multi-arch caveat
The distribution documentation describes `--delete-untagged` only as deleting manifests not referenced
by a tag. Run `--dry-run` first and verify a multi-arch pull afterwards.

## Harbor / cloud
Harbor: Administration -> Clean Up -> Garbage Collection (workers, "Allow garbage collection on
untagged artifacts", DRY RUN, GC Now, schedule none/hourly/daily/weekly/custom cron). Harbor runs GC
without interrupting push and pull, and skips blobs and manifests newer than a 2 hour window; GC Now
is limited to once per minute. Managed cloud registries have their own lifecycle policies.

## Verify
`du -sh` of the storage root (or bucket size metric) drops; `crane ls` shows remaining tags;
pull a few remaining images including multi-arch ones.

## Checked

2026-10-26. Documentation release: distribution/distribution docs/content at main (garbage-collection, configuration and API pages) and Harbor website docs main (updated 2026-10-15). Confirmed: garbage-collect command, --dry-run, --delete-untagged and --quiet flags, stop-the-world warning, maintenance readonly setting, DELETE manifest returns 202, Docker-Content-Digest header, config path /etc/distribution/config.yml, and the Harbor GC page options, schedule choices, 2 hour window and once-per-minute limit. Removed unconfirmed claims: the -m short flag, S3 sweep duration, the historical multi-arch deletion claim, wrong-Accept 404 behaviour, and the /etc/docker/registry config path.

Method: documentation only; no commands were run.
