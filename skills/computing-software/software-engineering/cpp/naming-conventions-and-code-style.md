---
id: computing-software.software-engineering.cpp.naming-conventions-and-code-style
name: naming-conventions-and-code-style
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-style, cpp-sy-naming, naming-conventions, clang-tidy-readability-identifier-naming, google-style, core-guidelines-naming]
level: practitioner
status: docs-checked
description: "Choose and enforce C++ naming conventions: Core Guidelines NL rules, the Google naming scheme per entity, reserved identifiers, readability-identifier-naming."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl-naming-and-layout-suggestions", "https://clang.llvm.org/extra/clang-tidy/checks/readability/identifier-naming.html", "https://google.github.io/styleguide/cppguide.html#Naming"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Naming conventions

Pick one house style, leave imported libraries in their original style, and enforce it mechanically. Core Guidelines NL.8: consistency in naming and naming style increases readability; choose a house style but leave imported libraries with their original style.

## Core Guidelines rules
- NL.5: avoid encoding type information in names (no `print_int`/`print_string`; use overloads). Hungarian notation is "generally unnecessary and actively harmful" in C++. General-purpose prefixes (`p` for indirection, `cnt` for count), member markers like `m_` and capitalised types do not encode type and are fine.
- NL.7: make the length of a name roughly proportional to the length of its scope (`i`, `p`, `x` are fine in small scopes; a global named `g` or `open` is bad).
- NL.8: avoid identifiers containing double underscores `__` or starting with an underscore followed by a capital letter (for example `_Throws`); they are reserved for the implementation. Be consistent with acronyms versus full words.
- NL.9: use `ALL_CAPS` for macro names only (so not for `const int SIZE` or for enumerators; see also Enum.5).
- NL.10: prefer `underscore_style` names (the C++ standard library style); this is a default for when you have a choice, and consistency beats personal taste.
- ES.9: avoid `ALL_CAPS` names.

## Google style scheme
| Entity | Style | Example |
|---|---|---|
| Types (classes, structs, aliases, enums, type template parameters) and concepts | `PascalCase`, no underscores | `UrlTable`, `UrlTableError` |
| Variables, parameters, struct data members | `snake_case` | `table_name`, `num_entries` |
| Class data members | `snake_case` with trailing underscore | `table_name_` |
| Constants with static storage (const or constexpr, fixed for program duration) | `k` plus mixed case | `kDaysInAWeek` |
| Enumerators | like constants, not macros | `kOutOfMemory`, not `OUT_OF_MEMORY` |
| Functions | `PascalCase` | `AddTableEntry()` |
| Accessors and mutators | may be `snake_case` | `count()`, `set_count()` |
| Namespaces | `snake_case` | `my_project` |
| Macros (avoid them) | all caps with underscores and a project prefix | `MYPROJECT_ROUND` |
| Files | lowercase with `_` (or `-`); `.cc` and `.h` | `http_server_logs.h` |

- Non-type template parameters follow variable or constant rules; the `k` convention is optional for automatic variables.
- Name files specifically (`http_server_logs.h`, not `logs.h`) and avoid names that exist in `/usr/include`.
- Nested namespaces should avoid names of well-known top-level namespaces such as `std` and `absl`.
- Names analogous to an existing C or C++ entity may follow that entity's convention.

## Enforcement with clang-tidy readability-identifier-naming
- It enforces one casing per kind of identifier: `lower_case`, `UPPER_CASE`, `camelBack`, `CamelCase`, `camel_Snake_Back`, `Camel_Snake_Case`, `aNy_CasE`, `Leading_upper_snake_case`, plus a fixed prefix and suffix regardless of casing.
- It only enforces kinds that are configured, so an empty configuration disables it. `DefaultCase` enforces a style on every kind, which specific options can override (for example `DefaultCase` `lower_case`, `MacroDefinitionCase` `UPPER_CASE`, `TemplateParameterCase` `CamelCase`).
- Per-kind options include `ClassCase`, `FunctionCase`, `ConstantCase`, `ConstantPrefix`, `PrivateMemberSuffix`, `EnumConstantCase`, `ConceptCase` and many more, with `...IgnoredRegexp` variants to skip matches. Rules fall back to a more generic rule if a specific one is not configured.
- Hungarian notation can be enabled via `HungarianPrefix` settings (default `Off`).
- Virtual method names are reported where they occur in the base class, not where overridden.

## Verify
- CI runs the naming check on changed files.
- Search project code for reserved identifiers (leading underscore plus capital, double underscore).

## Checked
Read Core Guidelines NL.5 to NL.10 and ES.9, the Google C++ Style Guide naming section, and the clang-tidy readability-identifier-naming page (casing types and option descriptions). Removed as unconfirmed: the `.clang-tidy` YAML key format, `--fix` rename scope and `clang-rename`, `HeaderFilterRegex`, `using namespace` and `inline namespace` rules, the Core Guidelines enumerator preference beyond NL.9.
Method: docs-checked 2026-11-09 against Core Guidelines NL.5-NL.10 and ES.9, the Google style guide naming section and the clang-tidy readability-identifier-naming page.
