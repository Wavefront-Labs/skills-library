---
id: computing-software.web-development.appwrite.appwrite-migrations-self-hosting
name: appwrite-migrations-self-hosting
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, migrations, self-hosting, docker, backups]
level: advanced
status: docs-checked
description: "Migrate data into Appwrite from other platforms and install or back up a self-hosted instance with Docker."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/migrations/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/self-hosting/installation/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/self-hosting/production/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move to or run your own Appwrite.

Migrations: the service moves projects from Firebase, Supabase and Nhost, between self-hosted and Cloud projects in either direction, between two self-hosted instances, or duplicates a project on the same instance. It moves accounts, database rows and storage files to a new or existing Appwrite project. Per source: Firebase, Supabase and Nhost migrate users, databases and files automatically, rows only partially, and functions manually; Cloud and Self hosted sources migrate users, databases, rows, files, functions and sites. Limitations: fields such as `$createdAt` and `$updatedAt` may not be transferred, complex databases and unique features such as functions may need manual migration, and you should validate permissions and data integrity. Usage during a migration into Cloud does not count towards Cloud usage charges, but your source vendor may charge for data transfer.

Self-hosted install (Docker): requirements are 2 CPU cores, 4GB of RAM, 2GB of swap, an operating system that supports Docker, Docker Compose Version 2 and a recent enough Docker Engine. The installer runs a web setup wizard on port 20080, which must be open in your firewall on a remote server (you can close it afterwards). On macOS and Linux:

`docker run -it --rm --publish 20080:20080 --volume /var/run/docker.sock:/var/run/docker.sock --volume "$(pwd)"/appwrite:/usr/src/code/appwrite:rw --entrypoint="install" appwrite/appwrite:1.9.6`

The page has Windows CMD and PowerShell variants. Then open `http://localhost:20080`. The wizard's first step sets the Hostname and the Database (MongoDB or MariaDB, MongoDB selected by default); the second shows a generated secret API key used to encrypt sensitive data, which you cannot see again after proceeding, so copy it. The uninstall command permanently deletes all Appwrite data, so back up first.

Production: the preparation page lists a checklist (security, scaling, rate limits, email delivery, error monitoring, backups, updates, debugging) and advises backing up regularly with automated strategies; the detailed pages are not covered here.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages Migrations, Installation and Production preparation: the sources table and limitations, the charges note, system requirements, port 20080, the macOS and Linux command, the wizard's database and API key steps, the uninstall warning and the production checklist. Removed: the `mongodump` and `mysqldump` backup commands and the list of Docker volumes (not on these pages), the "Cloud backup policies do not apply" gotcha, and the Verify step about admin sign-up.
Method: documentation only; no commands were run.
