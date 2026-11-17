---
id: computing-software.digital-privacy-hygiene.vpn-tools.tor-downloads-and-external-app-leaks
name: tor-downloads-and-external-app-leaks
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, tor-download-safety, tor-browser, dangerzone, opsec]
level: practitioner
status: draft
description: "Handle files downloaded over Tor so documents and media opened in external apps don't reveal your real IP, using offline viewing, Tails or Dangerzone."
sources:
  - "https://support.torproject.org/"
  - "https://tb-manual.torproject.org/known-issues/"
  - "https://dangerzone.rocks/"
  - "https://tails.net/doc/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Downloads and external apps leaking outside Tor

**Goal:** keep anonymity after the download, when the file is opened by software that does not use Tor.

## The risk
Tor Browser only protects traffic it makes itself. Documents (PDF, DOCX, ODT), media files and torrent files opened in
other apps can load remote resources, call home, or run macros, connecting directly from your real IP. Tor Browser
warns about this when you download such files.

## Safe options, from simplest
1. **View inside Tor Browser** where possible (its built-in PDF viewer).
2. **Disconnect from the network** before opening in an external app, and close the app before reconnecting.
3. **Tails**: all apps are forced through Tor or blocked, so external apps cannot leak your IP. Amnesic by default.
4. **Dangerzone** converts untrusted PDFs, office docs and images into a safe flattened PDF in a sandbox with no
   network access; open the output instead of the original.
5. A disposable VM with networking off (or Whonix, where the workstation can only reach Tor).

## Never
- Open torrents found over Tor in a normal BitTorrent client: it announces your real IP to the swarm.
- Enable macros in a downloaded document.
- Install browser plugins/add-ons to play media in Tor Browser.

## Metadata going the other way
Before uploading files over Tor, strip metadata (EXIF GPS, author names) with `mat2` (included in Tails) or
equivalent; Tor hides the connection, not what's in the file.

## Gotchas
- Some file types are opened automatically by the OS preview pane (Windows Explorer, macOS Quick Look). Don't preview
  untrusted downloads on a networked host.
