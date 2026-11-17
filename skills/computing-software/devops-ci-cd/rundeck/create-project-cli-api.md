---
id: computing-software.devops-ci-cd.rundeck.create-project-cli-api
name: create-project-cli-api
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, create-project, rd-projects, project-config, directory-source]
level: practitioner
status: docs-checked
description: "Create a Rundeck project from the GUI, the rd CLI or the REST API, including project label, default SSH key and a directory resource model source."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/projects/project-create.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
GUI: use the Project Picker or the full project menu, "New Project". Fields:
- Name: unique identifier; letters and numbers, no spaces or special characters.
- Label: friendly display name, may contain spaces.
- Description: brief; for long text use a project README.
- Execution History Clean, Execution Mode (Disable Execution, Disable Schedule), Job Group Expansion Level (`1` default, `0` collapse all, `-1` expand all), README and MOTD display, Default Node Executor (SSH on Linux) and Default File Copier (SCP on Linux).

Setup creates the project config and a local resource model describing the Rundeck server node.

CLI:

```bash
rd projects create -p MyProject
rd projects create -p MyProject -- \
   --project.label="My Project" \
   --project.ssh-keypath=/path/to/.ssh/id_rsa \
   --resources.source.2.type=directory \
   --resources.source.2.config.directory=/path/to/projects/MyProject/resources.d
```

The `--` separates rd options from project configuration properties. Run `rd projects create help` for syntax.

API:

```
POST /api/13/projects
Content-Type: application/json

{ "name": "MyProject", "config": { "project.label":"My Project" } }
```

Verify the project appears in the project picker or with `rd projects list`.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Project Create: New Project fields and their descriptions, Job Group Expansion Level values 1/0/-1, default SSH node executor and SCP file copier on Linux, rd projects create with -- separated properties, directory resource source keys, and POST /api/13/projects body. Example key path replaced with a placeholder. Nothing removed.

Method: documentation only; no commands were run.
