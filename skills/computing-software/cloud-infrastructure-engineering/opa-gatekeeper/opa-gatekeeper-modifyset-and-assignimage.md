---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-modifyset-and-assignimage
name: opa-gatekeeper-modifyset-and-assignimage
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, modifyset, assignimage, prune, merge, image, digest]
level: advanced
status: docs-checked
description: "Remove or add list items with the ModifySet mutator and rewrite image domain, path or tag with AssignImage in Gatekeeper."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/mutation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper modifyset and assignimage

ModifySet treats a list like a set. `operation: merge` (default) appends missing values at the end; `operation: prune` removes them. Values come from `parameters.values.fromList`. Remove an argument from all containers:

```yaml
apiVersion: mutations.gatekeeper.sh/v1
kind: ModifySet
metadata:
  name: remove-err-logging
spec:
  applyTo:
    - groups: [""]
      kinds: ["Pod"]
      versions: ["v1"]
  location: "spec.containers[name: *].args"
  parameters:
    operation: prune
    values:
      fromList:
        - --alsologtostderr
```

AssignImage (apiVersion `mutations.gatekeeper.sh/v1alpha1`) edits parts of an image such as `my.registry.io:2000/repo/app:latest`: domain `my.registry.io:2000`, path `repo/app`, tag `:latest`. Set one or more of `assignDomain`, `assignPath`, `assignTag` under `parameters`. `assignTag` must start with `:` or `@` (so a digest works: `@sha256:...`). If `assignPath` could be read as a domain, such as `my.repo.lib/app`, also set `assignDomain`. The match section accepts `source: "All"`.

Both are in the same family as Assign and use the same `applyTo`, `match` and `location` syntax, including list selectors such as `spec.containers[name:nginx].image`. The `fromMetadata` option does not apply to ModifySet; values come from `fromList`.

## Checked

2026-11-04. Confirmed against mutation.md (ModifySet, AssignImage, applyTo/match/location). Removed or corrected: an unsourced 'typical use' sentence and a repeated reminder.

Method: documentation only; no commands were run.
