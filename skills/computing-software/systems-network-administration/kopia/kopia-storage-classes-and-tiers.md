---
id: computing-software.systems-network-administration.kopia.kopia-storage-classes-and-tiers
name: kopia-storage-classes-and-tiers
category: computing-software
field: systems-network-administration
product: kopia
tags: [storage-class, glacier, cold-storage, storageconfig, lifecycle, s3]
level: advanced
status: docs-checked
description: "Which cloud storage classes work with Kopia and how to set per-blob storage classes with .storageconfig."
sources: ["https://kopia.io/docs/advanced/storage-tiers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Storage classes trade cost against access speed and redundancy: hot is the most expensive to store and cheapest to access, cold is cheaper to store and costlier to access, archive is cheapest but typically delays access by hours. Some classes bill a minimum retention period (for example 90 days) even if you delete sooner.

Kopia works with any class giving instant access (hot or cold). It does not work with delayed-access archive classes such as Amazon Glacier Deep Archive. If you rarely download or test snapshots, a cold instant-access class may save money.

## Ways to set a class

1. Lifecycle rules in your provider account that move objects after some days (managed outside Kopia).
2. A default storage class for the bucket (also outside Kopia; Kopia just inherits it).
3. A `.storageconfig` file for S3 and compatible storage, uploaded before you create the repository so it applies to every upload. It never changes objects already uploaded.

```json
{
   "blobOptions": [
     { "prefix": "p", "storageClass": "STANDARD_IA" },
     { "storageClass": "STANDARD" }
  ]
}
```

Add an object to `blobOptions` for each blob type whose class you want to change, naming its `prefix` (`p`, `q`, `n`, `m`, `l`, `x`, `s`). In the example, `p` blobs use `STANDARD_IA` and all other blobs `STANDARD`. `p` blobs are rarely read again, so cold storage may save money there; `q`, index and session blobs are read and written often, so cold storage is unlikely to save money for them. For non-AWS S3 providers, look up that provider's storage class names.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Storage Tiers page (hot/cold/archive trade-offs, minimum retention example of 90 days, instant-access requirement, lifecycle rules, bucket default, .storageconfig for S3-compatible storage and its upload-before-create caveat, blob prefixes). Removed or corrected: the unsupported 'keep metadata in hot storage' phrasing and the claim that an entry without a prefix is a named default, replaced with the page's wording.
Method: documentation only; no commands were run.
