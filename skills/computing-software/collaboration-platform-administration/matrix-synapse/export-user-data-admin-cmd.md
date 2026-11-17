---
id: computing-software.collaboration-platform-administration.matrix-synapse.export-user-data-admin-cmd
name: export-user-data-admin-cmd
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, export-data, admin-cmd, gdpr, user-data, media-ids, data-export]
level: advanced
status: docs-checked
description: "Export a user's data with python -m synapse.app.admin_cmd export-data: output layout, media metadata only, encrypted media stays encrypted."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/admin_faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Synapse ships a command to export the data held for one user. It takes the homeserver config and the user's full Matrix ID:

```console
python -m synapse.app.admin_cmd -c <config_file> export-data <user_id> --output-directory <directory_path>
```

With Poetry, prefix with `poetry run`. The output directory should be empty. If you omit `--output-directory`, Synapse creates a temporary directory whose name starts with `synapse-exfiltrate` in `/tmp`, `/var/tmp` or `/usr/tmp`, in that order.

Layout of the export:

```
output-directory
├───rooms
│   └───<room_id>
│       ├───events
│       ├───state
│       ├───invite_state
│       └───knock_state
├───user_data
│   ├───account_data
│   │   ├───global
│   │   └───<room_id>
│   ├───connections
│   ├───devices
│   └───profile
└───media_ids
    └───<media_id>
```

The `media_ids` folder holds only metadata about media the user uploaded, not the files. It covers only media that Synapse itself manages; if another repository such as matrix-media-repo is in use, export that separately. Media sent in encrypted rooms can only be retrieved in encrypted form.

To fetch the files, request each ID from the media repository (or a media worker). The FAQ supplies a Bash loop that, for each file name in the `media_ids` directory, downloads `<repository_url>/_matrix/media/v3/download/<server_name>/<media_id>` with `wget` into a target directory and reports any ID it could not download. The script takes four parameters: source directory, target directory, repository URL and your `server_name`.

## Checked

Method: docs-checked 2026-11-09 against docs/usage/administration/admin_faq.md (Synapse develop branch, raw markdown, read in full).
