---
id: computing-software.data-engineering.metabase.dashboard-filters
name: dashboard-filters
category: computing-software
field: data-engineering
product: metabase
tags: [dashboard-filters, filter-widgets, default-value, time-grouping-filter, card-level]
level: practitioner
status: docs-checked
description: "Build Metabase dashboard filters: filter types, dashboard, header and card levels, connecting widgets to cards, default and required values, and the gotchas."
sources:
  - https://www.metabase.com/docs/latest/dashboards/filters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Filter types: date picker (Month and Year, Quarter and Year, Single Date, Date Range, Relative Date, All Options); location (City, State, ZIP/Postal Code, Country, with Is, Is not, Contains, Starts with, Ends with); ID; Number; Text or category; Boolean; and a Time grouping parameter that changes granularity rather than filtering.

Levels: dashboard-level (all tabs), header-level (same tab) or card-level (one card). Prefer dashboard-level by default. Connect a widget by choosing the card's field from its dropdown. Metabase may auto-connect a filter to other cards using the same field, including on other tabs.

Defaults: set a default in the filter sidebar's "Default value". "Always require a value" needs a default. The search box is the default input for columns with fewer than 100 unique values; an input box for more.

Gotchas:
- A filter not connected to any card on the current tab is hidden.
- Changing a widget's type disconnects it from all cards.
- Basic SQL variables accept only single-value filter types; use field filters for date ranges.
- Time grouping works only if the query's last stage is a datetime summary; adding a filter stage breaks it.
- Metadata settings override the widget's input type.
- Text cards can be wired only if they contain a variable.
- Widgets cannot be dragged between levels; use "Move filter".
- Selections are per viewer, not shared.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Every claim matched the page; no content changes.
