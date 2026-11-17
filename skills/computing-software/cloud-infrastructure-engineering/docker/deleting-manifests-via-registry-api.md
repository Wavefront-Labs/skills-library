---
id: computing-software.cloud-infrastructure-engineering.docker.deleting-manifests-via-registry-api
name: deleting-manifests-via-registry-api
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, registry, crane-delete, regctl, registry-api, image-lifecycle, distribution-spec]
level: advanced
status: docs-checked
description: "Delete tags and manifests from an OCI registry: digest-only DELETE semantics, crane delete, regctl tag rm and manifest rm, scripting by age, and following up with GC."
sources: ["https://github.com/opencontainers/distribution-spec/blob/main/spec.md#deleting-manifests", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_delete.md", "https://github.com/regclient/regclient/blob/main/docs/regctl.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deleting manifests via the registry API

`docker` has no command to delete remote images. The distribution API does, with caveats.

## API semantics
- `DELETE /v2/<name>/manifests/<digest>` deletes a manifest **by digest**. Every tag pointing
  at it goes too.
- The OCI distribution spec defines tag deletion (`DELETE /v2/<name>/manifests/<tag>`, 202 on success)
  and manifest deletion by digest. If deletion is disabled the registry answers 400 or 405. The
  distribution registry's own API reference says a manifest can only be deleted by digest, so
  registry-specific behaviour for tag deletion varies.
- The distribution registry has `storage.delete.enabled` default to false; enable it before deleting.
- Blobs are not freed until registry garbage collection runs.

## crane
```bash
crane digest reg.example.com/team/app:pr-123            # resolve the tag
crane delete reg.example.com/team/app@sha256:<digest>   # delete the manifest
crane ls reg.example.com/team/app                        # list tags
```

## regctl
```bash
regctl tag ls reg.example.com/team/app
regctl tag rm reg.example.com/team/app:pr-123            # tag delete API, or dummy-manifest workaround
regctl manifest rm reg.example.com/team/app@sha256:<digest>
regctl manifest rm --referrers reg.example.com/team/app@sha256:<digest>   # check for referrers (signatures, SBOMs)
```
`regctl tag delete` (aliases `rm`, `del`, `remove`) removes a tag: it uses the OCI tag delete API and,
for registries without it, a dummy-manifest workaround; if the registry has no delete API the dummy
manifest remains. `regctl manifest delete` takes `--referrers` to check for referrers, recommended when deleting artifacts.

## Scripted cleanup by pattern
```bash
for t in $(crane ls reg.example.com/team/app | grep -E '^pr-[0-9]+$'); do
  d=$(crane digest "reg.example.com/team/app:$t")
  # skip if another kept tag shares the digest
  if crane ls reg.example.com/team/app | grep -vE '^pr-' | while read k; do
       [ "$(crane digest reg.example.com/team/app:$k)" = "$d" ] && echo keep; done | grep -q keep; then
    continue
  fi
  echo "deleting $t $d"; crane delete "reg.example.com/team/app@$d"
done
```
The tag list endpoint returns tag names only, with no timestamps; for age-based cleanup read the image
config `created` field (`crane config`) or use registry-native retention.

## Gotchas
- A multi-arch index references child manifests; deleting a child while the index remains breaks
  pulls for that platform, so delete the index and its children together.
- Cloud registries (ECR, GAR, ACR) have their own CLIs and lifecycle policies that are safer
  than raw API deletes.

## Checked

2026-10-26. Documentation release: OCI distribution-spec main (spec.md end-9), distribution/distribution API reference, regclient source (cmd/regctl tag.go and manifest.go) and go-containerregistry crane docs. Confirmed: 202 on delete, 400/405 when deletion is disabled, distribution API note that a manifest can only be deleted by digest, delete.enabled default false, crane delete/digest/ls/config commands, regctl tag delete aliases and the dummy-manifest fallback, regctl manifest delete --referrers. Removed unconfirmed claims: UNSUPPORTED being returned for tag deletes, the 405 wording for the distribution registry, timestamps being unreliable, child-manifest GC behaviour, and the jq pipeline.

Method: documentation only; no commands were run.
