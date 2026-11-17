---
id: computing-software.devops-ci-cd.backstage.plugin-analytics
name: plugin-analytics
category: computing-software
field: devops-ci-cd
product: backstage
tags: [analytics-api, capture-events, analytics-context, backstage]
level: advanced
status: docs-checked
description: "Instrument plugins and wire analytics tools using the event-based Backstage Analytics API."
sources:
  - https://backstage.io/docs/plugins/analytics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Analytics API collects usage events so you can measure the return on a Backstage investment, using any analytics tool.

Concepts:

- Events have an `action` (such as `click`) and a `subject` (what was clicked).
- Attributes are key/value dimensions on an individual event, for example `{ "to": "/a/page" }`.
- Context is the surrounding information, such as `pluginId`, `extension` and `routeRef`, added by default.

Plugin authors capture events with the `useAnalytics` hook:

```tsx
import { useAnalytics } from '@backstage/core-plugin-api';

const analytics = useAnalytics();
analytics.captureEvent('click', 'Download report', {
  attributes: { format: 'csv' },
});
```

App integrators write an analytics API implementation that forwards events to their tool, handling user identity as appropriate. The docs list supported analytics tools and cover:

- Key events, such as navigation and search.
- Providing extra attributes and context.
- Event naming considerations.
- Unit testing event capture.

On naming, the docs say to avoid an overly specific action (use `filter` rather than `filterEntityTable` and let context carry the component) and to reuse existing context keys such as `entityRef` so events aggregate across plugins. For user identity, base the user id on `userEntityRef` from `identityApi.getBackstageIdentity()`. The page is marked legacy for the old frontend system, but its concepts and events apply to both frontend systems.

## Checked

2026-11-03. Confirmed on the Plugin Analytics page: events have an action and subject, attributes (for example `{ "to": "/a/page" }`), default context `pluginId`, `extension` and `routeRef`, `useAnalytics` from `@backstage/core-plugin-api` with `captureEvent(action, subject, { attributes })`, the AnalyticsApi implementation, supported tools, key events, event naming considerations, identity handling with `userEntityRef`, and unit testing with `MockAnalyticsApi`. Removed: the lowercase subject and hashing or pseudonymising advice, which the page does not give.

Method: documentation only; no commands were run.
