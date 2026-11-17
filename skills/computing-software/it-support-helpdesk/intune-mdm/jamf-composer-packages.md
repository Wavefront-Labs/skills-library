---
id: computing-software.it-support-helpdesk.intune-mdm.jamf-composer-packages
name: jamf-composer-packages
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, jamf-composer, jamf-pro, macos-packages, pkg, package-signing, distribution-point]
level: practitioner
status: draft
description: "Build and ship macOS packages for Jamf Pro: Composer snapshots vs pkgbuild, signing with a Developer ID Installer cert, uploading, and install policy checks."
sources:
  - "https://learn.jamf.com/en-US/bundle/composer-user-guide-current/page/About_Composer.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Packages.html"
  - "https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-composer-packages

Jamf Pro installs software from packages (`.pkg`, or `.dmg` for Composer-style file drops)
stored on a distribution point (Jamf Cloud Distribution Service or file share).

## Prefer the vendor package
If the vendor ships a signed flat `.pkg`, upload it as-is. Repackaging is for apps
delivered as drag-to-Applications `.app` in a DMG, or for adding config files.

## Composer
1. **Snapshot**: Composer records the file system before and after you install/configure,
   then shows the diff as a package source. Remove noise (caches, `/private/var`,
   user-specific prefs) before building.
2. **Drag and drop**: drag an `.app` from `/Applications` into Composer; it builds a source
   with correct paths. Set ownership `root:wheel` and permissions 755 for apps.
3. Add pre/postinstall scripts in the source (Scripts folder) if needed.
4. Build as PKG (flat package). Composer can sign with an installer certificate if
   configured.

## pkgbuild alternative (scriptable)
```
pkgbuild --component "/Applications/Contoso.app" --install-location /Applications \
  --identifier com.contoso.app --version 5.2.0 Contoso-5.2.0.pkg
productsign --sign "Developer ID Installer: Your Org (TEAMID)" Contoso-5.2.0.pkg Contoso-5.2.0-signed.pkg
pkgutil --check-signature Contoso-5.2.0-signed.pkg
```

## Signing
- Packages installed by Jamf policy via the Jamf agent don't strictly need signing, but
  packages installed by **InstallEnterpriseApplication** MDM command (PreStage enrollment
  packages) **must** be signed with a Developer ID Installer or a trusted cert.
- Notarization is not required for MDM/agent installs but helps if users open the pkg.

## Upload and deploy
1. Settings > Computer management > Packages > New: upload, set category, priority,
   "Fill user templates" (only for DMGs that need it).
2. Policy: Packages payload > Install; scope; trigger (recurring check-in, enrollment,
   custom event, Self Service); frequency Once per computer; run Update inventory.

## Troubleshooting
- Policy logs (Computers > the Mac > History > Policy logs) show install output.
- On the Mac: `/var/log/jamf.log` and `/var/log/install.log`; run
  `sudo jamf policy -event <trigger> -verbose` to test.
- "Package is not signed" during PreStage: sign it.
- Installs but app won't open: quarantine or Gatekeeper; check `spctl -a -vv
  /Applications/Contoso.app`.

## Gotchas
- Snapshots taken on a dirty Mac pick up junk; use a clean VM.
- Packages with `/Users/<name>` paths are wrong; use User Template or a login script.
- Update app versions with a new package and a new policy or Patch Management title.

## Verify
Pilot Mac installs via the policy without user interaction, the app launches, the policy
log shows success, and inventory reports the new version.
