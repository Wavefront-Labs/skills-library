---
id: computing-software.digital-privacy-hygiene.vpn-tools.ublock-origin-filter-lists-and-medium-mode
name: ublock-origin-filter-lists-and-medium-mode
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, ublock-filter-lists, ublock-origin, tracker-blocking, medium-mode, dynamic-filtering, ublock-origin-lite, manifest-v3]
level: practitioner
status: docs-checked
description: "Tune uBlock Origin: filter list choices and risks, medium mode (block 3rd-party scripts and frames) with per-site noop fixes, and what uBO Lite and Manifest V3 change."
sources:
  - "https://github.com/gorhill/uBlock/wiki/Blocking-mode:-medium-mode"
  - "https://github.com/gorhill/uBlock/wiki/Dashboard:-Filter-lists"
  - "https://www.privacyguides.org/en/browser-extensions/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uBlock Origin filter lists and medium mode

**Goal:** get more out of uBO than the defaults without breaking the web.

## Filter lists (Dashboard, Filter lists)
- uBO ships with a default selection including the uBlock filters; Peter Lowe's Ad and tracking server list is enabled by default, Dan Pollock's hosts file is not.
- Optional lists include AdGuard ones such as AdGuard/uBO - URL Tracking Protection. Commit changes with "Apply change".
- More lists raise the chance of breakage and list conflicts; quality matters (EasyList and AdGuard lists are actively maintained). If you prune, keep the uBlock filters. Privacy Guides adds that extra lists slow things and may increase attack surface: apply only what you need.
- "Update now" appears only when a list is out of date. Duplicate filters across lists are discarded, so a list showing "0 filters used" is not necessarily broken.

## Medium mode (advanced)
Blocks third-party scripts and frames by default; passive third-party resources (images, CSS) are not blocked.
1. Settings: tick "I am an advanced user".
2. 3rd-party filters: enable all uBO lists, EasyList, Peter Lowe's, EasyPrivacy and Online Malicious URL Blocklist.
3. My rules: add `* * 3p-script block` and `* * 3p-frame block`.
A blue badge on the toolbar button shows medium mode is active.

Expect breakage ("high likelihood"), less than hard mode and less over time as you build rules. To relax one site: set a local noop rule on the 3rd-party script cell (optionally 3rd-party frames too, which rarely breaks sites), then click the padlock to make it permanent. Local rules apply only to that site.

## uBO Lite / Manifest V3
- uBO Lite is the MV3 build (Chrome, Edge, Safari). Chrome supports only MV3 extensions.
- Privacy Guides recommends it only if you will not add extra filter lists and do not need dynamic filtering or the network logger. Basic level needs no broad permissions; Optimal and Complete do, and can be raised per site.
- Filter updates arrive with extension releases, and only "safe rules" can be updated. MV3 has a hard rule limit.
- Brave and Opera committed to keeping MV2 support as long as they can. For medium mode you need the full uBO.

## Verify
- [ ] Badge shows medium mode active (if used).
- [ ] Your daily sites work and permanent noop fixes are saved.

## Checked
Method: 2026-11-08 read all three cited pages. Medium-mode steps, list advice and MV3 notes follow them. Removed as unsupported: the recommendation to add Annoyances/EasyList Cookie/regional lists, the element picker section, "Firefox remains the place" for full uBO, and "fixes within the first week".
