---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-uninstall-and-crd-cleanup
name: opa-gatekeeper-uninstall-and-crd-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, uninstall, helm, crd, cleanup, kubectl]
level: practitioner
status: docs-checked
description: "Remove OPA Gatekeeper by the same method used to install it, and delete the leftover CRDs that Helm v3 does not clean up."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/install.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper uninstall and crd cleanup

Uninstall using the same route as install:
- Manifest install: `kubectl delete -f` the same `gatekeeper.yaml` URL.
- make install: from the repository directory run `make uninstall`.
- Helm: `helm delete gatekeeper --namespace gatekeeper-system`.

Helm v3 leaves the Gatekeeper CustomResourceDefinitions behind. Remove them with:

```sh
kubectl delete crd -l gatekeeper.sh/system=yes
```

This also deletes any user-installed config changes, ConstraintTemplates and Constraints, so back up your policy YAML first.

Only the Helm route is documented as leaving CRDs behind; the manifest and make routes list no extra cleanup step.

## Checked

2026-11-08: read the Uninstallation section of website/docs/install.md in the Gatekeeper repo. Confirmed the three uninstall routes, the Helm v3 CRD note, the label selector command and the data-loss note. Removed: the emergency webhook deletion advice and the redeploy claim, which that page does not state.

Method: documentation only; no commands were run.
