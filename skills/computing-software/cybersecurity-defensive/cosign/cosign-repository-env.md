---
id: computing-software.cybersecurity-defensive.cosign.cosign-repository-env
name: cosign-repository-env
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, cosign-repository, artifact-registry, gcr, separate-repository]
level: practitioner
status: docs-checked
description: "Store cosign signatures in a different repository with COSIGN_REPOSITORY, including the Artifact Registry format gotcha."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# COSIGN_REPOSITORY

By default signatures go in the same repo as the image. To use another:

```
export COSIGN_REPOSITORY=gcr.io/my-new-repo
cosign sign --key cosign.key $IMAGE_URI_DIGEST
```

This replaces the repository part, so the signature for `gcr.io/dlorenc-vmtest2/demo` is stored at `gcr.io/my-new-repo/demo:sha256-DIGEST.sig`.

Registry formats differ:
- GCR: a registry name like `gcr.io/$REPO` is enough.
- Artifact Registry: specify a full image name `$LOCATION-docker.pkg.dev/$PROJECT/$REPO/$STORAGE_IMAGE`, for example `us-docker.pkg.dev/my-new-repo/demo`. Just `$LOCATION-docker.pkg.dev/$PROJECT/$REPO` "will not work".

`cosign triangulate <IMAGE>` appears in the README counter-signing example; `cosign tree <IMAGE>` lists the signatures, SBOMs and attestations of an image.

## Checked

2026-11-04. Confirmed in the cosign README (Specifying Registry section): the default of the same repo as the image, the COSIGN_REPOSITORY replacement example and resulting tag, the GCR and Artifact Registry formats and the "will not work" warning; and in the cosign tree reference page. Removed: advice to set the variable when verifying, the use-case bullets and the claim that these commands show where a signature is stored (none on the pages).

Method: documentation only; no commands were run.
