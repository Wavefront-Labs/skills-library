---
id: computing-software.software-engineering.d.d-package-d-and-project-layout
name: d-package-d-and-project-layout
category: computing-software
field: software-engineering
product: d
tags: [d-package-d-and-project-layout, modules-packages, package-d, project-layout, source-folder, library-layout, package-visibility, src-structure, d]
level: practitioner
status: draft
description: "Layout a D project: source/app.d, source/pkg/package.d, library versus app layout, public import in package.d, visibility package(pkg), and test directories."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# package.d, project layout and dub source folders

Goal: create a conventional dub project layout.

```
myproj/
  dub.sdl
  source/
    app.d                # app entry (main)
    myproj/
      package.d          # public import myproj.core; ...
      core.d
      util/package.d
  tests/ ...             # optional extra configuration
```
- `dub init` produces the skeleton; for a library omit `app.d` or set `targetType "library"`.
- Name modules `myproj.core`, put `module myproj.core;` as first line; importers write `import myproj;` and see the re-exports.
- Use `package(myproj)` visibility for internals; `private` for module internals; keep the public API in `package.d`.
- Do not name a module `std`, `core`, `object`, `etc` (reserved roots).
- Separate `internal` modules (`myproj.internal.*`) and exclude from docs.
- Add `sourcePaths`/`importPaths` when deviating from `source/`.

Gotchas:
- A file called `package.d` cannot also have a module name other than the dir path.
- Name clash between a module and a package folder of same name produces a conflict (`foo.d` and `foo/package.d`).

Verify: `dub build` from a clean checkout.
