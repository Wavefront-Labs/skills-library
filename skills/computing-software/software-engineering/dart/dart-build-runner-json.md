---
id: computing-software.software-engineering.dart.dart-build-runner-json
name: dart-build-runner-json
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-codegen, build-runner-json]
level: practitioner
status: docs-checked
description: "Generate JSON serialization code with build_runner and json_serializable and keep generated parts consistent."
sources: ["https://pub.dev/packages/build_runner", "https://pub.dev/packages/json_serializable"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# build_runner and json_serializable
- Add `build_runner` and `json_serializable` as dev dependencies, then `dart run build_runner build` (one-off) or `dart run build_runner watch`. A build_runner code generator is called a builder.
- Generated output lands in a part file: `part 'example.g.dart';` plus `@JsonSerializable()` on the class; wire the generated `fromJson` and `toJson` from `example.g.dart` into the class by hand.
- Configure generation three ways: properties on `JsonKey` on a field, properties on `JsonSerializable` on the type, or `build.yaml` for all classes (explicit annotation values win over `build.yaml`; `JsonKey` wins over `JsonSerializable`). `fieldRename`, for example `FieldRename.kebab`, sets default naming; `JsonKey(fromJson:, toJson:)` take top-level or static functions for custom conversion; `JsonKey.defaultValue` is reflected in the generated schema.
- `.dart_tool/build` artifacts are private to build_runner and should not be edited, checked in or published. Whether to commit `.g.dart` files is a team choice: keep it consistent, and have CI run the build and fail on a diff.
- Round-trip `fromJson(toJson(x))` in tests.

Verify: change a field, forget to rebuild, and confirm the tests or analyzer catch the stale `.g.dart`.

## Checked

Checked 2026-11-08 against the pub.dev pages of build_runner and json_serializable (README text read). Removed (not confirmed in pages read): `--delete-conflicting-outputs`, the `explicitToJson` and `includeIfNull` options, freezed, and the statement about Dart macros being abandoned.

Method: documentation only; no commands were run.
