---
id: computing-software.devops-ci-cd.gitlab-ci.container-registry-cleanup-policies
name: container-registry-cleanup-policies
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, cleanup-policy, container-registry-cleanup, tag-expiration, registry-garbage-collection, protected-container-tags]
level: practitioner
status: docs-checked
description: "Stop container registry bloat with cleanup policies (keep_n, regex keep/remove, older_than), bulk tag deletion via API, protected tags, and garbage collection on self-managed."
sources: ["https://docs.gitlab.com/user/packages/container_registry/reduce_container_registry_storage/", "https://docs.gitlab.com/api/container_registry/", "https://docs.gitlab.com/administration/packages/container_registry/#container-registry-garbage-collection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container registry cleanup policies

## 1. Policy (Settings → Packages and registries → Cleanup policies)
- Run cleanup: choose a cadence (the reduce-storage page lists the values, for example `3month`).
- **Keep** the most recent N tags per image (`keep_n`), and tags matching a regex (`v\d+\.\d+\.\d+|main|latest`).
- **Remove** tags older than X days matching a regex (`.*` or `mr-.*|sha-.*`).
Keep rules win over remove rules.
API:
```bash
curl -X PUT -H "PRIVATE-TOKEN: $T" "$API/projects/$PID" \
  --data "container_expiration_policy_attributes[enabled]=true" \
  --data "container_expiration_policy_attributes[cadence]=1month" \
  --data "container_expiration_policy_attributes[keep_n]=10" \
  --data "container_expiration_policy_attributes[older_than]=14d" \
  --data-urlencode "container_expiration_policy_attributes[name_regex]=.*" \
  --data-urlencode "container_expiration_policy_attributes[name_regex_keep]=v.+|main|latest"
```

## 2. Immediate bulk delete
```bash
REPO=$(curl -s -H "PRIVATE-TOKEN: $T" "$API/projects/$PID/registry/repositories" | jq '.[]|select(.path|endswith("/api")).id')
curl -X DELETE -H "PRIVATE-TOKEN: $T" "$API/projects/$PID/registry/repositories/$REPO/tags" \
  --data-urlencode 'name_regex_delete=mr-.*' --data 'keep_n=5' --data 'older_than=7d'
```
Runs asynchronously, and excludes protected tags and the tag `latest`.

## 3. Protect release tags
Protected container tags are excluded from cleanup policies and from the bulk delete API.

## 4. Storage actually freed?
Deleting tags removes references; layers are reclaimed by garbage collection. The next-generation registry (with the metadata database) supports online garbage collection. Otherwise an administrator runs `sudo gitlab-ctl registry-garbage-collect` (the `-m` switch also removes untagged manifests and unreferenced layers), which shuts the registry down while it runs.

## Gotchas
- The tag `latest` is never removed by a cleanup policy or the bulk delete API.
- Images referenced by running deployments by tag will fail to re-pull after deletion — deploy by digest.

## Verify
- [ ] Registry size drops after the first policy run and the garbage collection that follows (the docs describe it starting about 24 hours after a tag is deleted).

## Checked

2026-10-28. Confirmed on the reduce-storage, container registry API and administration pages: cleanup policy keep_n, name_regex and name_regex_keep, older_than, 3month cadence value, the project API attribute container_expiration_policy_attributes with cadence/keep_n/older_than/name_regex/name_regex_keep, bulk DELETE with name_regex_delete, keep_n and older_than, asynchronous execution, protected tags excluded, tag latest never removed, gitlab-ctl registry-garbage-collect with -m, online garbage collection in the next-generation registry, 24-hour garbage collection delay. Removed: the once-per-hour rate limit, the full cadence list, anchored-regex claim, shared-tag claim, and the claim that GitLab.com handles GC.
Method: documentation only; no commands were run.
