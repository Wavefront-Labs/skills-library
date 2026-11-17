---
id: computing-software.software-engineering.mobile-development.remote-config-and-feature-flags
name: remote-config-and-feature-flags
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, remote-config, feature-flags, firebase-remote-config, kill-switch, ab-testing, rollout]
level: practitioner
status: docs-checked
description: "Control mobile app behaviour remotely with Firebase Remote Config: in-app defaults, loading strategies, real-time updates, rollouts, limits and policies."
sources: ["https://firebase.google.com/docs/remote-config", "https://firebase.google.com/docs/remote-config/loading", "https://firebase.google.com/docs/remote-config/real-time"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote config and feature flags

**Goal:** change the behaviour of shipped apps without an app update: roll features out gradually,
switch broken ones off, and run experiments.

## How Remote Config works
- You set in-app default values (`setDefaults()`), then override them from the Firebase console or the
  Remote Config backend APIs by creating parameters with the same names. Conditional values can
  override the default for app instances that match a condition.
- The client library fetches and caches values, and you control when fetched values are activated.
  Getters read in-app defaults and fetched values through the same call.
- Conditions segment by app version, language, Google Analytics audience, imported segment, or custom
  signal conditions. A/B Testing adds random percentage targeting.
- Rollouts use parameter values as feature flags, released gradually, and compare Crashlytics and
  Analytics results against an equal-sized control group.
- Update in-app defaults whenever you ship; the console and REST API can download a defaults file
  (XML, plist or JSON).

## Loading strategies (pick by how visible the change is)
1. **Fetch and activate on load** (`fetchAndActivate` at startup): fine for changes with no dramatic UI
   effect. Avoid where the UI could visibly change while the user is using it.
2. **Activate behind a loading screen**: show a loading screen, call `fetchAndActivate`, then dismiss.
   Add your own timeout: Remote Config's one-minute timeout may be too long for startup. Strongly
   recommended when loading values for an A/B Testing experiment, which needs extra time to place the
   user in the experiment.
3. **Load for next startup**: at startup activate previously fetched values (near instant), then fetch
   asynchronously within the minimum fetch interval and do nothing in the completion handler; the new
   values activate at the next start.

## Real-time updates
- `addOnConfigUpdateListener` opens an HTTP connection to the backend; when a newer template is
  published the SDK fetches it and calls your listener. This fetch bypasses caching and
  `minimumFetchInterval`. The connection is kept while the app is in the foreground and stops in the
  background automatically.
- Recommended: call fetch once per app launch, then listen in real time and `activate()` where values
  will not cause dramatic visual changes. `onUpdate` is not called when a fetch yields no change;
  `updatedKeys` lists changed keys so a view can check relevant ones before activating.
- The first listener call opens the connection and later ones reuse it; the returned registration has
  `remove`. A project is limited to 20 million concurrent connections, beyond which clients fall back to
  standard fetch.
- Real-time updates need Firebase SDK for Apple platforms v10.7.0 or later.

## Anti-patterns (from the docs)
- Do not change UI while the user is viewing or using it, except for strong reasons such as removing
  options for a promotion that just ended.
- Do not send mass simultaneous fetch requests (throttling risk); use real-time updates for frequent
  updates.
- Do not depend on network connectivity: always set in-app defaults so the app behaves as expected.

## Policies and limits
- Do not store confidential data in keys or values: end users can read any default or fetched value.
- Do not use it for changes that require user authorization, or to circumvent platform requirements.
- 3000 parameters per template type (client or server); up to 300 lifetime template versions per type
  (deleted ones count); up to 24 running A/B experiments and rollouts combined.

## Verify
- [ ] The app works with defaults only on first launch and with no network.
- [ ] Values are activated only at points where the UI will not visibly jump.
- [ ] No secrets in parameter keys or values.

## Checked
Read in full the three cited Firebase pages. Removed as unconfirmed: the Kotlin and Swift snippets, the 12-hour default fetch interval, country and percentile condition claims, force-update and store-review advice, template rollback, and third-party flag providers.
Method: docs-checked 2026-11-09 against the Remote Config overview, loading strategies and real-time pages.
