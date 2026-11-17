---
id: computing-software.general-digital-literacy.web-browsers.pop-up-blocker-and-redirects
name: pop-up-blocker-and-redirects
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-troubleshooting, pop-up-blocker, redirects, allow-pop-ups, notification-spam]
level: intro
status: docs-checked
description: "Allow pop-ups for a site that needs them (banks, portals), block abusive pop-ups and redirects, and stop notification spam in Chrome, Edge and Safari."
sources:
  - https://support.google.com/chrome/answer/95472
  - https://support.microsoft.com/en-us/microsoft-edge/block-pop-ups-in-microsoft-edge-1d8ba4f8-f385-9a0b-e944-aa47339b6bb5
  - https://support.apple.com/guide/safari/block-pop-ups-sfri40696/mac
  - https://support.google.com/chrome/answer/2765944
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pop-up blocker and redirects

**Goal:** genuine pop-up windows (payment, login, print) work; ads and fake warnings do not.

## Allow pop-ups for one site
- **Chrome:** by default Chrome blocks pop-ups and marks the address bar "Pop-up blocked". On the page, click **Pop-up blocked** > the pop-up link > **Always allow pop-ups and redirects from [site]** > Done. Default setting: More > Settings > Privacy and security > Site Settings > **Pop-ups and redirects**.
- **Edge:** Settings > Privacy, search, and services > **Site permissions** > All permissions > **Pop-ups and redirects**; under *Allowed to send pop-ups and use redirects* choose **Add site** and enter the address starting with https://. The blocker is on by default.
- **Safari (Mac):** Safari > Settings > **Websites** > **Pop-up Windows** (scroll to the bottom of the list if you do not see it); in the site's menu choose **Allow**, **Block and Notify** or **Block**. The "When visiting other websites" menu sets the default.

## Block a site
- Chrome: Site Settings > Pop-ups and redirects > find the site under Allowed > More > **Block**, or **Add** it under *Not allowed to send pop-ups or use redirects*. `[*.]example.com` covers a whole domain.

## Abusive pop-ups and redirects
- Keep the blocker on.
- Pop-ups, new tabs that will not go away, a changing homepage or search engine, or alerts about a virus can mean unwanted software: Chrome's help recommends removing unwanted programs and then resetting browser settings. Apple says the same may apply on a Mac if you keep seeing Safari pop-ups after blocking them.
- Never call a number shown in a fake warning page; close the tab or quit the browser.
- Edge's blocker cannot stop adverts built to look like pop-ups, and it does not stop a window you open by selecting a button or link.

## Notification spam (looks like pop-ups)
- Chrome: on the site, click **View site information** > **Notifications** > **Block**, or manage them under Site settings. Chrome may also remove notification permission from sites you have not visited for a while, and from sites Safe Browsing finds tricking users into allowing it.
- Edge: see Microsoft's "Manage website notifications in Microsoft Edge" page.

## Verify
- [ ] The site's pay/print/login window opens; the site appears in the allowed list.
- [ ] No unknown sites in notification permissions.

## Checked
2026-10-27. Chrome Help (Block or allow pop-ups; Remove unwanted ads, pop-ups and malware), Microsoft's Edge pop-up page and Apple's Safari User Guide (pop-ups) were read. Confirmed the menu paths and option names above. Firefox and the Safari notification menu are not covered because they could not be confirmed. Method: documentation only; no commands were run.
