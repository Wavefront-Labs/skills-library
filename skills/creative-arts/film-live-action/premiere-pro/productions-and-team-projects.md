---
id: creative-arts.film-live-action.premiere-pro.productions-and-team-projects
name: productions-and-team-projects
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, film-live-action, productions-setup, shared-project, project-locking, team-projects-setup, cloud-collaboration, shared-team-project, multi-editor, shared-storage]
level: practitioner
status: draft
description: "Set up multi-editor Premiere Pro work: Productions on shared storage with project locking and referencing, versus Team Projects in the cloud, with scratch disks and media paths."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/productions.html (Adobe - Productions in Premiere Pro)"
  - "https://helpx.adobe.com/premiere-pro/using/team-projects.html (Adobe - Team Projects)"
  - "https://helpx.adobe.com/premiere-pro/using/best-practices-productions.html (Adobe - Productions best practices)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Productions and Team Projects

**Goal:** several editors and assistants work on one show at once without overwriting
each other or breaking media links.

## 1. Productions (shared storage)
A **Production** is a folder of Premiere projects managed together (*File > New >
Production*), stored on shared storage (SAN/NAS) every workstation mounts at the **same
path**.
- Split work into many small projects: one per reel/scene/episode, dailies by day,
  "Assistant" and "Editor" projects - smaller projects open fast.
- **Project locking**: when one user opens a project with write access, others open it
  **read-only** (lock icon, user name shown). Ask for the lock or work in your own
  project.
- **Referencing across projects**: drag clips/sequences between projects in the
  Production panel; Premiere keeps **one master clip reference** in the production -
  avoids duplicates.
- Production settings: shared **scratch disks** (preview files, auto-save) set to
  per-user/local paths for performance and to avoid collisions (*Production Settings*).
- Media on shared storage, never on local drives.

## 2. Team Projects (cloud)
Hosted via Creative Cloud: the **project** (not media) syncs through Adobe's cloud;
each editor has media locally or on their own storage at matching relative paths.
- Collaborators **share changes** explicitly (upload) and accept others' changes;
  conflicts flagged.
- Good for remote teams with small media footprints or proxies (see remote proxies).
- Check current Adobe status - Adobe has been moving collaboration toward Frame.io
  integrations; confirm Team Projects availability for your version.

## 3. Choosing
| Need | Use |
|---|---|
| Facility with shared storage, features/series | Productions |
| Remote editors, small team | Team Projects or Productions on a cloud-synced/ remote desktop setup |
| Single editor | Normal project |

## 4. Conventions
- Naming: `EP101_Edit_v012_JS.prproj`; who owns which project written in a team doc.
- Archive versions daily (Auto Save + manual dated copies).
- Same Premiere version and plugins on every seat.

## Gotchas
- Different mount paths (`/Volumes/Media` vs `M:`) - media offline on other seats.
- One giant project in a Production - slow, locked by one person all day.
- Shared scratch disk paths causing render-file collisions.
- Mixed Premiere versions - projects can't be opened backwards.

## Verify
- [ ] Production on shared storage with identical mount paths.
- [ ] Work split into small projects; locking understood.
- [ ] Scratch disks per user; same app/plugin versions.
- [ ] Project naming and ownership documented; backups daily.
