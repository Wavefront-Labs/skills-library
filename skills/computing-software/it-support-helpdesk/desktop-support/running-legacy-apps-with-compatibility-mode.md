---
id: computing-software.it-support-helpdesk.desktop-support.running-legacy-apps-with-compatibility-mode
name: running-legacy-apps-with-compatibility-mode
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, application-troubleshooting, compatibility-mode, program-compatibility-troubleshooter, appcompatflags, shims, compatibility-administrator, runasinvoker, ie-mode, legacy-apps]
level: practitioner
status: draft
description: "Keep legacy apps running on Windows 10/11: compatibility mode, RunAsInvoker shims instead of admin rights, folder permissions, and Edge IE mode."
sources:
  - "https://support.microsoft.com/en-us/windows/make-older-apps-or-programs-compatible-with-windows-783d6dd7-b439-bdb0-0490-54eea0f45938"
  - "https://learn.microsoft.com/en-us/windows/deployment/planning/compatibility-administrator-users-guide"
  - "https://learn.microsoft.com/en-us/deployedge/edge-ie-mode"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# running-legacy-apps-with-compatibility-mode

Goal: make a legacy app work for standard users without handing out local
admin rights.

## Try in this order
1. **Vendor update** — check for a supported version first; compatibility
   fixes are a bridge, record them as technical debt.
2. **Program Compatibility Troubleshooter** (right-click exe →
   Troubleshoot compatibility) — tries the common modes.
3. **Compatibility tab** — "Run in compatibility mode for Windows 7/8",
   reduced colour, 640×480, **High DPI override** ("System (Enhanced)") for
   blurry UIs, "Run as administrator" (avoid).
4. Applied per user or all users ("Change settings for all users"); stored
   in `HKCU|HKLM\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers`
   as a string like `~ WIN7RTM HIGHDPIAWARE` — deployable by GPO/Intune
   registry.

## The "needs admin" app
Most legacy apps demand admin because they write to their install folder
or HKLM. Fix the cause:
- Run **Process Monitor** filtered on the exe and `Result is ACCESS DENIED`
  → grant Users Modify on just that folder/key.
- Or apply the **RunAsInvoker** shim (Compatibility Administrator → create
  application fix → RunAsInvoker; plus `VirtualRegistry` / file
  virtualization fixes) and deploy the `.sdb` with
  `sdbinst -q app_fix.sdb`.
- Quick test without a shim: `cmd /c "set __COMPAT_LAYER=RunAsInvoker && start app.exe"`.

## Legacy web apps (ActiveX, IE-only)
Edge **IE mode**: Enterprise Mode Site List XML (pushed via the
"Configure the Enterprise Mode Site List" policy) with `<open-in>IE11</open-in>`
per site. Test locally with `edge://compat`.

## Gotchas
- 16-bit apps do not run on 64-bit Windows at all — VM or replacement.
- Compatibility mode "Windows XP" lies about the OS version; installers that
  check for a minimum version may then refuse.
- Shim databases must be redeployed after major Windows feature updates if
  the app fails again.

## Verify
A standard user (no admin token) launches the app, completes a full business
workflow (open, save, print), and settings persist across restarts.
