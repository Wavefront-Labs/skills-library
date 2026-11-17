---
id: computing-software.software-engineering.objective-c.viewcontroller-lifecycle
name: viewcontroller-lifecycle
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-ui, viewcontroller-lifecycle]
level: practitioner
status: draft
description: "Place setup and teardown in the correct UIViewController lifecycle methods, call super, and keep UI work on the main thread."
sources:
  - https://developer.apple.com/documentation/uikit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# View controller lifecycle
**Goal:** put code in the right callback.

```objc
- (void)viewDidLoad { [super viewDidLoad]; [self buildViews]; }                // once, view exists, bounds not final
- (void)viewWillAppear:(BOOL)animated { [super viewWillAppear:animated]; [self refresh]; }   // each time
- (void)viewDidAppear:(BOOL)animated { [super viewDidAppear:animated]; [self startAnimations]; }
- (void)viewWillDisappear:(BOOL)animated { [super viewWillDisappear:animated]; [self.timer invalidate]; }
- (void)viewDidLayoutSubviews { [super viewDidLayoutSubviews]; /* frames final */ }
- (void)dealloc { /* only non-object cleanup */ }
```
- Order: `init` -> `loadView` -> `viewDidLoad` -> `viewWillAppear:` -> `viewWillLayoutSubviews` -> `viewDidLayoutSubviews` -> `viewDidAppear:`.
- Always call super in `viewDid/Will*` overrides.
- Add observers/timers in `viewWillAppear:` and remove in `viewWillDisappear:` to avoid cycles and background work.
- Since iOS 6, views are no longer unloaded on memory warnings; `viewDidUnload` is gone.
- UIKit is main-thread only (except where documented): `dispatch_async(dispatch_get_main_queue(), ...)` for updates from background tasks; Main Thread Checker detects violations.
- Use `didMoveToParentViewController:` / `willMoveToParentViewController:` for containment.

## Gotchas
- Using `self.view` in `init` forces `loadView` early.
- `viewDidLoad` frame values are not final; layout-dependent code goes in `viewDidLayoutSubviews`.

## Self-check
Log each callback and compare against the order above when pushing and popping.
