---
id: computing-software.software-engineering.objective-c.nsnotificationcenter
name: nsnotificationcenter
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-runloop, nsnotificationcenter]
level: practitioner
status: draft
description: "Post and observe notifications with selectors or blocks, control delivery queue and remove observers correctly."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSNotificationCenter
**Goal:** loosely coupled one-to-many events.

```objc
extern NSNotificationName const ABCDidSyncNotification;
[[NSNotificationCenter defaultCenter] postNotificationName:ABCDidSyncNotification object:self userInfo:@{@"count": @3}];

[[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(didSync:) name:ABCDidSyncNotification object:nil];
id token = [[NSNotificationCenter defaultCenter] addObserverForName:ABCDidSyncNotification object:nil
    queue:[NSOperationQueue mainQueue] usingBlock:^(NSNotification *n) { ... }];
[[NSNotificationCenter defaultCenter] removeObserver:token];
```
- Delivery is synchronous on the posting thread (for selector observers and nil-queue block observers); pass a queue to hop threads.
- Selector-based observers are auto-removed on dealloc in modern OS versions, but block-based tokens must be removed explicitly; the block retains what it captures (weak self).
- `name:nil` / `object:nil` are wildcards; filter by sender with `object:`.
- Use constants for names; keep `userInfo` keys documented.
- `NSNotificationQueue` coalesces and delays posting until the run loop idles.

## Gotchas
- Posting from background and updating UI in the handler crashes or misbehaves.
- Notifications are not for request-response; use delegates or blocks.

## Self-check
Post from a background queue and assert the handler runs on the main queue when one is provided.
