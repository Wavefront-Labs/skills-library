---
id: computing-software.software-engineering.ada.elementary-functions-random
name: elementary-functions-random
category: computing-software
field: software-engineering
product: ada
tags: [ada, elementary-functions-random, ada-numerics]
level: practitioner
status: docs-checked
description: "Ada.Numerics.Elementary_Functions, Float_Random, Discrete_Random and Complex_Types."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elementary functions and random numbers
```ada
with Ada.Numerics.Elementary_Functions; use Ada.Numerics.Elementary_Functions;
Y := Sqrt (2.0) * Sin (0.5);
with Ada.Numerics.Float_Random;
G : Ada.Numerics.Float_Random.Generator;  Reset (G);  R := Random (G);
package R is new Ada.Numerics.Discrete_Random (Result_Subtype => Die);
```
- `Ada.Numerics.Generic_Elementary_Functions` is instantiated for other float types: `new Ada.Numerics.Generic_Elementary_Functions (Float)`.
- `Float_Random` yields values between 0.0 and 1.0; `Discrete_Random` is generic and is instantiated for a discrete (sub)type that sets the range.
- `Complex_Types` and `Complex_Elementary_Functions` cover Float; similar packages exist for Long_Float and Long_Long_Float, plus `Generic_Complex_Types`.
## Gotchas
- Declare a `Generator` and call `Reset (G)` before drawing numbers, as the library's examples do.
## Self-check
Print 5 die rolls using a Discrete_Random generator.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Standard Library: Numerics: Elementary_Functions, Generic_Elementary_Functions, Float_Random, Discrete_Random, Reset, Complex_Types and generic complex packages. Removed `Argument_Error` and the determinism claim (not on the pages read) and the Ada.Numerics.Pi use.
Method: documentation only; no commands were run.
