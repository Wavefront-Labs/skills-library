---
id: computing-software.devops-ci-cd.gitea.permissions
name: permissions
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-unit-permissions, gitea, repository-units, owner-team, collaborator-permission, organization-teams]
level: practitioner
status: docs-checked
description: "Gitea permission model: repository units (Code, Issues, PullRequests, Releases, Wiki, Projects, Packages, Actions, Settings), collaborators, owner, admin and general teams."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/access-control/permissions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea permissions

A repository is split into **units**; each has a permission level:
Code, Issues, PullRequests, Releases, Wiki, Projects, Packages, Actions: Read / Write. ExternalWiki and ExternalTracker: Read (links only). Settings: Admin.

What each level allows:
- Code: Read views tree, files, commits, branches; Write pushes.
- Issues / PullRequests: Read views and creates; Write adds labels, assigns, closes.
- Releases: Read views and downloads; Write creates and edits.
- Wiki: Read views and clones the wiki repo; Write edits pages and pushes.
- Projects: Read views columns; Write moves issues across columns.
- Packages: Read views; Write uploads and deletes.
- Actions: Read views logs; Write approves, cancels, restarts runs.
- Settings: Admin manages the repository.

## Individual repositories
The creator is the only owner, with no limits including delete and transfer. The owner adds collaborators with Read, Write or Admin. A private repo behaves for permitted users like an anonymous public one: read content, clone, create issues, comment, open PRs. Write can push to branches, subject to branch protection (`gitea-branch-protection`), and edit wiki pages; Admin can change repository settings. Only the owner can delete or transfer.

## Organization repositories
Owners are the members of the **Owner team**, created with the organization (creator first member, cannot be deleted, must keep at least one member). Teams come in two kinds:
- **Admin team**: members can do anything on the repositories it covers; only owner or admin team members can create new teams.
- **General team**: per-unit permissions, a repository scope (all repositories or selected ones), and whether the team may create repositories. A user can join several teams.

## Checked
2026-11-03. Unit levels, individual and organization repository behaviour, and team types confirmed against the Gitea docs page permissions.md (raw markdown, gitea/docs main branch). Removed the Practical notes section, which is not on the page.
Method: documentation only; no commands were run.
