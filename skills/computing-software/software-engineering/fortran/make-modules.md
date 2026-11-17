---
id: computing-software.software-engineering.fortran.make-modules
name: make-modules
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, make-modules, fortran-build-systems]
level: practitioner
status: draft
description: "Write Makefiles that respect module dependencies, so objects are built after the .mod files they use."
sources:
  - https://www.gnu.org/software/make/manual/
  - https://cmake.org/cmake/help/latest/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Makefiles, module files and compile order
**Goal:** build correctly with make.
```make
FC = gfortran
FFLAGS = -O2 -Wall -J build -I build
OBJ = build/geometry.o build/main.o
app: $(OBJ)
	$(FC) $(FFLAGS) -o $@ $^
build/%.o: src/%.f90 | build
	$(FC) $(FFLAGS) -c $< -o $@
build/main.o: build/geometry.o      # main uses module geometry
build:
	mkdir -p build
```
- Order by dependency: any file that `use`s a module depends on the object that creates its `.mod`.
- Tools: `makedepf90` or `fortdepend` can generate dependency rules; or let fpm/CMake do it.
- Parallel builds (`make -j`) race without correct dependency lines.
## Gotchas
- Editing a module body changes the `.mod` only if the interface changes (gfortran keeps timestamps in some versions); a naive rule rebuilds all users.
- Recipe lines need tabs.
## Self-check
Touch a module and confirm only dependents rebuild; `make -j4` from clean works repeatedly.
