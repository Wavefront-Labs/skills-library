---
id: computing-software.software-engineering.objective-c.target-action
name: target-action
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-cocoa-patterns, target-action]
level: intro
status: draft
description: "Wire controls with addTarget:action:forControlEvents: (UIKit) or target/action (AppKit) and understand responder chain dispatch."
sources:
  - https://developer.apple.com/documentation/uikit
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Target-action
**Goal:** connect UI controls to handlers.

```objc
[button addTarget:self action:@selector(didTapButton:) forControlEvents:UIControlEventTouchUpInside];
- (void)didTapButton:(UIButton *)sender { ... }
// AppKit
button.target = self; button.action = @selector(save:);
```
- Action signatures accepted: `-(void)action`, `-(void)action:(id)sender`, and on UIKit `-(void)action:(id)sender forEvent:(UIEvent *)event`.
- A `nil` target (`[UIApplication sendAction:to:from:forEvent:]` with nil) walks the responder chain from the first responder up to the application and delegate.
- Targets are not retained by the control (weak/unretained reference): keep the target alive and remove targets in `dealloc` if necessary.
- Interface Builder connections create `IBAction`/`IBOutlet` markers (`IBAction` is `void`).
- Actions named in storyboards are resolved at runtime by name; renaming without updating the storyboard causes a crash on tap.

## Gotchas
- A missing selector raises unrecognized selector at tap time, not compile time.
- Strong `IBOutlet` to subviews is fine; to top-level views use strong, to children weak by convention (modern guidance: strong or weak both accepted when the view hierarchy holds them).

## Self-check
Compile with `-Wundeclared-selector` and add a UI test tapping the button.
