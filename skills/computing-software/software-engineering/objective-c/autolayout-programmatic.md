---
id: computing-software.software-engineering.objective-c.autolayout-programmatic
name: autolayout-programmatic
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-ui, autolayout-programmatic]
level: practitioner
status: draft
description: "Build constraints in code with layout anchors, activateConstraints, priorities and translatesAutoresizingMaskIntoConstraints."
sources:
  - https://developer.apple.com/documentation/uikit
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Programmatic Auto Layout
**Goal:** correct, conflict-free constraints.

```objc
UILabel *label = [UILabel new];
label.translatesAutoresizingMaskIntoConstraints = NO;
[self.view addSubview:label];
[NSLayoutConstraint activateConstraints:@[
    [label.leadingAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.leadingAnchor constant:16],
    [label.trailingAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.trailingAnchor constant:-16],
    [label.topAnchor constraintEqualToAnchor:self.view.safeAreaLayoutGuide.topAnchor constant:8],
]];
[label setContentHuggingPriority:UILayoutPriorityRequired forAxis:UILayoutConstraintAxisVertical];
```
- Add the view to its superview before constraining.
- Set `translatesAutoresizingMaskIntoConstraints = NO` on views you constrain yourself.
- Use anchors (`leadingAnchor`, `centerYAnchor`, `widthAnchor`) and `UIStackView` for linear layouts; prefer `leading`/`trailing` over left/right for RTL.
- Priorities below 1000 let constraints break gracefully; mark the optional ones.
- Constraint changes inside `[UIView animateWithDuration:animations:]` followed by `[self.view layoutIfNeeded]` animate.
- Debug: `po [self.view _autolayoutTrace]` (private), `constraintsAffectingLayoutForAxis:`, and the console log with `UIViewAlertForUnsatisfiableConstraints`.

## Gotchas
- Missing width/height ambiguity causes zero-size views.
- Constraints between views without a common ancestor crash.

## Self-check
Add a conflicting constraint and read the console log to find which one to remove.
