---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-violations-dryrun-warn-and-log-denies
name: opa-gatekeeper-violations-dryrun-warn-and-log-denies
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, enforcement-action, dryrun, warn, log-denies, rollout, constraint-status]
level: practitioner
status: docs-checked
description: "Roll out new Gatekeeper constraints safely with enforcementAction dryrun or warn, and log every deny, dryrun and warn with --log-denies."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/violations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper violations dryrun warn and log denies

`enforcementAction` on a Constraint defaults to `deny`. Supported values are `deny`, `dryrun` and `warn`.

- `dryrun`: the constraint is deployed but changes nothing. Impacted resources show up as violations in the Constraint `status`, each tagged `enforcementAction: dryrun`. Use this when introducing a constraint to a running cluster.
- `warn` (Gatekeeper v3.4+ with Kubernetes v1.19+): same as dryrun, plus the user gets immediate feedback. `kubectl apply` prints for example `Warning: [prod-repo-is-openpolicyagent] container <nginx> has an invalid image repo <nginx>, allowed repos are ["openpolicyagent"]` and the object is still created.

```yaml
spec:
  enforcementAction: dryrun
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
  parameters:
    labels: ["gatekeeper"]
```

Start the controller with `--log-denies` to log all deny, dryrun and warn failures. That is useful for seeing what is being denied or failing a dry run, and for debugging cluster problems without enabling data sync or reading the status of every constraint.

The `--disable-enforcementaction-validation=true` flag turns off validation against the list of supported actions.

## Checked

2026-11-08. Confirmed against violations.md, read in full: --log-denies, dryrun behaviour and status example, warn availability (v3.4+, Kubernetes v1.19+) and output, supported actions list, --disable-enforcementaction-validation. Removed or corrected: mention of scoped as a supported value (this page lists deny, dryrun, warn) and the custom action name framing.

Method: documentation only; no commands were run.
