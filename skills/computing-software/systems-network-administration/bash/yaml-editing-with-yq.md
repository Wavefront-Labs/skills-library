---
id: computing-software.systems-network-administration.bash.yaml-editing-with-yq
name: yaml-editing-with-yq
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, yq, yaml, text-processing, mikefarah-yq, kubernetes-manifests, config-editing]
level: practitioner
status: draft
description: "Read and edit YAML from the shell with yq (mikefarah v4): select paths, in-place updates, env substitution, merging files, multi-document handling and the python-yq trap."
sources:
  - https://mikefarah.gitbook.io/yq
  - https://github.com/mikefarah/yq
  - https://github.com/kislyuk/yq
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# YAML with yq

## Which yq?
Two different tools share the name: **mikefarah/yq** (Go, `yq --version` → `mikefarah/yq version v4.x`) and
**kislyuk/yq** (Python jq wrapper, Debian/Ubuntu `apt install yq`). Syntax below is mikefarah v4 —
get it from GitHub releases, snap, brew or `dnf install yq` (Fedora). Scripts should check the version.

## Read
```bash
yq '.spec.replicas' deploy.yaml
yq '.spec.template.spec.containers[].image' deploy.yaml
yq '.items[] | select(.kind == "Service") | .metadata.name' all.yaml
yq -o=json '.' config.yaml | jq ...          # convert; -p=json/xml/csv/props for input formats
yq 'keys' values.yaml
```
## Write
```bash
yq -i '.spec.replicas = 3' deploy.yaml
yq -i '.image.tag = strenv(TAG)' values.yaml              # env var as string (env() parses as YAML)
yq -i '.servers += [{"name": "web3", "ip": "10.0.0.13"}]' inv.yaml
yq -i 'del(.debug)' app.yaml
yq -i '(.containers[] | select(.name == "app") | .resources.limits.memory) = "512Mi"' pod.yaml
yq eval-all '. as $item ireduce ({}; . * $item)' base.yaml override.yaml > merged.yaml   # deep merge
```
## Multi-document files
`---`-separated docs are processed one by one; `select(documentIndex == 1)`; `yq -s '.metadata.name' all.yaml`
splits into files named by expression.

## Gotchas
- Quote the expression in single quotes; inside it use double quotes for strings.
- `-i` rewrites formatting minimally but may change quoting/comments positions; diff before committing.
- `"yes"`/`on` are strings in YAML 1.2 (yq) but booleans to YAML 1.1 parsers (old PyYAML, Ansible) — quote them.
- Anchors/aliases: use `explode(.)` before editing aliased nodes.

## Verify
- [ ] `yq '.' file.yaml >/dev/null` parses; `git diff` shows only the intended change.
