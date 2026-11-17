---
id: computing-software.software-engineering.mobile-development.android-activity-and-fragment-lifecycle
name: android-activity-and-fragment-lifecycle
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, activity-lifecycle, fragment-lifecycle, lifecycle-aware, repeatonlifecycle, viewlifecycleowner, kotlin]
level: practitioner
status: docs-checked
description: "Handle Android Activity and Fragment lifecycles: what belongs in each callback, the separate fragment view lifecycle, lifecycle-aware components and flow collection."
sources: ["https://developer.android.com/guide/components/activities/activity-lifecycle", "https://developer.android.com/guide/fragments/lifecycle", "https://developer.android.com/topic/libraries/architecture/lifecycle", "https://developer.android.com/topic/libraries/architecture/coroutines#lifecycle-aware"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Android Activity and Fragment lifecycle

**Goal:** do work in the right callbacks so the app does not leak, touch a destroyed view, or
waste battery collecting data while invisible.

## Activity callbacks
The six core callbacks are `onCreate`, `onStart`, `onResume`, `onPause`, `onStop` and `onDestroy`
(plus `onRestart` when a stopped activity returns).
- `onPause` is the first sign the user is leaving; the activity may still be visible in
  multi-window mode, where only one app has focus and the system pauses the others. Use it to
  pause or adjust work you expect to resume shortly, or release sensors and battery-draining
  resources. It is very brief: do not save data, make network calls or run database
  transactions there.
- `onStop` is called when the activity is no longer visible. Release or adjust resources not
  needed while invisible, and do relatively CPU-intensive shutdown work such as saving a draft
  to a database. Using `onStop` rather than `onPause` keeps UI work running in multi-window mode.
- `onDestroy` runs when the activity is finishing or when the system destroys it temporarily for
  a configuration change (rotation, multi-window); in the latter case a new instance is created
  immediately and gets `onCreate`.
- Persist user data when the activity is in the foreground where possible; otherwise in `onStop`.
- Camera or similar shared resources: initialising on `ON_RESUME` keeps them only while the
  activity is resumed; on `ON_START` keeps them while paused-but-visible, which can deny the
  resource to another app in multi-window mode. Put this logic in a lifecycle-aware component
  rather than directly in callbacks, so it can be reused across activities.
- By default a configuration change destroys the activity and wipes UI state held in the instance.
  Order of `onStop` and `onSaveInstanceState` differs by API: before API 28 state is saved
  first; from API 28 `onStop` is called first.

## Fragment: two lifecycles
A fragment's view has a separate `Lifecycle` managed independently, with its own owner
(`getViewLifecycleOwner()`), so use it for work that should run only while the view exists,
such as observing LiveData that is displayed on screen.
- `onAttach()` is always called before any lifecycle state change; `onDetach()` after.
- CREATED: `onCreate()` (restore state of the fragment itself; the view does not exist yet).
- View INITIALIZED: with a non-null view, `onViewCreated()` is called: set up the view, start
  observing LiveData that updates the view, set up adapters.
- View CREATED: `onViewStateRestored()` follows once view state is restored.
- STARTED: tie lifecycle-aware components to this state; the view is available and child
  transactions are safe. `onStart()`. RESUMED: `onResume()`; fragments that are not resumed
  should not set focus or handle input method visibility.
- Downward: `onPause()`, then `onStop()` (after which the fragment's state may be saved; ON_STOP
  is the last safe point for a child `FragmentTransaction`), then `onDestroyView()`, then
  `onDestroy()`.
- After `onDestroyView()` all references to the view should be removed so it can be garbage
  collected; `getViewLifecycleOwnerLiveData()` returns null at that point.
- Do not reuse a `Fragment` instance after it is removed from its `FragmentManager`; add
  fragments in XML with `FragmentContainerView`, not the `<fragment>` tag.

## Lifecycle-aware collection
- Compose: `collectAsStateWithLifecycle()` converts a Flow to State, starts collecting when
  the lifecycle is STARTED and stops when it is STOPPED; `minActiveState` overrides the
  threshold (for example RESUMED). The Jetpack lifecycle guide says not to start and stop
  collection by hand from lifecycle events.
- `viewModelScope` coroutines are cancelled when the ViewModel is cleared.
- `LaunchedEffect` is bound to the composition, not the Activity lifecycle, and can run when the
  composable is not visible (for example off-screen pager pages); for work that depends on the
  user actually viewing the screen, use lifecycle-aware APIs such as `LifecycleEventEffect`.

## Checked
Confirmed in the four cited pages: Activity callback roles, multi-window pause behaviour,
configuration-change destruction, `onStop`/`onSaveInstanceState` order on API 28, fragment view
lifecycle and callbacks, `collectAsStateWithLifecycle` and scopes. Removed as not on these
pages: `repeatOnLifecycle` and `launchWhenStarted` claims, the ViewBinding null-out rule, the
duplicate-observer claim, the `commit` after `onSaveInstanceState` exception text, the
no-arg-constructor rule, the "Don't keep activities" adb setting and LeakCanary advice.
Method: docs-only read of cited pages, 2026-11-08
