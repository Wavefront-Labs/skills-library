---
id: computing-software.web-development.frontend-development.notifications-api-and-permission-ux
name: notifications-api-and-permission-ux
category: computing-software
field: web-development
product: frontend-development
tags: [device-apis, notifications-api, permission-prompts, push-notifications, javascript]
level: practitioner
status: docs-checked
description: "Showing system notifications with the Notifications API: when and how to ask permission, double-permission UX, service worker showNotification, and handling clicks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API
  - https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/showNotification
  - https://web.dev/articles/permissions-best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Notifications API and permission UX

## 1. Permission states
`Notification.permission`: `"default"` (not asked), `"granted"`, `"denied"`. `"default"` means the user has not been asked, and the app must act as if permission were `denied`. Treat the browser prompt as a scarce resource: do not spend it before the user has shown interest.

## 2. Ask well
- Only in response to a user gesture such as a button click. MDN notes Firefox (from version 72) and Safari already disallow requests that are not triggered by a user gesture and that browsers are moving that way; Chrome and Firefox also require a secure context and no longer allow the request from cross-origin iframes.
- Double permission: show your own in-page explanation ("Get notified when your order ships?") with Yes/Not now; call the browser prompt only after Yes.
```js
async function enable() {
  if (!("Notification" in window)) return;
  const p = await Notification.requestPermission();   // must be inside a click handler
  if (p === "granted") await subscribePush();
}
```
- "Not now" should snooze your prompt (store a timestamp), not re-ask every visit.

## 3. Showing
The `Notification()` constructor is fine on desktop, but on most mobile browsers it throws a `TypeError`; MDN says to register a service worker and use `ServiceWorkerRegistration.showNotification()` there instead:
```js
const reg = await navigator.serviceWorker.ready;
reg.showNotification("Order shipped", { body: "Arrives Thursday", icon: "/icon-192.png", tag: "order-123", data: { url: "/orders/123" } });
```
`tag` identifies a notification so a new one with the same tag replaces it (no stacking); `renotify: true` alerts the user again for a replacement (MDN marks `renotify` as limited-availability, so check compatibility).

## 4. Clicks (in the service worker)
```js
self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(clients.matchAll({ type: "window", includeUncontrolled: true }).then(list => {
    const c = list.find(w => w.url.includes(e.notification.data.url));
    return c ? c.focus() : clients.openWindow(e.notification.data.url);
  }));
});
```

## 5. iOS
WebKit announced Web Push for Home Screen web apps in iOS and iPadOS 16.4; check Apple's current documentation before relying on notifications for sites that are not installed.

## Verify
DevTools > Application > Service workers "Push" to test; reset permission via the site info (lock icon) menu to retest the default flow.

## Checked

Checked 2026-10-26 against MDN Using the Notifications API, Notification.requestPermission(), Notification.renotify and ServiceWorkerRegistration.showNotification() (mdn/content main) and the WebKit blog post 'Web Push for Web Apps on iOS and iPadOS' (iOS 16.4 beta). Confirmed: permission values `default`/`granted`/`denied` and the meaning of `default`, user-gesture and secure-context rules, the mobile `TypeError` from the constructor, and showNotification from a service worker. Removed the unconfirmed Chrome quiet-UI and 'denial is permanent' claims and softened the iOS statement.

Method: documentation only; no commands were run.
