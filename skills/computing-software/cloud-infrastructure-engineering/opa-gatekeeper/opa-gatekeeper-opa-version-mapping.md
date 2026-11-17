---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-opa-version-mapping
name: opa-gatekeeper-opa-version-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, opa, versions, compatibility, rego, upgrade]
level: practitioner
status: docs-checked
description: "Look up which OPA engine version each Gatekeeper release bundles, for example v3.19.0 bundling OPA 1.3.0 and v3.18 bundling 0.68.0."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/opa-versions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper opa version mapping

Gatekeeper embeds Open Policy Agent, so Rego features and builtins available to your ConstraintTemplates depend on the Gatekeeper release. The project publishes a mapping table. A selection:

- v3.23.0 and v3.23.1: OPA v1.17.1
- v3.22.0 to v3.22.2: OPA v1.13.2
- v3.21.0 and v3.21.1: OPA v1.10.0
- v3.20.1: OPA v1.7.1; v3.20.0: OPA v1.5.1
- v3.19.0 and v3.19.1: OPA v1.3.0; v3.19.2 and v3.19.3: OPA v1.5.1
- v3.18.x and v3.17.2: OPA v0.68.0
- v3.17.0/v3.17.1: v0.67.0
- v3.15.x: v0.60.0
- v3.13.x: v0.54.0
- v3.12.0: v0.49.2
- v3.10.0: v0.44.0
- v3.6.0 through v3.7.2: v0.29.4
- v3.1.0 through v3.2.3: v0.21.0

Check the table before using newer OPA builtins or syntax in a template, since an older Gatekeeper cannot evaluate them.

## Checked

2026-11-04. Confirmed against opa-versions.md (every version pair listed was compared to the table). Removed or corrected: the claim that v3.19 introduced opt-in Rego v1 syntax (not on the page).

Method: documentation only; no commands were run.
