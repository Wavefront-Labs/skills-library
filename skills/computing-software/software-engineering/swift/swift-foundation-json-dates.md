---
id: computing-software.software-engineering.swift.swift-foundation-json-dates
name: swift-foundation-json-dates
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-interop, foundation-json-dates]
level: practitioner
status: draft
description: "Handle JSON, dates, formatters and URLs with Foundation correctly."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Foundation essentials Codable JSON dates
- `JSONDecoder().decode(T.self, from: data)`; set `.dateDecodingStrategy = .iso8601`; use `Date.FormatStyle`/`ISO8601FormatStyle` in modern code; `DateFormatter` is expensive: cache and set `locale = Locale(identifier: "en_US_POSIX")` for fixed formats.
- Calendar-aware math with `Calendar.current.date(byAdding:)`, never add 86400 seconds blindly.
- `URL(string:)` returns nil for invalid strings; use `URLComponents` for queries.
Verify: test around DST changes and a non-Gregorian locale.
