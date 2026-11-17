---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-gator-policy-library-manager
name: opa-gatekeeper-gator-policy-library-manager
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, gator-policy, gatekeeper-library, bundles, catalog, pod-security, exit-codes]
level: advanced
status: docs-checked
description: "Search, install, upgrade and remove gatekeeper-library policies with gator policy, including bundles, conflict handling and exit codes (v3.22+, alpha)."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/gator.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper gator policy library manager

`gator policy` (alpha, v3.22+) is a brew-style manager for the official gatekeeper-library. Commands: `search` and `update` (use the cached catalog, no cluster needed), `list`, `install`, `uninstall` and `upgrade` (need a cluster), and `generate-catalog` (for library maintainers). Run `update` first to fetch the catalog.

Install model: installing an individual policy installs only its ConstraintTemplate; installing a bundle installs templates plus pre-configured Constraints. Bundles include `pod-security-baseline` and `pod-security-restricted` (Pod Security Standards levels).

Managed resources get tracking metadata. Conflict rules: install if absent; update if managed by gator and the version differs; skip if same version; refuse with an error if the resource exists but is not managed by gator.

Exit codes: 0 success; 1 general error (network, bad arguments); 2 cluster error (not found, permission denied); 3 conflict (exists and unmanaged); 4 partial success.

Environment: `GATOR_HOME` (cache directory, default under the user config dir), `GATOR_CATALOG_URL` (catalog source) and `KUBECONFIG`.

## Checked

2026-11-04. Confirmed against gator.md (gator policy sections: commands, bundles, conflict resolution, exit codes, environment variables). Removed or corrected: nothing.

Method: documentation only; no commands were run.
