---
id: computing-software.cybersecurity-defensive.system-hardening.golden-image-pipeline
name: golden-image-pipeline
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [golden-image, immutable-infrastructure, packer, image-pipeline, cis-hardened-images, patch-baseline, image-versioning, ami, vm-template, container-base-image, rebuild-vs-patch]
level: advanced
status: draft
description: "Build and maintain a hardened golden image pipeline (Packer/image builder) so new instances start compliant, patched, and rebuildable instead of hand-hardened and drifting."
sources: ["HashiCorp Packer documentation (public)", "CIS Hardened Images / CIS Benchmarks (public)", "AWS/Azure/GCP image builder service documentation (public)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Golden image pipeline — build hardened and patched in, don't bolt it on after

**Goal:** produce a versioned, hardened base image (VM or container) that every
new instance launches from, so hardening and patch baseline are applied once in
the pipeline rather than manually on every box — and so "rebuild from the latest
image" is a real, fast remediation option, not a multi-day manual rebuild.

## 1. Bake the CIS baseline into the image, don't apply it post-boot
Apply the hardening baseline (see the companion cis-benchmark-baselines skill
for the control-by-control detail) as part of the image build itself (Packer
provisioners, cloud image builder service, or a container base-image Dockerfile
layer) rather than as a configuration-management run that happens after an
instance boots. Baking it in means every instance starts compliant from first
boot, including ones launched by auto-scaling before any post-boot
configuration pass has a chance to run — a real gap when auto-scaling launches
instances faster than a CM tool's first convergence cycle.

## 2. Patch the image on a schedule, not just the fleet
Rebuild the golden image on a regular cadence (weekly is common for OS patches)
by running the build pipeline against the latest upstream base image plus
current patches, then **replace running instances with new ones from the new
image** rather than patching long-lived instances in place. This is the core
shift immutable infrastructure makes: patching becomes "deploy a new image
version and cycle instances" instead of "SSH in and apply updates," which is
more consistent (no drift between instances patched at different times) and
makes rollback trivial (redeploy the previous image version).

## 3. Version and test every image before it's promoted
Tag each built image with a version, the base image/patch level it was built
from, and a build date. Run an automated compliance scan (CIS benchmark scanner,
your own test suite) against every new image build *before* it's promoted to
"latest" / made available for launch — a hardening regression introduced by an
upstream base image change should fail the pipeline, not reach production
instances. Keep at least the last few known-good image versions available for
fast rollback.

## 4. Minimize what's baked in
A golden image with every tool "just in case" installed increases attack surface
and patch burden for packages most instances never use. Bake in only what's
genuinely needed by the majority of launches (base OS hardening, the agent
stack — EDR, logging, config management client), and push workload-specific
software to a later, narrower provisioning step or a separate layer (for
containers, a thin application layer on top of a minimal hardened base).

## 5. The rebuild-vs-patch decision at incident time
A golden image pipeline turns "redeploy from a known-good image" into a real
incident-response option: if a host is compromised and the entry vector is
understood, replacing it with a fresh instance from the current hardened image
is often faster and more certain than trying to fully clean an existing host —
but only if the image pipeline is actually current and the application's state/
data lives outside the instance (externalized to a database, object storage, or
a config management pass that runs post-launch) rather than baked into
whichever instance happens to be running.

## Gotchas
- An image pipeline that nobody rebuilds regularly becomes a stale, falsely
  reassuring artefact — "we launch from a hardened image" is false if that image
  is eight months out of patch.
- Secrets or credentials baked into an image at build time (even temporarily, for
  a provisioner step) persist in the image artefact and every instance launched
  from it — use runtime secret injection (instance metadata, a secrets
  manager pulled at boot), never bake credentials in.
- Auto-scaling groups pinned to an old, specific image ID (rather than "latest
  approved") silently keep launching outdated instances even after the pipeline
  produces new, patched versions — audit what image ID is actually referenced by
  every launch template/configuration, not just whether the pipeline runs.
- Container base images have the same staleness risk as VM images but are
  easier to forget — a Dockerfile `FROM` pinned to an old tag doesn't get newer
  patches just because the registry has a newer one available; rebuild and
  re-tag on the same cadence as VM images.

## Verify
- [ ] Hardening and current patches are baked into the image build, not applied
      only after instance boot.
- [ ] Images are rebuilt on a regular cadence and automatically scanned for
      compliance before promotion.
- [ ] Launch templates/configurations reference the current approved image, not
      a pinned old version, confirmed by audit.
- [ ] No credentials/secrets are baked into the image artefact.
- [ ] Application state/data lives outside the instance so rebuild-from-image is
      a viable fast remediation path.

Related: computing-software.cybersecurity-defensive.system-hardening.cis-benchmark-baselines,
computing-software.cybersecurity-defensive.system-hardening.configuration-drift-detection,
computing-software.cybersecurity-defensive.vulnerability-management.patch-management-coordination
