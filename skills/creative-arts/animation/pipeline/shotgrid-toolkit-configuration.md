---
id: creative-arts.animation.pipeline.shotgrid-toolkit-configuration
name: shotgrid-toolkit-configuration
category: creative-arts
field: animation
product: pipeline
tags: [sgtk, shotgrid-toolkit, toolkit, pipeline-configuration, templates, engines, apps]
level: advanced
status: draft
description: "Configure ShotGrid Toolkit (sgtk): pipeline configuration layout, environments, engines and apps, templates and roots, hooks, descriptors and safe update practice."
sources:
  - https://developer.shotgridsoftware.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ShotGrid Toolkit configuration (sgtk)

**Toolkit** is the pipeline framework from ShotGrid (Flow Production Tracking). It provides file management, publishing and app launching through **engines** (DCC integrations such as tk-maya, tk-nuke, tk-houdini) and **apps** (such as Workfiles, Publish and Loader). A **pipeline configuration** defines which ones a project uses and how files are named. Check the developer site for the current default-config version and details.

## Config layout (typical)
```
config/
  core/templates.yml      # path and file templates
  core/roots.yml          # storage roots per OS
  core/hooks/             # core hooks (e.g. folder creation)
  env/*.yml               # environments: project, asset_step, shot_step ...
  hooks/                  # overrides for apps and engines
  info.yml, tk-metadata
```

## Key concepts
- **Templates** (`templates.yml`) define **keys** (name, version, Step, Shot) and **paths** and **strings** built from them, giving every file a predictable location; the templates drive Workfiles and Publish. Keep them in one place.
- **Roots** map named storage locations to OS-specific paths (`cross-platform-path-mapping.md`).
- **Environments** (`env/`) pick the engines and app settings per context (project, asset step, shot step), including which apps appear in which DCC.
- **Descriptors** state where code comes from, for example the app store, a git repo, a dev path or a path on disk; versions are pinned.
- **Hooks** are Python files that customise behaviour (publish plugins, folder creation, file naming) without editing core code. Override in `config/hooks`, not in installed app code.

## Workflow
1. Start from the default configuration provided by Autodesk and clone it for your project instead of building from scratch.
2. Make a **new pipeline configuration** to test (in ShotGrid's Pipeline Configurations or via `tank`), try changes on a dev config, then promote to production.
3. Use `tank` commands from the project's folder to update apps (for example `tank updates`) and to create folders for a context (`tank folders`). Check `tank --help` for the commands in your version.
4. Version-control the config in git; pin descriptors; record changes.
5. For publishing, write a **publish2** plugin through hooks (`pyblish-publish-plugins.md` for the alternative pattern).

## Gotchas
- Editing templates after assets exist breaks existing paths; plan the schema first.
- Different OS roots must all be defined, or farm hosts cannot resolve paths.
- Updating apps on the live config without testing can break artists' sessions.

## Verify
- [ ] Config tested in a dev config, then promoted.
- [ ] All OS roots defined; templates produce expected paths.
- [ ] Config is in version control.
