---
id: computing-software.it-support-helpdesk.desktop-support.onedrive-known-folder-move
name: onedrive-known-folder-move
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, known-folder-move, onedrive, kfm, folder-redirection, intune, group-policy]
level: practitioner
status: docs-checked
description: "Deploy and troubleshoot OneDrive Known Folder Move: silent and prompt policies with tenant ID, rollout limits, and conflicts with Windows folder redirection."
sources:
  - "https://learn.microsoft.com/en-us/sharepoint/redirect-known-folders"
  - "https://learn.microsoft.com/en-us/sharepoint/use-group-policy"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# onedrive-known-folder-move

## Policies (Group Policy, or Intune with the OneDrive administrative template)
| Setting | Registry value under `HKLM\SOFTWARE\Policies\Microsoft\OneDrive` | Effect |
|---|---|---|
| Silently move Windows known folders to OneDrive | `KFMSilentOptIn` = tenant ID (string) | Moves Desktop, Documents and Pictures with no user interaction |
| Same policy, notification | `KFMSilentOptInWithNotification` = 1 | Shows a notification after a successful move |
| Same policy, choose folders | `KFMSilentOptInDesktop`, `KFMSilentOptInDocuments`, `KFMSilentOptInPictures` = 1 | If none is set, all three move |
| Prompt users to move Windows known folders to OneDrive | `KFMOptInWithWizard` = tenant ID | Shows a prompt; a reminder stays in the Activity Center until they move the folders |
| Prevent users from redirecting known folders back to their PC | `KFMBlockOptOut` = 1 | Disables the Stop protecting button; users get an error if they try to stop |
| Silently sign in users with Windows credentials | `SilentAccountConfig` = 1 | Works on PCs joined to Microsoft Entra ID; Microsoft recommends enabling it |

- After a folder has moved, the silent policy does not affect it again, even if you clear the folder's checkbox.
- Microsoft recommends pairing the silent policy with the prompt policy, so users are prompted to fix an error when the silent move fails.
- The Group Policy setting User Configuration > Administrative Templates > Desktop > Prohibit User from manually redirecting Profile Folders must be Disabled or Not configured, or folders will not move.
- The block-move policy (named BlockKnownFolderMove) writes the registry value `KFMBlockOptIn`; look for that name when verifying it.

## Rollout limits (Microsoft guidance)
Silent policy: at most 1,000 existing devices a day and 4,000 a week (Windows and macOS combined). Prompt policy: existing devices only, at most 5,000 a day and 20,000 a week. With many files per user, roll out slowly and consider temporarily limiting the sync app upload rate. Known Folder Move does not work for users syncing OneDrive files in SharePoint Server.

## Check a device
OneDrive sync app settings, Backup tab, Manage backup shows which folders are protected.

## Why a move fails or stalls
- Folders already redirected with Windows Folder Redirection Group Policy. Microsoft's steps: if redirected to OneDrive, disable the folder redirection policy, leave the contents in OneDrive, then enable Known Folder Move. If redirected to a local path, disable the policy, leave the contents, and Known Folder Move moves them. If redirected to a network file share, first copy the share content into the user's existing Documents, Pictures and Desktop folders in OneDrive with Migration Manager (do not select Preserve file share permissions if Migration Manager creates the folders), then disable the redirection policy, then enable Known Folder Move.
- Folders currently redirected to OneDrive in another organisation: redirecting to your organisation creates new empty folders, and the user must migrate files by hand. Disable the other redirect first if possible.
- Music and Videos are not affected by the OneDrive policies, so they can stay on Windows Folder Redirection.
- For other blockers, Microsoft points to its "Fix problems with folder protection" article.

## Verify
Manage backup shows the folders protected, and a test file in a known folder appears in OneDrive on the web.

## Checked
Date: 2026-11-09. Confirmed in the Microsoft Learn pages "Redirect and move Windows known folders to OneDrive" and "Use Group Policy to control OneDrive sync app settings": policy names, registry values, silent and prompt behaviour, rollout limits, the Prohibit User policy conflict, the transition steps from Windows Folder Redirection, other-organisation redirect, Backup tab and Manage backup. Removed as unconfirmed on those pages: where to find the tenant ID, silent opt-in "waits and retries", the User Shell Folders registry check, the Sync and backup menu wording, the open-file, path-length and file-size causes, and the Files On-Demand, move-back and kiosk gotchas.
Method: docs-checked 2026-11-09 against the two Microsoft Learn pages listed in sources, downloaded and read (the group policy page by targeted reads of the Known Folder Move and silent sign-in sections).
