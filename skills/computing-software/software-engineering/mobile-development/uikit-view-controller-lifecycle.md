---
id: computing-software.software-engineering.mobile-development.uikit-view-controller-lifecycle
name: uikit-view-controller-lifecycle
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, uikit, viewcontroller-lifecycle, viewdidload, viewwillappear, layout, auto-layout, containment]
level: intro
status: draft
description: "Know the UIKit view controller lifecycle: what to do in viewDidLoad, viewWillAppear, viewDidLayoutSubviews and viewDidDisappear, plus containment and leak traps."
sources: ["https://developer.apple.com/documentation/uikit/uiviewcontroller", "https://developer.apple.com/documentation/uikit/view_controllers/displaying_and_managing_views_with_a_view_controller"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UIKit view controller lifecycle

Order for a presented controller: `init` -> `loadView` -> `viewDidLoad` -> `viewWillAppear` -> `viewWillLayoutSubviews` -> `viewDidLayoutSubviews` -> `viewDidAppear` ... `viewWillDisappear` -> `viewDidDisappear`.

| Callback | Do here | Do not |
|---|---|---|
| `viewDidLoad` | one-time setup: add subviews, constraints, bind data sources | rely on final frame/bounds; start per-appearance work |
| `viewWillAppear(_:)` | refresh data that may have changed, start observers, update nav bar | heavy synchronous work (delays the transition) |
| `viewDidLayoutSubviews` | frame-dependent tweaks (gradient layer frames, corner radius from bounds) | add/remove constraints each pass (loops) |
| `viewDidAppear(_:)` | start animations, analytics screen view, begin camera/location | assume it is called once |
| `viewWillDisappear` / `viewDidDisappear` | stop timers, observers, camera, save state | assume the view is deallocated |

```swift
override func viewDidLoad() {
    super.viewDidLoad()               // always call super in lifecycle overrides
    tableView.dataSource = self
}
override func viewWillAppear(_ animated: Bool) {
    super.viewWillAppear(animated)
    Task { await viewModel.refresh() }
}
override func viewDidDisappear(_ animated: Bool) {
    super.viewDidDisappear(animated)
    timer?.invalidate()
}
```

## Gotchas
- `viewWillAppear` fires again after dismissing a modal or popping back; `viewDidLoad` does not (unless the view was purged, which is rare since iOS 6).
- Interactive pop-gesture can start `viewWillDisappear` and then cancel, calling `viewWillAppear` again; use `transitionCoordinator` if it matters.
- Child controllers: `addChild(vc)`, add its view, then `vc.didMove(toParent: self)`; reverse with `willMove(toParent: nil)` and `removeFromParent()`.
- Closures capturing `self` in timers, NotificationCenter blocks or Combine sinks cause retain cycles; use `[weak self]`.

Verify: add `print` in each override, push, pop (including a cancelled swipe) and present modally, and compare the observed order to the table; check deinit prints when popped.
