---
id: computing-software.cloud-infrastructure-engineering.harbor.cosign-signing
name: cosign-signing
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [cosign, sigstore, image-signing, accessories, harbor]
level: practitioner
status: docs-checked
description: "Sign images in Harbor with cosign sign, view and delete signatures as accessories, and replicate them (manual or scheduled only)."
sources:
  - https://goharbor.io/docs/main/working-with-projects/working-with-images/sign-images/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor v2.5 and later integrates Cosign, part of Sigstore. Cosign pushes the signature to Harbor, where it is stored as an accessory next to the signed artifact. Harbor tracks the link, so tag retention and other policies can apply to the pair.

Sign: install cosign and generate a key, then
`cosign sign --key cosign.key <harbor-instance>/<image/path>:<image-tag>`
Enter the key password and the signature is uploaded. In the project, click the `>` icon on the artifact to open the Accessories table: name, type, size, created time.

Delete: expand Accessories, click the three-dot icon beside a signature, then Delete. Deleting the signed artifact deletes all its signatures. Garbage collection never removes a signature on its own, because the collector cannot see accessory artifacts. Harbor does not support `cosign clean`, since it uses tag deletion that Harbor has not implemented.

Replication: signatures replicate with their artifact. Between Harbor instances the target keeps the link. To another registry type, the subject manifest and signatures appear as separate artifacts in the repository. Only Manual and Scheduled trigger modes apply; event-based replication cannot work because an unsigned image cannot be replicated before the signature exists.

Enforcement is separate: enable the Cosign policy in project Configuration to block unverified pulls.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Sign Artifacts with Cosign and Notation.
Method: documentation only; no commands were run.
