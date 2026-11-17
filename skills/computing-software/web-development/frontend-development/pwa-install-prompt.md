---
id: computing-software.web-development.frontend-development.pwa-install-prompt
name: pwa-install-prompt
category: computing-software
field: web-development
product: frontend-development
tags: [progressive-web-app, pwa, beforeinstallprompt, pwa-install, add-to-home-screen, appinstalled, display-mode-standalone, related-applications]
level: practitioner
status: docs-checked
description: "Offering a custom install button with beforeinstallprompt, detecting standalone mode, measuring installs and guiding iOS users to Add to Home Screen."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/BeforeInstallPromptEvent
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/prefer_related_applications
  - https://developer.mozilla.org/en-US/docs/Web/API/Navigator/getInstalledRelatedApps
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PWA install prompt

**Goal:** show an install button at a good moment, only where install is possible, and know when the app runs installed.

## 1. Capture and defer the prompt (Chromium)
```js
let deferred;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();           // suppress the mini-infobar
  deferred = e;
  installBtn.hidden = false;
});
installBtn.addEventListener('click', async () => {
  installBtn.hidden = true;
  deferred.prompt();             // must be called from a user gesture
  const { outcome } = await deferred.userChoice;   // 'accepted' | 'dismissed'
  track('pwa_install_prompt', { outcome });
  deferred = null;               // a prompt event can be used only once
});
window.addEventListener('appinstalled', () => track('pwa_installed'));
```
`beforeinstallprompt` is non-standard and experimental (MDN browser-compat data: Chrome 44 onwards, not Firefox or Safari), and it is part of the install-prompt technique for installable PWAs. `prompt()` must be called from a user action such as a button click and may be called only once per event instance (MDN). Feature-detect by the event firing, not by user agent.

## 2. iOS / Safari
No programmatic prompt. On iOS 16.4+ PWAs are installed from the Share menu; show a dismissible hint such as "Tap Share, then Add to Home Screen". Safari 17 on macOS Sonoma and later has File > Add to Dock (MDN).

## 3. Detect installed mode
```js
const standalone = matchMedia('(display-mode: standalone)').matches;
```
Use it to hide install UI, adjust layout (no browser back button - provide in-app navigation), and tag analytics. CSS: `@media (display-mode: standalone) { … }`.

## 4. Timing
Don't prompt on first page view. Prompt after a sign of engagement (second visit, completed task) and in context ("Install for offline access"). Remember dismissal (store a timestamp) and don't re-ask immediately.

## 5. Native app relationship
If you also have a store app, `related_applications` plus `prefer_related_applications: true` is a hint to prefer the native app; MDN's installability list says `prefer_related_applications` must be false or absent for Chromium to treat the PWA as installable. `navigator.getInstalledRelatedApps()` can detect an installed related app.

## Verify
- [ ] Chrome desktop/Android: custom button appears only when installable; prompt works once per event.
- [ ] Installed app launches standalone and hides the install UI.
- [ ] Analytics shows prompt outcomes and `appinstalled`.

## Checked
Checked 2026-10-26 against MDN BeforeInstallPromptEvent and its prompt() method (user action required, once per event; non-standard, experimental), MDN browser-compat data (Chrome 44, no Firefox or Safari), MDN Making PWAs installable (iOS 16.4 Share menu, Safari 17 Add to Dock, beforeinstallprompt technique, prefer_related_applications must be false or absent) and the getInstalledRelatedApps page. Removed the unconfirmed navigator.standalone check and the 'for weeks' figure. The scripts were not run.

Method: documentation only; no commands were run.
