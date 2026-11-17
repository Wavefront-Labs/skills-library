---
id: computing-software.cloud-infrastructure-engineering.portainer.manage-registry-tags-in-portainer
name: manage-registry-tags-in-portainer
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [registries, tags, retag, docker-registry, delete]
level: intro
status: docs-checked
description: "Browse a registry in Portainer and add, retag or remove tags, including the registry setting that must be enabled for deletes."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/registries/manage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Portainer's registry manager lets you browse defined registries and manipulate their content from one interface.

Browse: Registries, choose the registry, click browse, and select a repository.

Add a tag: tags are created by cloning an existing one. Click Clone on the tag to use as a template, type the new name and click Clone Tag.

Retag: for a registry you host yourself, set `REGISTRY_STORAGE_DELETE_ENABLED=TRUE` in the registry's environment first. Then clone the tag under the new name, tick the original tag and click Remove.

Remove a tag: the same delete setting is needed on a self-hosted registry, then tick the tag and remove it.

Retagging is therefore clone-then-delete rather than a rename. Removing a tag asks for confirmation; click Delete.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Removed unconfirmed claims about restarting the registry and hosted registries; added the confirmation step.

Method: documentation only; no commands were run.
