---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-offline-and-degraded-states
name: designing-offline-and-degraded-states
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [offline-state, offline-first, degraded-state, connectivity, service-worker, sync-status, ui-states]
level: practitioner
status: draft
description: "Design for offline and degraded connectivity: detect and show state, queue actions, sync with conflict handling, cache for read access, and avoid false error messages."
sources:
  - "web.dev - Offline UX design guidelines and Offline Cookbook (web.dev/articles/offline-ux-design-guidelines)"
  - "Google Developers - Progressive Web Apps, service workers (developer.chrome.com/docs/workbox)"
  - "Apple Human Interface Guidelines - Offline / network use (developer.apple.com/design/human-interface-guidelines)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offline and degraded states

**Goal:** the product stays useful and honest when the network is absent, slow or flaky.

## Detect and show
- Use `navigator.onLine` plus request failures (not alone: it only reports a network interface) and reachability checks; handle "lie-fi" (connected but no throughput) with timeouts.
- Show a quiet persistent indicator ("Offline. Changes will sync when you're back online") and disable only what truly needs the network, with a reason on the disabled control.

## Design levels
1. **Read-only cache:** serve last-known content with a timestamp ("Updated 12:04"); service worker strategies: stale-while-revalidate for content, cache-first for static assets, network-first for critical data.
2. **Queue writes:** record actions locally (IndexedDB or app database) with visible pending state per item (clock icon), then replay in order; use idempotency keys to avoid duplicates; Background Sync where available.
3. **Sync feedback:** states: pending, syncing, synced, failed with retry; summary count in status area.
4. **Conflicts:** last-write-wins is simplest but loses data; for collaborative data use merge (CRDT or field-level merge) or show a conflict dialog with both versions.
5. **Failure of non-critical parts:** degrade features individually (images fail, maps unavailable) with placeholders, not a blank page.

## Copy
Be specific and calm: "You're offline" not "Error"; tell what works and what does not; confirm when reconnected, then sync silently or with a brief toast.

## Test
Use DevTools throttling and Offline mode, airplane mode on devices, and tunnel/elevator scenarios; test resume after hours offline and session expiry on reconnect.

## Verify
- [ ] Offline state visible; unavailable actions explained.
- [ ] Writes queue safely; sync states and conflicts handled.
- [ ] Verified under throttled and fully offline conditions.
