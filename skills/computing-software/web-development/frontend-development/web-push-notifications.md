---
id: computing-software.web-development.frontend-development.web-push-notifications
name: web-push-notifications
category: computing-software
field: web-development
product: frontend-development
tags: [progressive-web-app, pwa, web-push, push-notifications, vapid, pushmanager, push-subscription, notificationclick, web-push-ios]
level: practitioner
status: docs-checked
description: "Implementing Web Push end to end: VAPID keys, permission timing, PushManager subscriptions, sending from the server, showing and handling notifications."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Push_API
  - https://developer.mozilla.org/en-US/docs/Web/API/PushManager/subscribe
  - https://datatracker.ietf.org/doc/html/rfc8030
  - https://datatracker.ietf.org/doc/html/rfc8292
  - https://github.com/web-push-libs/web-push
  - https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Push notifications

**Goal:** opt-in push messages that arrive with the app closed and open the right page when tapped.

## 1. Pieces
- **VAPID key pair** (server identity, RFC 8292): generate once, e.g. with the web-push library's `generate-vapid-keys` command. Public key goes to the client; private key stays on the server (secret store).
- **Subscription**: `{endpoint, keys: {p256dh, auth}}` from the browser's push service; store per user/device.
- **Service worker** `push` and `notificationclick` handlers.

## 2. Subscribe (after a user gesture)
```js
btn.addEventListener('click', async () => {
  if (await Notification.requestPermission() !== 'granted') return;
  const reg = await navigator.serviceWorker.ready;
  const sub = await reg.pushManager.subscribe({
    userVisibleOnly: true,                       // required by Chrome
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
  });
  await fetch('/api/push/subscriptions', { method: 'POST', body: JSON.stringify(sub), headers: { 'Content-Type': 'application/json' } });
});
```
Ask only after explaining the value ("Notify me when my order ships"), in response to a user gesture; MDN's subscribe() page says to call it from a user gesture and notes browsers penalise or block prompts that are not.

## 3. Send (Node example)
```js
import webpush from 'web-push';
webpush.setVapidDetails('mailto:ops@example.com', process.env.VAPID_PUBLIC, process.env.VAPID_PRIVATE);
try { await webpush.sendNotification(sub, JSON.stringify({ title: 'Shipped', url: '/orders/42' }), { TTL: 3600, urgency: 'normal' }); }
catch (e) { if (e.statusCode === 410) await deleteSubscription(sub.endpoint); else throw e; }   // 410 Gone: subscription expired
```
Delete subscriptions when the push service reports them gone (410) or you keep sending to dead endpoints; the web-push library exposes the push service's `statusCode` on its error. RFC 8030: push services must not reject messages of 4096 bytes or less with 413, so keep payloads at or below 4096 bytes and fetch details on click if needed. `TTL` is in seconds.

## 4. Service worker
```js
self.addEventListener('push', (e) => {
  const d = e.data?.json() ?? {};
  e.waitUntil(self.registration.showNotification(d.title, { body: d.body, icon: '/icons/192.png', data: { url: d.url }, tag: d.tag }));
});
self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  e.waitUntil(clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
    const open = list.find(c => c.url.endsWith(e.notification.data.url));
    return open ? open.focus() : clients.openWindow(e.notification.data.url);
  }));
});
```
Every push should show a notification: Chrome and Edge reject `subscribe()` unless `userVisibleOnly` is `true`. `tag` is an identifying string for the notification.

## 5. iOS
WebKit's announcement: Web Push arrived with iOS and iPadOS 16.4 for Home Screen web apps, and permission can only be requested in response to direct user interaction such as tapping a subscribe button.

## Verify
- [ ] DevTools > Application > Push "Push" button shows a notification with the SW handler.
- [ ] Notification arrives with browser closed (desktop) / app closed (Android, installed iOS).
- [ ] Tapping opens or focuses the right URL; expired subscriptions get deleted.

## Checked
Checked 2026-10-26 against MDN PushManager.subscribe (userVisibleOnly required by Chrome and Edge, call on a user gesture) and Push API best practices, RFC 8030 (push services must not return 413 for bodies of 4096 bytes or less; TTL in seconds), the web-push README (setVapidDetails, generate-vapid-keys, sendNotification options TTL and urgency, error statusCode) and the WebKit blog post on Web Push for iOS and iPadOS 16.4 (Home Screen web apps, user interaction). Removed unconfirmed items: Chrome quiet-UI auto-block, 404 handling, subscription revocation for silent pushes, and tag replacement behaviour. Code was not run.

Method: documentation only; no commands were run.
