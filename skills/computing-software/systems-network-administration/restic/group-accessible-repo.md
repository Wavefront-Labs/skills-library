---
id: computing-software.systems-network-administration.restic.group-accessible-repo
name: group-accessible-repo
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, group-access, permissions, setgid, local-backend, sftp]
level: advanced
status: docs-checked
description: "Share one local restic repository between several Unix users with a group, setgid directories and group-readable files."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group-accessible repositories

Since restic 0.14, local and SFTP repositories can be made accessible to all members of a UNIX group on the repository host. Run `restic init` first if needed, then give the repository files group permissions:

```
chgrp -R restic-users /srv/restic-repo
find /srv/restic-repo -type f -exec chmod 440 '{}' \;
find /srv/restic-repo -type d -exec chmod 2770 '{}' \;
```

Why these modes:

- The group read permission on the `config` file tells restic to create all future files and directories in the repository with group-read permission.
- The setgid bit on directories (`2770`) causes restic to set the group of each newly created file to the group of its parent directory, so files stay accessible to the group whoever created them.

Manage who is in the group with `usermod` on Linux.

## Over SFTP

For a repository accessed via SFTP, the user used for the SFTP connection should belong to the group (here `restic` would be a member of `restic-users` on `repohost`):

```
restic -r sftp:restic@repohost:/srv/restic-repo backup /path/to/data
```

## Checked

Checked 2026-11-08 against the restic Preparing a new repository page (030_preparing_a_new_repo), the Group accessible repositories section read in full (the rest of the page was read in part only: local, SFTP and REST sections). Confirmed: available since 0.14 for local and SFTP repositories, the chgrp and find/chmod 440 and 2770 commands, the explanation of the config file group-read hint and the setgid bit, usermod, and the SFTP user's group membership. Removed: the second-user ownership check, which the page does not state.

Method: documentation only; no commands were run.
