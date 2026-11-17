---
id: computing-software.collaboration-platform-administration.nextcloud.sharing-policy-admin-settings
name: sharing-policy-admin-settings
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [file-sharing, share-api, public-links, resharing, group-restrictions]
level: practitioner
status: docs-checked
description: "Set the Nextcloud Sharing policy: Share API, resharing, group limits, link shares, public uploads, enforced link passwords and excluded groups."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/file_sharing_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide who may share what, from the Sharing section of the admin settings.

Users can share with groups and users on the same server, with users on other servers through federated sharing, and with non-users through public links.

Master switch: `Allow apps to use the Share API`. If unchecked, nobody can create shares.

Under it:
- `Allow resharing`: users may re-share files shared with them.
- `Allow sharing with groups`.
- `Restrict users to only share with users in their groups`: confines sharing to group membership. An optional list of ignored groups removes those groups from the membership test. This does not apply to Federated Cloud sharing; if that is enabled, users can still share with any users on any instances via a remote share.

Link and email shares:
- `Allow users to share via link and email`: public shares for non-users.
- `Allow public uploads`: anyone can upload to public shares.
- `Always ask for a password`: prompts the user to set one.
- `Enforce password protection`: all public links need a password. This does not apply to local user and group shares.
- `Exclude groups from creating link shares`: the settings above do not apply to those groups.

Blocking sharing:
- `Exclude groups from sharing`: members cannot create shares but can still receive them.


Check: sign in as a user in an excluded group and confirm the share action is not offered, while a share sent to them still arrives.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/file_sharing_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
