---
id: computing-software.it-support-helpdesk.remote-support-tools.remote-control-of-macos
name: remote-control-of-macos
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, macos-remote-control, screen-recording-permission, accessibility-permission, pppc, apple-remote-desktop, screen-sharing]
level: practitioner
status: draft
description: "Remote-control Macs reliably: Screen Recording and Accessibility permissions, PPPC limits, Screen Sharing/ARD via kickstart, vendor tools, and the 'can see but can't click' fix."
sources:
  - "https://support.apple.com/guide/mac-help/turn-screen-sharing-on-or-off-mh11848/mac"
  - "https://support.apple.com/guide/deployment/privacy-preferences-policy-control-payload-dep38df53c2a/web"
  - "https://support.apple.com/en-us/108030"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# remote-control-of-macos

macOS privacy controls (TCC) mean a remote tool needs explicit permission to capture the
screen and to send clicks/keys. Missing permissions are the cause of most Mac remote
session failures.

## Permissions a remote tool needs
- **Screen & System Audio Recording** (Screen Recording): to see the screen. Without it,
  the helper sees only the wallpaper or a black screen.
- **Accessibility**: to control mouse and keyboard. Without it: "can see but can't click".
- Sometimes **Full Disk Access** (file transfer to protected folders) and **Input
  Monitoring**.
System Settings > Privacy & Security > each category > enable the app (admin password
needed). The app usually must be restarted after granting.

## MDM limits
A PPPC (Privacy Preferences Policy Control) profile can **grant Accessibility** to a
signed app, but Apple does **not** allow MDM to grant Screen Recording; it can only allow a
standard user to approve it themselves (`ScreenCapture` with `Allow Standard User To Set
System Service`). So the user must click Allow once. Deploy PPPC with the vendor's bundle ID
and code requirement (`codesign -dr - /Applications/Tool.app`).

## Built-in Screen Sharing / ARD
- Enable: System Settings > General > Sharing > Screen Sharing (or Remote Management for
  ARD). Remote: `vnc://hostname` from Finder > Go > Connect to Server, or Apple Remote
  Desktop.
- Scripted (needs MDM-enabled Remote Management on macOS 12.1+ for the kickstart to fully
  work):
  ```
  sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart \
    -activate -configure -access -on -privs -all -users <admin_shortname> -restart -agent
  ```
  On recent macOS, enabling Remote Management purely by kickstart is restricted; use the
  MDM `EnableRemoteDesktop` command (Jamf/Intune support) and the PPPC profile.

## Vendor tools (TeamViewer, Splashtop, ScreenConnect, Intune Remote Help)
Install the vendor's Mac agent; it shows a permissions checklist on first launch. For
unattended access, grant permissions during setup with the user present, or via PPPC
(Accessibility) plus a one-time user approval (Screen Recording).

## Common issues
- Black screen: Screen Recording missing, or the Mac is at the login window and the tool
  lacks the login-window helper (needs its daemon component installed).
- Lost control after macOS update: Apple sometimes resets TCC approvals; re-approve.
- Retina scaling makes sessions slow: lower the session resolution/quality in the tool.

## Verify
In a test session you see the live screen, can click and type, can reach the login window
after a logout (for unattended tools), and permissions show enabled in Privacy & Security.
