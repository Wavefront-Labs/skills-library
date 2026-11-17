---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-cli-install-and-applications
name: quadlet-cli-install-and-applications
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet-install, application, quadlets-file, filename, replace, reload-systemd, podman-quadlet]
level: practitioner
status: docs-checked
description: "Install Quadlets with podman quadlet install: single files, directories as applications with --application, .quadlets multi-unit files with FileName comments, URLs and --replace."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-quadlet-install.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: install Quadlets for the current user without copying files by hand.

`podman quadlet install [options] quadlet-path-or-url [files-path-or-url]...` installs a single Quadlet (optionally with extra non-Quadlet files), a directory of Quadlet and other files (such as a config file for a container), or several Quadlets from one `.quadlets` file whose units are separated by `---`. Each section in a `.quadlets` file needs a `# FileName=<name>` comment. Sources may be local files or web URLs.

An application is a set of Quadlet and non-Quadlet files that live together. Removing a Quadlet in an application removes the whole application. Everything installed from a directory is a single application. Multiple units from one `.quadlets` file count as one application only if you pass `--application`.

Options: `--application=string` installs the files under a directory of that name; it is required when giving a directory path and the name may not end in a Quadlet extension (`foo.container` is invalid). `--replace`/`-r` replaces the installation even if the generated unit already exists (default false), used mainly to update a unit. `--reload-systemd` reloads systemd after the operation (default true).

Example: `podman quadlet install --application=foo ./quadlet-app/`. Multi-quadlet processing needs the `.quadlets` extension.

## Checked

2026-11-03. Read against the official page text (podman-quadlet-install.1); every key, value, default, path and example left in this skill was confirmed there. Nothing removed. Wording tightened where the page is softer than the draft.
Method: documentation only; no commands were run.
