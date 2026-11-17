---
id: computing-software.systems-network-administration.windows-server.folder-redirection-group-policy
name: folder-redirection-group-policy
category: computing-software
field: systems-network-administration
product: windows-server
tags: [group-policy, gpo, folder-redirection, offline-files, file-server]
level: practitioner
status: docs-checked
description: "Configure Folder Redirection for Documents, Desktop and AppData: share and NTFS permissions, basic vs advanced targeting, offline files and moving targets."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/folder-redirection/deploy-folder-redirection
  - https://learn.microsoft.com/en-us/windows-server/storage/folder-redirection/folder-redirection-rup-overview
  - https://learn.microsoft.com/en-us/windows-server/storage/folder-redirection/deploy-primary-computers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Folder Redirection with Group Policy

## Share and permissions (the part people get wrong)
Create `\\FS01\Redirect$` with:
- NTFS on the root: disable inheritance (convert to explicit); SYSTEM Full Control (this folder, subfolders and files);
  Administrators Full Control (this folder only); Creator/Owner Full Control (subfolders and files only); the redirected
  users group **List folder / read data, Create folders / append data, Read attributes, Read extended attributes** on
  **this folder only**; remove all other accounts. Use the Microsoft table that matches your server role (the permissions
  differ when the file server also runs Remote Desktop Services).
- Clear **Enable continuous availability** on the share (it can cause performance problems with Folder Redirection and
  Offline Files); optionally enable access-based enumeration.
- If the share uses DFS Namespaces or DFS Replication, users must reach a single target only.

## Policy
User Configuration > Policies > Windows Settings > Folder Redirection > Documents (and Desktop, etc.):
- Setting: **Basic - Redirect everyone's folder to the same location** (or an advanced per-group setting).
- Target: "Create a folder for each user under the root path", root path such as `\\fs1.corp.example.com\users$`.
- Optional Policy Removal: **Redirect the folder back to the local userprofile location when the policy is removed**,
  which makes behaviour more predictable.
- Scope the GPO with security filtering to the intended group, and give Authenticated Users delegated Read on the GPO
  (required since MS16-072).

## Offline Files
Offline Files is enabled by default for redirected folders on Windows client computers and disabled on Windows Server;
the policy is **Allow or disallow use of the Offline Files feature**.

## Moving to a new server
Plan the move of data to the new share (single DFS target at a time) and test with a pilot group before changing the
root path in the GPO.

## Troubleshooting
Use `gpresult /h` to confirm the GPO applied to the user, and check that the user has Read on the GPO.

## Verify
- [ ] The redirected folder's Location tab shows the file share path instead of a local path.
- [ ] Users cannot browse other users' folders.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed in Deploy Folder Redirection with Offline Files: the NTFS permission table (System, Administrators, Creator/Owner, users group with list/create/read attribute rights), disabling continuous availability, optional access-based enumeration, single DFS target, Offline Files defaults and policy name, the Basic setting and Create a folder for each user option, Policy Removal option, and Authenticated Users Read on the GPO (MS16-072); the Location tab check comes from the primary computers page. Removed as unconfirmed: the share-level Authenticated Users Full Control, Grant the user exclusive rights and Move the contents options, the VDI Offline Files policy path, the robocopy migration shortcut, events 501 and 502, Always wait for the network, and the User Shell Folders registry check.

Method: documentation only; no commands were run.
