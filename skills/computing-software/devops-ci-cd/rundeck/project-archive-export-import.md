---
id: computing-software.devops-ci-cd.rundeck.project-archive-export-import
name: project-archive-export-import
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, project-archive, rdproject-jar, export-archive, import-archive]
level: practitioner
status: docs-checked
description: "Export a Rundeck project to an archive and import it into another project for backup, database migration or upgrades; know what the archive omits."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/maintenance/backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Rundeck 1.4.4 a project's database contents can be exported to an archive and imported into another project. Uses: backup, migrating between database backends, upgrading between versions.

Export: click "Admin" in the page header, then the link under "Export Archive". The archive contains all job definitions, all executions (job and ad hoc), execution output logs, and history reports.

It does not contain:
- `project.properties` under `$RDECK_BASE/projects/[name]/etc`
- resource definitions (such as `resources.xml` or resources from external providers)

Back those up separately and reconfigure them on the target.

Import: Admin, then "Import Archive", choose the file (ends in `.rdproject.jar`), click "Import". The import:
- creates jobs not in the project with a new unique UUID
- updates jobs whose group and name match
- creates new executions and output log files on disk
- creates new history reports

Keys are separate. File-based Key Storage (`rundeck.storage.provider.1.type=file`, or no such line) survives an upgrade on the same filesystem. DB storage (`type=db`) carries over with a full DB dump. If you move to a different database provider you may need to recreate keys manually.

## Checked

2026-11-04: export contents and omissions, import behaviour and key scenarios confirmed against the Backup and Recovery page (Project Import and Export section).
Method: documentation only; no commands were run.
