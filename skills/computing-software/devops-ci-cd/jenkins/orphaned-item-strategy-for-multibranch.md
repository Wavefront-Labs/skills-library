---
id: computing-software.devops-ci-cd.jenkins.orphaned-item-strategy-for-multibranch
name: orphaned-item-strategy-for-multibranch
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, multibranch-pipeline, orphaned-item-strategy, discard-old-items, dead-branches, branch-cleanup, organization-folder, jenkins-home-disk, build-discarder, job-dsl]
level: practitioner
status: draft
description: "Set the multibranch/org-folder orphaned item strategy so deleted branches and closed PRs are removed on schedule without losing release history or filling JENKINS_HOME."
sources: ["https://www.jenkins.io/doc/book/pipeline/multibranch/", "https://plugins.jenkins.io/branch-api/", "https://jenkinsci.github.io/job-dsl-plugin/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Orphaned item strategy

When a branch is deleted or a PR closed, the next scan marks its job **orphaned** (shown
struck through, "dead branch"). The *Orphaned Item Strategy* decides when it is deleted.

## Settings
*Configure -> Orphaned Item Strategy -> Discard old items*:
- **Days to keep old items**: delete orphaned jobs this many days after they became
  orphaned (based on the last build time). 7-14 days is typical: long enough to look at
  a closed PR's logs, short enough to bound disk.
- **Max # of old items to keep**: cap the count of orphaned jobs regardless of age.
- Blank both = keep forever (the default for some versions; check, it fills disk).
- *Abort builds* (Branch API 2.7+ option): abort running builds of orphaned items.

This is distinct from the **Build Discarder** (`options { buildDiscarder(logRotator(numToKeepStr: '20')) }`),
which trims builds *inside* a live branch job. You want both.

## As code
```groovy
multibranchPipelineJob('payments') {
  orphanedItemStrategy {
    discardOldItems { daysToKeep(7); numToKeep(50) }
  }
}
// organizationFolder: same block; it applies to repos removed from the org,
// while each repo's own multibranch inherits the folder's setting
```

## Gotchas
- Deletion happens only during a **scan** (branch indexing). If you rely solely on
  webhooks and never scan, orphans never get deleted. Keep a periodic scan
  (`Periodically if not otherwise run`, e.g. 1 day).
- Release history: if releases are built on `release/*` branches that you later delete,
  their artifacts and logs vanish too. Build releases from tags (tag discovery) and keep
  tags, or archive artifacts to an external repository.
- A transient SCM outage or credential failure during a scan can make every branch look
  deleted. Branch API refuses to orphan items when the scan fails, but a misconfigured
  filter (`Filter by name` regex change) will orphan everything legitimately; review
  before editing filters on large orgs.
- Org folders: removing a repo from the GitHub App installation orphans its whole
  multibranch project.

## Verify
Delete a test branch, run *Scan Repository Now*: the log reports
`Will remove <branch>` once the age/count threshold is passed; with 0 days it disappears
on that scan.
