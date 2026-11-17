---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-branch-override-and-pinned-revisions
name: controller-branch-override-and-pinned-revisions
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, allow-override, scm-revision, scm-branch, project-update, release-pinning, job-templates]
level: practitioner
status: docs-checked
description: "Pin controller projects to tags or commits for production, allow branch override on job templates for testing, and use refspecs for PR refs."
sources: ["https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/con-controller-job-branch-overriding.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-git-refspec.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/proc-scm-git-subversion.adoc", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/project.py", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/job_template.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller branch override and pinned revisions

Goal: production jobs run a known, reviewed commit; engineers can still launch the same template
against a feature branch without cloning the template or project.

## Pin production
The project's source control branch/tag/commit field accepts a branch, tag, commit hash or other
ref; blank means `HEAD`. Some commit hashes and refs are only available if you also set a custom
refspec. Production projects: a tag or SHA, changed by a pipeline on release.
```yaml
- ansible.controller.project:
    name: network-automation-prod
    organization: NetOps
    scm_type: git
    scm_url: https://git.example.com/netops/automation.git
    scm_branch: v2.4.1
    allow_override: false
```
(`awx.awx.project` takes the same parameters.)

## Allow override for test projects
**Allow branch override** lets a job template or inventory source that uses the project start with
a branch or revision other than the project's. Project admins can delegate branch selection to
template authors who need only the project's `use_role`.
```yaml
- ansible.controller.project:
    name: network-automation-dev
    scm_branch: main
    allow_override: true
    scm_refspec: "refs/*:refs/remotes/origin/*"   # extra refs to fetch so overrides resolve
- ansible.controller.job_template:
    name: Deploy VLANs (dev)
    project: network-automation-dev
    scm_branch: ""                   # blank = project default
    ask_scm_branch_on_launch: true   # prompt for branch at launch
```
The job template's `scm_branch` is only allowed if the project's `allow_override` is true.

## Pull requests and refspecs
The refspec field names extra references fetched from the remote; blank fetches only default refs
(branches under `refs/heads/`). Documented examples:
- `refs/*:refs/remotes/origin/*` fetches all references.
- `refs/pull/*:refs/remotes/origin/pull/*` (GitHub-specific) fetches all pull request refs.
- `refs/pull/62/head:refs/remotes/origin/pull/62/head` fetches one pull request ref.

With a refspec that fetches PR refs, a template that prompts for the branch can be launched with
`pull/N/head`. Project updates of any type run an extra `git fetch` for the refspec. The first two
examples can be slow on large projects.

## Update on launch and caching
**Update revision on launch** refreshes the project's revision to the remote's before each job.
To avoid job overflow when jobs start faster than the project can sync, set a cache timeout (seconds)
so recent syncs are reused. The collection ignores `scm_update_cache_timeout` unless
`scm_update_on_launch` is true.

## Gotchas
- Pinning a branch name is not pinning: `main` moves. Use tags/SHAs where change control matters.
- Update on launch with a moving branch means jobs minutes apart can run different code; pin for production.

## Verify
- [ ] The production project's synced revision equals the release tag's commit (`git rev-parse v2.4.1^{commit}`).
- [ ] Launching the dev template with a branch runs that branch's commit (check job details).

## Checked

- Date: 2026-11-09. Sources: ansible/aap-docs main (downstream modules: job branch overriding, git refspec, SCM types), ansible/awx devel awx_collection project.py and job_template.py.
- Confirmed: branch/tag/commit/ref field and blank = HEAD; refspec examples and default `refs/heads/` behaviour; extra `git fetch` per update; allow-branch-override definition, delegation via `use_role`; update revision on launch with cache timeout; module parameters `allow_override`, `scm_refspec`, `scm_update_on_launch`, `scm_update_cache_timeout`, `ask_scm_branch_on_launch`, and the "only allowed if allow_override is true" rule.
- Removed unconfirmed claims: `scm_revision` recorded on jobs via `/api/v2/jobs/<id>/`; the `awx job_templates launch --scm_branch` CLI example; override installing the branch's `requirements.yml`; webhook templates passing the branch; inventory sources ignoring overrides (the docs say inventory sources can override too); `scm_update_on_launch: false` as "nothing to fetch".

Method: documentation and collection source read from cloned repositories; no commands were run against a controller.
