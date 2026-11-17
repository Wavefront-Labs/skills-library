---
id: computing-software.web-development.frontend-development.cross-tab-sync-broadcastchannel
name: cross-tab-sync-broadcastchannel
category: computing-software
field: web-development
product: frontend-development
tags: [client-side-storage, broadcastchannel, cross-tab-sync, storage-event, web-locks, leader-election, multi-tab]
level: practitioner
status: docs-checked
description: "Keeping multiple tabs consistent: storage events, BroadcastChannel messaging, logout-everywhere, and Web Locks for single-leader tasks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/storage_event
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-tab sync with BroadcastChannel

**Goal:** a change in one tab (logout, theme, cart) shows up in all tabs of the same origin, and background work runs once, not per tab.

## 1. BroadcastChannel
```js
const bc = new BroadcastChannel('app');
bc.postMessage({ type: 'logout' });
bc.onmessage = ({ data }) => { if (data.type === 'logout') location.assign('/login'); };
```
- Delivers to every other `BroadcastChannel` object of the same origin and name (windows, tabs, frames, iframes), except the object that sent the message.
- Messages are serialised with the structured clone algorithm (objects fine, functions not); a `SharedArrayBuffer` cannot be posted across agent clusters and raises `messageerror` on the receiving side.
- Close it (`bc.close()`) when a component unmounts.

## 2. storage event (fallback / when state already lives in localStorage)
```js
window.addEventListener('storage', (e) => {
  if (e.key === 'prefs:v2') applyPrefs(JSON.parse(e.newValue));
});
```
Fires in other same-origin browsing contexts (not the one that made the change) when `localStorage` changes. For `sessionStorage` it fires only for iframes in the same tab, so it does not sync tabs.

## 3. Logout everywhere
On logout: server invalidates the session, then the tab broadcasts `logout`; other tabs redirect. Also handle 401 responses globally since tabs that were asleep miss messages.

## 4. One tab does the work: Web Locks
```js
navigator.locks.request('sync-leader', async () => {
  // only one tab at a time gets here; the lock is released when the callback's promise settles
  await runSyncLoopForever();
});
```
Use it for polling, websocket connection sharing, or token refresh so N tabs don't hit the server N times. For token refresh, also share the result via BroadcastChannel.

## 5. Gotchas
- Reconcile state on `visibilitychange` to visible in case a message was missed while the tab was in the background.
- Same-origin only.

## Verify
- [ ] Log out in tab A: tab B redirects within a second.
- [ ] With five tabs open, the server sees one poll stream (Web Locks).
- [ ] Closing the leader tab hands the lock to another tab (test it; the docs only state release when the callback finishes).

## Checked

Checked 2026-10-26 against the MDN BroadcastChannel, BroadcastChannel.postMessage(), Window storage event, Web Locks API and LockManager.request() pages (mdn/content main): sender exclusion, same-origin scope, structured clone, storage-event scope for localStorage vs sessionStorage, and lock release when the callback finishes. Removed unconfirmed claims about the key being null on clear(), lock hand-off when a tab closes and cross-profile behaviour.

Method: documentation only; no commands were run.
