---
id: computing-software.digital-privacy-hygiene.password-managers.keepassxc-browser-integration-and-auto-type
name: keepassxc-browser-integration-and-auto-type
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, keepassxc-auto-type, keepassxc-browser, keepassxc, kdbx, autofill, auto-type-sequence, window-title-matching]
level: practitioner
status: docs-checked
description: "Connect KeePassXC to browsers with KeePassXC-Browser and fill desktop apps with Auto-Type sequences and window matching, without typing into the wrong window."
sources:
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_browser_integration"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_auto_type"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KeePassXC browser integration and Auto-Type

**Goal:** cloud-manager convenience from a local KDBX vault. Auto-Type is a separate feature from Browser Integration and does not need the extension.

## Browser integration
1. Tools > Settings > Browser Integration: tick Enable browser integration and select your browsers. Extension supports Chrome/Vivaldi/Brave, Firefox/Tor Browser, Edge, Chromium. On Linux, Flatpak and Snap browsers are generally unsupported (Ubuntu's Firefox Snap is the known exception). Managed Edge needs a custom native messaging configuration.
2. Install KeePassXC-Browser from the browser's store; unlock the database and (re)open the browser.
3. Click the extension icon, Connect, then name the connection (for example `firefox-laptop`) and Save and allow access. Reusing a connection name in a database overwrites the earlier browser connection and blocks its access.
4. The icon shows state: disconnected, not connected to this database, connected but locked, or ready (a number = credentials found for the site). Use Reload if it is not connected.
5. On first use a Confirm Access dialog lists credentials; tick them, optionally Remember, then Allow Selected. Click the KeePassXC icon in the username field to fill.
6. Per entry, the Browser Integration tab lets you add extra URLs (wildcards such as `https://*.example.com` need 2.7.10+) or hide the entry. Extra fields: add attributes named `KPH: ...` then use Choose Custom Login Fields.
7. Database > Database reports > Browser Statistics shows URLs, allowed/denied sites and custom settings; Database Settings > Browser Integration has "Forget all site-specific settings on entries" (cannot be undone once saved).

## Auto-Type
- Set the global shortcut at Tools > Settings > Auto-Type; adjust start and inter-key delays if it misbehaves.
- On the hotkey, KeePassXC searches unlocked databases for entries matching the focused window title; a selection dialog appears for no match, multiple matches, unavailable title, or when "Always ask before performing Auto-Type" is on.
- Default sequence: `{USERNAME}{TAB}{PASSWORD}{ENTER}`. Change it for all entries on the root group; per entry use the Auto-Type tab, add a window association and tick "Use specific sequence".
- Window title: `*` is a wildcard (`*` alone matches all), blank offers sequences for every window, and `//regex//` uses a regular expression.
- Placeholders include `{TITLE}`, `{URL}`, `{TOTP}`, `{S:Name}`; codes include `{DELAY X}` (pause), `{DELAY=X}` (key delay), `{CLEARFIELD}`; modifiers `+ ^ % #` = Shift, Ctrl, Alt, Win/Cmd.
- Entry-level Auto-Type (toolbar, context menu, Ctrl+Shift+V) types into the previously selected window; the guide warns it can hit the wrong window, such as chat or email.
- Wayland: uses XDG Desktop Portals (Remote Desktop and Global Shortcuts); support varies by desktop (KDE, GNOME; others may need a custom portal).

## Verify
- [ ] Extension shows ready state and fills a test login.
- [ ] Global Auto-Type picks the right entry by title in one desktop app.

## Checked
Method: 2026-11-08 read the Browser Integration and Auto-Type sections of the KeePassXC User Guide in full. Removed as unsupported: the specific browser option recommendations (best-matching only, expired credentials, never-ask) and "sandboxed browsers need extra steps in the guide" (guide says generally unsupported). Added the Browser Statistics report and forget-sites steps.
