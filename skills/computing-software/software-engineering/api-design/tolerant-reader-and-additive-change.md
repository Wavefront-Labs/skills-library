---
id: computing-software.software-engineering.api-design.tolerant-reader-and-additive-change
name: tolerant-reader-and-additive-change
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, tolerant-reader, additive-change, robustness-principle, unknown-fields, unknown-enum-values, forward-compatibility, consumer-design]
level: practitioner
status: docs-checked
description: "Make API clients and servers evolve safely: tolerant readers that take only what they need, and additive-only producer changes per Google AIP-180, with defaults preserved."
sources: ["https://martinfowler.com/bliki/TolerantReader.html", "https://google.aip.dev/180"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tolerant reader and additive change

**Goal:** most API evolution should need no new major version: producers only ADD, consumers
tolerate what they don't understand.

## Consumer side: be a tolerant reader (Fowler)
- Take only the elements you need and ignore the rest; make minimal assumptions about payload structure
  (his XML example: `//order` rather than a full path).
- Schema-driven binding (e.g. classes generated from an XSD) often breaks when the provider merely adds a
  field; adding a field should not break anyone.
- Keep one piece of code that reads the payload, behind a Data Transfer Object, so the rest of the system is
  insulated from changes.
- Send the provider your reader and its tests so they can run them in their build (the step towards
  consumer-driven contracts).
- Expect new enum values in responses: AIP-180 warns that user code may not handle them gracefully.

## Producer side: additive change (AIP-180)
Allowed within a major version, with care:
- New interfaces, methods, messages, fields, enums and enum values may generally be added.
- Code unaware of the new component must be treated as before.
- Never add a new required field to an existing request message or resource.
- A new client-populated field needs a default that matches pre-existing behaviour (adding paging with a
  smaller default page size makes old clients wrongly assume they got all results).
- A field the server used to populate must keep being populated, even if redundant.
- Enum values may be added freely to enums used only in requests; enums used in responses that will grow should
  document that, and additions still need caution.

Breaking within a major version:
- Removing a component; renaming is "remove and add", so add the new one and keep the old.
- Changing a field's type, even to a wire-compatible one.
- Changing a resource's name or the set of valid names.
- Changing default values, the format or construction of an existing field, or how defaults are serialized.
- Increasing the upper bound for string field length.
- Semantic changes likely to break reasonable user code (a judgment call).
Compatibility has three kinds: source, wire and semantic. Guidance assumes protobuf and JSON and a broad consumer
base; a narrower API should work out its own requirements.

## Postel's law
Fowler frames this as Postel's Law: be conservative in what you do, be liberal in what you accept. Be tolerant of
extra data, but validate the data you actually use.

## Checked
Date: 2026-11-01. Confirmed against Martin Fowler's Tolerant Reader page and AIP-180 (adding, removing, renaming,
type, name, default, serialization and string-length rules; three compatibility types). Removed: deserialiser
settings for specific libraries, exhaustive-switch advice, compatibility-tool names, capability-field and
parallel-field techniques, which neither page states.
Method: documentation only; no commands were run.
