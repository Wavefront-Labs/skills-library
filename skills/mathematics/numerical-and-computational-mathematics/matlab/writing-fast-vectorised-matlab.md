---
id: mathematics.numerical-and-computational-mathematics.matlab.writing-fast-vectorised-matlab
name: writing-fast-vectorised-matlab
category: mathematics
field: numerical-and-computational-mathematics
product: matlab
tags: [matlab, octave, vectorisation, vectorization, preallocation, implicit-expansion, broadcasting, backslash, mldivide, sparse, profiler, timeit, tic-toc, logical-indexing, column-major, cellfun, arrayfun, element-wise-operators, numerical-computing, performance]
level: practitioner
status: draft
description: "Make MATLAB numerical code fast and correct: preallocate, vectorise with implicit expansion and logical indexing, use backslash and sparse properly, and profile before optimising."
sources: ["MathWorks documentation: Techniques to Improve Performance; Vectorization; mldivide; Profile Your Code", "Moler, Numerical Computing with MATLAB (SIAM 2004)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing fast, vectorised MATLAB

**Goal:** translate a mathematical formula into MATLAB that runs at library speed, gives
the right answer, and stays readable.

## 1. Measure first
- `timeit(@() myfun(x))` for reliable timings (it warms up and repeats); `tic/toc` for
  rough wall-clock.
- `profile on; myscript; profile viewer` — optimise the lines that actually dominate.
- Since R2015b the execution engine JIT-compiles loops, so a clean `for` loop over
  scalars is no longer automatically slow. Vectorise where it makes the code clearer or
  where the profiler points, not reflexively.

## 2. Preallocate
Growing an array inside a loop (`x(end+1) = ...`) reallocates and copies; cost becomes
quadratic. Preallocate with `zeros(n,1)`, `nan(n,m)`, `cell(n,1)`, or
`strings(n,1)`. The Code Analyzer flags this ("variable appears to change size on every
loop iteration") — read those orange underlines.

## 3. Vectorise with the right operators
- Element-wise vs matrix: `.*  ./  .^` are element-wise; `*  /  ^` are linear algebra.
  Mixing them up is the #1 silent bug — `x^2` on a vector errors, but `A^2` on a square
  matrix silently computes A·A.
- **Implicit expansion** (R2016b+): `A - mean(A)` subtracts the column-mean row from
  every row; no `repmat` or `bsxfun` needed. Watch for accidental expansion:
  a column minus a row gives an n×m matrix, not an error.
- **Logical indexing:** `x(x < 0) = 0;`, `mean(y(mask))`, `nnz(cond)`; avoid `find` when
  you only need the mask.
- Reductions take a dimension: `sum(A, 2)`, `max(A, [], 1)`, `vecnorm(A, 2, 1)`.
  Specify it — the default picks the first non-singleton dimension, which changes
  meaning when A happens to have one row.
- `cumsum`, `diff`, `accumarray` (group-by sums), `histcounts`, `discretize` replace many
  hand loops.
- `arrayfun`/`cellfun` are conveniences, not speedups; they are often slower than a loop.

## 4. Linear algebra the MATLAB way
- Solve `A*x = b` with `x = A\b` (mldivide). It inspects A and chooses Cholesky, LU, QR
  (for rectangular — least squares), or a triangular/banded solver. Never `inv(A)*b`.
- For repeated solves with one matrix, factor once: `dA = decomposition(A);
  x = dA\b;` (R2017b+) or keep `[L,U,P] = lu(A)`.
- Large and mostly zero? Build with `sparse(i, j, v, m, n)` from triplets in one call —
  inserting into a sparse matrix element by element is very slow. Iterative solvers:
  `pcg`, `gmres`, `bicgstab`, with `ichol`/`ilu` preconditioners.
- Heed the warning "Matrix is close to singular or badly scaled. RCOND = …": RCOND is an
  estimate of 1/κ₁(A); 1e-16 means the answer is noise.

## 5. Memory layout
MATLAB is **column-major**: loop with the row index innermost, and prefer operating on
columns (`A(:, k)`) over rows. Contiguous column access is noticeably faster on large
arrays.

## 6. Numerical hygiene
- Use `eps(x)` (spacing at x) for tolerances, not literal 1e-16. `eps` alone is 2^-52.
- `isequal`/`==` on floats is fragile; compare with `abs(a-b) <= tol`.
- `integral`, `fzero`, `fminsearch`, `ode45/ode15s` all take options (`AbsTol`,
  `RelTol`, `optimset`/`optimoptions`) — set them; defaults are modest.
- Integer types saturate (`uint8(250) + 10 == 255`) and mixed integer/double arithmetic
  returns the integer type.

## Gotchas
- `length(A)` is the largest dimension, not the number of rows — use `size(A,1)` or `numel`.
- `'` is the conjugate transpose; use `.'` for plain transpose of complex data.
- `i` and `j` as loop variables shadow the imaginary unit; write `1i` for imaginary.
- Octave runs most of this but lacks some newer functions (`decomposition`, some
  string functions); check before relying on portability. Uncertain: exact release in
  which each function appeared — confirm with `doc` on your installed version.

## Verify
- [ ] Profiler run; optimisation targeted at the measured hot spots.
- [ ] No arrays grow inside loops; Code Analyzer clean.
- [ ] Every `*`, `/`, `^` checked as matrix vs element-wise intent.
- [ ] Vectorised version matches the loop version to within tolerance on test data.
- [ ] No `inv(A)*b`; RCOND warnings investigated.
