---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-udf-basics
name: fluent-udf-basics
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-hpc, fluent-udf, user-defined-function, define-profile, compiled-udf, c-programming]
level: advanced
status: draft
description: "Write and load a basic Fluent user-defined function (profile example), choose compiled vs interpreted, and avoid common crash causes."
sources:
  - "Ansys Fluent UDF manual (DEFINE macros, loops and compiled/interpreted UDFs)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent UDF basics

**Goal:** custom boundary profiles or source terms.

## Example: velocity profile on a boundary
```c
#include "udf.h"
DEFINE_PROFILE(inlet_u, thread, position)
{
  real x[ND_ND];
  face_t f;
  begin_f_loop(f, thread)
  {
    F_CENTROID(x, f, thread);
    F_PROFILE(f, thread, position) = 10.0 * (1.0 - x[1]*x[1]);
  }
  end_f_loop(f, thread)
}
```

## Steps
1. Save as a `.c` file in the working directory.
2. **User Defined > Functions > Compiled** (or Interpreted): add source file, Build, Load. Compiled UDFs need a supported C compiler configured on the machine; interpreted ones are slower and have restrictions.
3. In the boundary condition panel pick the UDF from the drop-down for the variable.
4. In parallel runs use host and node macros (`#if RP_NODE`) and global reductions (`PRF_GRSUM1`) for any quantity gathered across processes.

## Gotchas
- Wrong thread or position arguments, or writing outside the loop macros, crash Fluent.
- Dimensional units are SI inside UDFs.
- Compiled libraries are tied to the Fluent version and the architecture.

## Verify
- [ ] Plot of the boundary profile on the face matches the intended formula.
- [ ] Runs in serial and parallel with identical results.
