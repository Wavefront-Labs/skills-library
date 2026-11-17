---
id: computing-software.it-support-helpdesk.desktop-support.rebuilding-a-corrupt-windows-profile
name: rebuilding-a-corrupt-windows-profile
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, profile-rebuild, user-profile, temporary-profile, profilelist, robocopy, windows, profile-deletion]
level: practitioner
status: gated
description: "Rebuild a corrupt or temporary Windows user profile without losing data: back up, remove the profile cleanly via CIM or ProfileList, sign in fresh, copy back only user data."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/remove-ciminstance"
  - "https://learn.microsoft.com/en-us/previous-versions/windows/desktop/userprofileprov/win32-userprofile"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# rebuilding-a-corrupt-windows-profile

**Back up first.** Removing a profile deletes the user's local data. Do not
proceed until the backup in step 2 is complete and checked.

## Confirm it is the profile
- "You've been signed in with a temporary profile", Start menu or search
  broken for one user only, or app settings reset at every sign-in. Another
  user on the same PC works fine.
- Rule out the cheap causes first: free disk space, a pending reboot, and a
  fresh sign-in after a restart.

## Rebuild
1. Have the user sign out; sign in as a different admin. Reboot if the profile
   is still loaded.
2. Back up the folder:
```cmd
robocopy "%SystemDrive%\Users\jsmith" "<BACKUP_DIR>\jsmith" /E /COPY:DAT /XJ /R:1 /W:1 /XF NTUSER.DAT* UsrClass.dat* /LOG:"<BACKUP_DIR>\jsmith.log"
```
   `/E` copies subdirectories including empty ones, `/XJ` excludes junction
   points, `/R:1 /W:1` stops one-million-retry hangs (the defaults are 1,000,000
   retries and 30 seconds), `/XF` excludes the named files, and `/COPY:DAT`
   (data, attributes, time stamps) is the default.
3. Remove the profile properly rather than only deleting the folder, so the
   profile registration goes with it:
```powershell
Get-CimInstance Win32_UserProfile | Where-Object LocalPath -like '*\jsmith' | Remove-CimInstance
```
   Removing the profile this way also deletes its folder and registration
   (gated: unconfirmed, source is paywalled or blocked). Microsoft's pages for the class and cmdlet do not
   describe what the delete does, so check the result before telling the user.
4. The user signs in; a fresh profile is created. Let OneDrive and browser
   sync finish.
5. Copy back only data: Desktop, Documents, Downloads, Pictures, Favorites,
   plus any application data the user confirms they need.
6. Never copy back `NTUSER.DAT` or the whole AppData tree; that brings the
   corruption back.

## Gotchas
- With OneDrive Known Folder Move, Desktop and Documents are already in the
  cloud; check before copying so you do not create duplicates.
- PST files and local databases may sit outside the profile; ask the user.

## Verify
The user signs in to a normal (non-temporary) profile, Start and search work,
data is present, and the backup is kept for an agreed period then deleted.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn robocopy, Remove-CimInstance and Win32_UserProfile pages as published October 2026. Confirmed: robocopy /E, /XJ, /XF, /R, /W (defaults 1,000,000 and 30), /COPY default DAT, /LOG; Remove-CimInstance exists and Win32_UserProfile has SID and LocalPath. Not confirmed: that Remove-CimInstance on Win32_UserProfile deletes the folder and the profile registration (marked gated). Removed: ProfileList .bak registry repair, event IDs 1511/1515/1500, Sticky Notes, Outlook signature and browser bookmark paths, cached-credential note.

Method: documentation only; no commands were run.
