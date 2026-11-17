---
id: computing-software.general-digital-literacy.web-browsers.videos-will-not-play
name: videos-will-not-play
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-troubleshooting, video-not-playing, javascript, extensions]
level: intro
status: docs-checked
description: "Fix web videos and games that will not load, show a blank or gray box, or freeze Chrome: JavaScript, extensions, cache, update, reset and connection steps."
sources:
  - https://support.google.com/chrome/answer/6138475
  - https://support.google.com/chrome/answer/4410268
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Videos will not play

Chrome's help covers: a video or game that will not load, is blank or shows a gray box, or makes Chrome freeze or crash while loading. Flash is not the cause to chase: Adobe ended Flash Player support in 2021 and Flash content no longer plays in any version of Chrome.

## Steps (Chrome, in order)
1. **JavaScript on:** More > Settings > Privacy and security > Site settings > JavaScript > Sites can use JavaScript. Reload the page. (Sites such as YouTube will not run without it.)
2. **Extensions, cache, cookies:** open a New Incognito Window and try the site. If it works there, go back to a normal window: More > Extensions > Manage extensions, turn all off, reload, then turn on one at a time; remove the one that breaks the video. If it still fails, More > Delete browsing data, choose a time range, tick "Cached images and files" and "Cookies and other site data", Delete data. Warning: this erases some website settings and signs you out of sites.
3. **Update Chrome:** More > Update Google Chrome (no button means you are current) > Relaunch.
4. **Reset settings:** Settings > Reset settings > Restore settings to their original defaults (on Windows Chrome's help also words the section "Reset and cleanup"). This clears cookies and turns off extensions.
5. **Reset the internet connection:** turn off the computer, unplug the modem (and router if separate) for about one minute, plug back in, wait for lights to settle, restart the computer.

## Protected content
Chrome plays protected (copyright-managed) content by default. On Android, Settings > Site settings > Protected Content can be set to Ask first or Blocked; check it was not changed.

## Verify
- [ ] The video plays with picture and sound after reloading.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Fix videos & games that won't play" and "Manage your protected content settings", read in October 2026. Confirmed: all five steps and paths, the Flash note, the protected content default and Android path. Removed as unconfirmed: Widevine component steps, Firefox DRM, hardware acceleration, codec and extension tips, Edge and Safari claims, and the autoplay note.
Method: documentation only; no commands were run.
