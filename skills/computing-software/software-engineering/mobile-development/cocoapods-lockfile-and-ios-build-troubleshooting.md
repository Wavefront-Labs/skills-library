---
id: computing-software.software-engineering.mobile-development.cocoapods-lockfile-and-ios-build-troubleshooting
name: cocoapods-lockfile-and-ios-build-troubleshooting
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, ios, cocoapods, podfile, podfile-lock, pod-install, pod-update, pod-outdated, xcworkspace, pods-xcconfig, duplicate-symbols, inherited-flags, ios-build, dependency-locking, pod-troubleshooting]
level: practitioner
status: docs-checked
description: "pod install versus pod update, why Podfile.lock must be committed, pod outdated, and build fixes: use the xcworkspace, $(inherited) settings, Pods.xcconfig, duplicate symbols."
sources: ["https://guides.cocoapods.org/using/pod-install-vs-update.html", "https://guides.cocoapods.org/using/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CocoaPods: the lockfile and iOS build troubleshooting

**Goal:** every machine resolves the exact same pod versions, and the pod-related iOS build errors
that follow dependency changes get fixed at the cause instead of by re-running `pod install` until
something happens.

## `pod install` is not just for first setup
The guides are explicit that this is a misconception: `pod install` is the command "every time you
edit your Podfile to add, update or remove a pod".

| Action | Command |
|---|---|
| First setup, or add/remove/change pods in the Podfile | `pod install` |
| Update one pod to the newest version its constraint allows | `pod update PODNAME` |
| Update every pod | `pod update` |
| See which pods have newer versions available | `pod outdated` |

- **`pod install`** resolves only the pods **not** already in `Podfile.lock`; locked pods install at
  their locked versions without checking for newer ones. New pods resolve against the Podfile's
  constraints and are written into the lock.
- **`pod update PODNAME`** ignores the lock for that pod and takes the newest version satisfying the
  Podfile constraint. Bare **`pod update`** does that to *every* pod - the blast radius people reach
  for by accident when they meant `pod install`.

The rule that keeps teams consistent: adding a pod means `pod install`, never `pod update` - the
latter risks updating unrelated pods in the same pass.

## Podfile.lock must be committed
The lock "keeps track of the installed version of each pod and *locks* those versions", so a fresh
clone + `pod install` reproduces the exact dependency tree the last committer had. The guides put it
in bold: "**you should always commit & push your `Podfile.lock` file**" - even when the policy is not
to commit the `Pods/` directory.

Pin-in-Podfile is *not* a substitute. `pod 'A', '1.0.0'` pins `A`, but if its podspec declares
`dependency 'A2', '~> 3.0'`, two machines can resolve `A2` 3.4 and 3.5 respectively. Only the lock
pins the whole transitive tree - "that is not enough to guarantee that user1 and user2 will always
get the exact same version of all their pods".

The `.xcworkspace` and `Pods.xcodeproj` are side effects of `pod install` creating them on first
run - generated output, not the record.

## Build troubleshooting
- **Use `<Project>.xcworkspace`, not the Xcode project.** The guide states this as the first rule when using CocoaPods.
- **`$(inherited)` in build settings**: never completely override options set from `Pods.xcconfig`;
  prepend `$(inherited)` to your value lists so the pod-provided flags survive.
- **Headers not found**: check the pod headers are symlinked under `Pods/Headers`, that you are not
  overriding `HEADER_SEARCH_PATHS`, and that *every* configuration selects `Pods.xcconfig`
  (project file -> Info -> Configurations). Last resort: prefix imports (`#import "Pods/SSZipArchive.h"`).
- **`Library not found for -lPods`**: add the `Pods` static library in Product -> Edit Scheme ->
  Build at the **top** of the list, then clean and build; also confirm the spec source was pulled
  (the directory under `Pods/<spec>` should not be empty) and set Derived Data's build location to
  "Relative to Workspace".
- **Duplicate symbols with static libraries** - typically a closed-source library bundling a
  dependency you also depend on. The real fix belongs to the vendor (prefixing its dependencies);
  the brute-force workaround is removing that dependency from the static library.
- **Unrecognised compiler options** (`cc1obj: unrecognised command line option`): use the Apple LLVM
  (clang) compiler and remove exported `CC`/`CPP`/`CXX` variables from the shell profile.
- **Archive empty in Organizer**: "Skip Install" must be `NO` for Release on the application target.

## Failure modes
- **"Works on my machine" dependency drift** - `Podfile.lock` not committed, or someone ran bare
  `pod update` locally and shipped a different tree.
- **A pod never updates no matter what** - it is locked; `pod install` honours the lock by design.
  That is correct behaviour - decide to update via `pod outdated` + `pod update PODNAME`.
- **Headers or library not found** - opened the `.xcodeproj` instead of the workspace.
- **Flags mysteriously missing after a dependency change** - a build setting overriding
  `Pods.xcconfig` without `$(inherited)`.
- **Unrelated pods jump versions** - bare `pod update` run where `pod install` was meant.

## Verify
- [ ] `Podfile.lock` is tracked in git; `Pods/` is not (unless deliberately vendored).
- [ ] A fresh clone + `pod install` builds without touching any version.
- [ ] `pod outdated` reviewed before any update; updates are named (`pod update PODNAME`), not bare.
- [ ] CI opens the `.xcworkspace`, and no build setting overrides a `Pods.xcconfig` value without
      `$(inherited)`.

## Checked
Date: 2026-11-08. Confirmed against the CocoaPods guides pages pod-install-vs-update and Troubleshooting: install/update/outdated semantics, committing Podfile.lock, the transitive-dependency example, workspace use, $(inherited), header search, Library not found for -lPods steps, duplicate symbols, compiler option errors and Skip Install. Removed the React Native/Flipper section and the claim that Pods/ is normally uncommitted, which neither page states.
Method: documentation only; no commands were run.
