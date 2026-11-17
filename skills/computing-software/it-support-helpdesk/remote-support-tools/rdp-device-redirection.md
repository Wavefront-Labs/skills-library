---
id: computing-software.it-support-helpdesk.remote-support-tools.rdp-device-redirection
name: rdp-device-redirection
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rdp-redirection, clipboard-redirection, printer-redirection, drive-redirection, rdp-properties, rdp]
level: practitioner
status: draft
description: "Troubleshoot RDP redirection: clipboard, drives, printers, USB, cameras and audio; client options vs host GPO vs RDS/AVD RDP properties, and the rdpclip restart fix."
sources:
  - "https://learn.microsoft.com/en-us/azure/virtual-desktop/rdp-properties"
  - "https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/rdp-files"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/cannot-copy-paste-files-remote-desktop"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# rdp-device-redirection

Redirection decides which local resources (clipboard, disks, printers, devices) appear
inside a remote session. Three layers must all allow it: client, host policy, and (for
RDS collections/AVD host pools) the published RDP properties.

## Layer 1: client
- mstsc > Show Options > **Local Resources**: Clipboard, Printers, More (Drives, Smart
  cards, Ports, PnP devices), Remote audio, Webcams.
- `.rdp` file lines, e.g. `redirectclipboard:i:1`, `redirectprinters:i:1`,
  `drivestoredirect:s:*`, `audiocapturemode:i:1`, `camerastoredirect:s:*`,
  `usbdevicestoredirect:s:*`.

## Layer 2: host policy (GPO / Intune)
Computer > Administrative Templates > Windows Components > Remote Desktop Services >
Remote Desktop Session Host > **Device and Resource Redirection**: "Do not allow
Clipboard redirection", "Do not allow drive redirection", "Do not allow supported Plug
and Play device redirection"; **Printer Redirection**: "Do not allow client printer
redirection", "Use Remote Desktop Easy Print printer driver first". Security baselines
often disable drive redirection deliberately.

## Layer 3: RDS collection / AVD host pool
- RDS: Server Manager > Collection > Properties > Client Settings (redirection checkboxes).
- AVD: host pool > RDP Properties > Device redirection (custom string such as
  `redirectclipboard:i:0;drivestoredirect:s:`). These override the user's client choices.
- Newer AVD/Windows 365 also have Intune "clipboard transfer direction" settings
  (client-to-server only, text only).

## Common fixes
- **Copy/paste stopped mid-session**: restart `rdpclip.exe` in the session (Task Manager >
  end rdpclip > Run `rdpclip`). Large file copies via clipboard are unreliable; use
  drive redirection or OneDrive.
- **Printer missing**: Easy Print requires the client to have a working local driver;
  check event logs under PrintService > Admin on the host; third-party drivers on the host
  may be blocked by Point and Print restrictions.
- **Webcam/mic in Teams on AVD**: use Teams media optimization (WebRTC redirector)
  instead of camera redirection.
- **USB device not redirected**: RemoteFX USB redirection needs the client policy
  "Allow RDP redirection of other supported RemoteFX USB devices" and host support;
  prefer high-level redirection (printer, drive, smart card) where possible.

## Gotchas
- Drive redirection is a data exfiltration path; security may block it on purpose. Check
  before "fixing".
- Smart card redirection needed for PIV sign-in inside sessions; disabling it breaks
  admin tiers that use smart cards.

## Verify
Inside the session, the resource appears (This PC shows the client drive "C on CLIENT",
printer list shows redirected printers, clipboard works both ways) and policy results
(`gpresult /h`) show the intended settings.
