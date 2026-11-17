---
id: computing-software.devops-ci-cd.jenkins.branch-build-strategies
name: branch-build-strategies
category: computing-software
field: devops-ci-cd
product: jenkins
tags: [jenkins, multibranch-pipeline, basic-branch-build-strategies, build-strategies, skip-initial-build, tag-builds, change-requests, named-branches, branch-indexing, build-storm, suppress-automatic-scm-triggering]
level: practitioner
status: docs-checked
description: "Control which discovered branches, PRs and tags auto-build in Jenkins multibranch with the basic-branch-build-strategies plugin, and stop build storms after indexing."
sources: ["https://github.com/jenkinsci/basic-branch-build-strategies-plugin/blob/master/docs/user.adoc", "https://plugins.jenkins.io/basic-branch-build-strategies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Branch build strategies

Discovery decides which jobs exist; **build strategies** decide which of them are built
automatically when indexing or a webhook finds a change. With no strategy configured,
every discovered branch and PR builds, but tags never auto-build.

Install **Basic Branch Build Strategies** to get these (Branch source -> *Build strategies*):
| Strategy (UI name) | Builds |
|---|---|
| Regular branches | heads that are neither change requests nor tags |
| Change requests | PRs; option *Ignore rebuilding merge branches when only the target branch changed* |
| Tags | tags, filtered by age with *Ignore tags newer than* / *Ignore tags older than* (days); with the older-than option a first scan does not build years of old tags |
| Named branches | ordered match rules: *Exact name*, *Wildcard include/excludes* or *Regular expression* |
| Skip initial build on first branch indexing | nothing on first discovery; builds only on later changes |
| All Strategies Match / Any Strategies Match / None Strategies Match | boolean combinations of the above |

Without any strategy the Branch API default is to build everything except tags. As soon as you
add any strategy that default is disabled, so *only* listed strategies trigger builds;
forgetting "Change requests" stops PR builds.

## Stopping build storms
Creating an org folder or changing discovery can index hundreds of branches and queue
them all. Combine *Skip initial build on first branch indexing* with the other strategies, or
restrict builds with *Named branches* so only matching heads build automatically.

## Gotchas
- Tag jobs appear under the *Tags* tab but stay unbuilt without the Tags strategy; teams
  think tag discovery is broken.
- Strategies are evaluated at indexing/event time; changing them doesn't build existing
  heads until they change or are re-scanned.

## Verify
Push a tag younger than the age limit: the tag job builds automatically. Push to an
unmatched branch with *Named branches* only: job exists, no build queued.

## Checked
2026-10-25, Jenkins documentation (jenkins.io source repo, latest commit 2026-10-21) and plugin READMEs on GitHub. Confirmed in the plugin user guide and its Messages.properties: strategy names, Named-branches rule types, Tags newer-than/older-than options, change-request option text, default of building everything except tags, and that adding any strategy disables that default. Removed the Job DSL snippet, the default `-1` age claim and the untrusted-changes and suppress-trigger claims, which no documentation read confirmed.
Method: documentation only; no commands were run.
