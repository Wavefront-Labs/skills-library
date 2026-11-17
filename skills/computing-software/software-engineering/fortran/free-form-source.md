---
id: computing-software.software-engineering.fortran.free-form-source
name: free-form-source
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, free-form-source, fortran-source-form, gfortran]
level: intro
status: docs-checked
description: "Write free-form Fortran for gfortran: source form selection, the 132-column default, line truncation errors and ampersand continuation of strings."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/Fortran-Dialect-Options.html
  - https://gcc.gnu.org/onlinedocs/gfortran/Error-and-Warning-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Free-form source layout
**Goal:** write free-form source that gfortran accepts cleanly.
- Source form: `-ffree-form` and `-ffixed-form` select the layout. Free form was introduced in Fortran 90; fixed form is the traditional layout of older programs. With neither option the form comes from the file extension. In an fpm project the `[fortran] source-form` key defaults to `"free"`.
- Line length: `-ffree-line-length-n` sets the column after which characters are ignored in free-form lines; the default is 132. `n` may be `none` (the entire line is meaningful); `-ffree-line-length-0` means the same as `none`. For fixed form the corresponding option is `-ffixed-line-length-n`, with default 72.
- Truncation: `-Wline-truncation` warns when a source line is truncated; it is implied by `-Wall`, and for free-form source the default is `-Werror=line-truncation`, so truncation is an error.
- Continuation: a continued character constant should have an ampersand at the start of the continuation line too. `-Wampersand` warns about a missing one (it is active with `-pedantic` and `-std=f95` through `-std=f2023`); without it gfortran assumes the continuation resumes at the first non-comment, non-whitespace character after the ampersand that started it.
```fortran
program demo
  implicit none
  integer :: total
  total = 1 + 2 + &
          3
  print *, 'total=', total; print *, 'done'  ! two statements
  print *, 'a long string that is &
           &continued'
end program demo
```
## Gotchas
- Text beyond column 132 is an error under the default settings, not a silent cut; raise the limit with `-ffree-line-length-none` only if you accept non-portable source.## Self-check
Compile `gfortran -std=f2018 -Wall demo.f90`; expect no warnings and the output you intended.

## Checked
Checked against the gfortran manual pages "Options controlling Fortran dialect" and "Options to request or suppress errors and warnings".
Removed: the 255 continuation lines and Fortran 95's 39-line limit (these are standard-language limits, not on the cited pages), the per-extension list of free-form suffixes, and the J3 source (not read). The comment and statement-separator syntax appears only in the example and is not a checked claim.
Method: docs-only read of cited pages, 2026-11-08
