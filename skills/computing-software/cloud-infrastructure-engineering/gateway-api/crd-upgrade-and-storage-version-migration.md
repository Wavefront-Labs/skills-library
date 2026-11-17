---
id: computing-software.cloud-infrastructure-engineering.gateway-api.crd-upgrade-and-storage-version-migration
name: crd-upgrade-and-storage-version-migration
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [crd, upgrade, storage-version, migration, kube-storage-version-migrator, webhook]
level: advanced
status: docs-checked
description: "Upgrade Gateway API CRDs safely: who owns them, avoiding rollbacks, stuck old storage versions and the validating webhook removed in v1.1."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/crd-management/_index.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/versioning.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The CRD management guide covers installing and upgrading the Gateway API CRDs, which are highly privileged cluster-scoped resources. A cluster admin or the cluster provisioning tool or provider should manage them. Implementations that bundle CRDs must never overwrite CRDs with unrecognised or newer versions, overwrite CRDs of a different release channel, or remove CRDs.

Upgrade guidelines:

- Standard channel CRDs make upgrades simpler and safer.
- Avoid moving backwards: newer CRDs can add fields, and rolling back could lose that configuration.
- Read the release notes before upgrading, and understand the versioning policy.
- Upgrading across several minor versions at once is usually safe, but one minor version at a time is the safest and most widely tested path.
- Experimental channel upgrades can include breaking changes or removals without prior deprecation; some may require uninstalling and reinstalling the Experimental CRDs, which release notes will say.
- Check the `gateway.networking.k8s.io/bundle-version` and `gateway.networking.k8s.io/channel` annotations on the CRDs to see what is installed.
- Validating admission policies guard channel boundaries: the Upgrade VAP stops Experimental CRDs being applied over Standard ones (remove it if you really need to).

Validating webhook: deprecated starting in v1.0 in favour of CEL validation within the CRDs, and removed in v1.1, so it is no longer an upgrade consideration.

API version removal (only relevant if you have used Gateway API since v0.5.0 in the same cluster): in the Standard channel, removing an alpha version such as `v1alpha2` is spread over at least four minor releases: a newer version becomes the storage version; the old one is deprecated; it stops being served but stays in the CRD for translation; finally it is dropped from the CRD. A CRD storage version change takes effect for an object only when that object is saved again, so objects never modified may still sit on the old storage version and block the upgrade that drops it (for example a GatewayClass created with v0.5.0 CRDs, stored as `v1alpha2`, blocks upgrading to v1.0.0 CRDs). Fix by updating every such object, for example an empty `kubectl patch` per object, or let `kube-storage-version-migrator` migrate resources to the latest storage version automatically.

## Checked

2026-11-08. Read in full (GitHub markdown): the CRD Management guide and the Versioning page. Confirmed: ownership guidance, bundling rules, upgrade guidelines, webhook deprecation and removal, the four-step version removal sequence with the GatewayClass example, empty patch and kube-storage-version-migrator, annotations, Upgrade VAP. Removed: the server-side apply recommendation, "install a whole release bundle", "upgrade only to a version all controllers support", the claim that validation moved into ValidatingAdmissionPolicies, and the observedGeneration verification step, none of which appear in these pages.

Method: documentation only; no commands were run.
