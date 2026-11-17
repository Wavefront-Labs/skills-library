---
id: computing-software.devops-ci-cd.dagger.module-layout-and-runtime
name: module-layout-and-runtime
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, modules, dagger-init, dagger-develop, runtime-container, packaging, file-layout]
level: practitioner
status: docs-checked
description: "Initialize a Dagger module, split its code across files per SDK, and know the runtime container and language packaging each SDK uses."
sources: [https://docs.dagger.io/0.21/extending/modules]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Initialize a module, organize files, understand the runtime

Goal: create a module and structure its source correctly (Dagger 0.21 docs).

## Initialize

`dagger init` creates `dagger.json` and sample source in the current directory; the module name defaults to the directory name unless `--name` is given. `dagger develop --sdk=...` sets up or updates everything needed for local development; code goes in the current directory unless `--source` is set. Generated files cannot be edited (changes are not persisted).

`dagger develop` regenerates code for current dependencies and Dagger API version. Read the changelog before running it, or use `--compat=skip` to avoid bumping the API version.

## Splitting code into files

- **Go**: add files in the same package (`utils.go`) to share private symbols; a subpackage (`utils/`) can only use exported symbols and cannot see `main.go` types. Only the top-level package is the public API. In a subpackage import `dagger/<module>/internal/dagger` and pass `*dagger.Client` since `dag` is unavailable.
- **Python**: make a package; `__init__.py` must import the main object (`from .main import MyModule as MyModule`) and `main.py` imports other object types. Layout is library-style (src layout, package name matching the project name). To use a different import package, add to `pyproject.toml`: `[project.entry-points."dagger.mod"]` with `main_object = "<import package>:<main object>"`. Default lookup is `my_module:MyModule`, falling back to `main:MyModule`. For a single `main.py` module, configure your build backend (hatchling: `packages = ["main.py"]`; setuptools: `py-modules = ["main"]`).
- **TypeScript**: the main class stays in `src/index.ts`; sub-classes can live in other files and be imported.
- **PHP**: only the main class (`src/MyModule.php`) is callable initially; return other classes from its functions.
- **Java**: the main class must be named after the module in PascalCase; annotate with `@Object` and `@Function`. Describe the module in `package-info.java` with `@Module`.

## Runtime container

Go: hardcoded to Go 1.21. Python: `python:3.14-slim` by default; override with `requires-python` or a `.python-version` file (`echo "3.12" > .python-version`), or `[tool.dagger] base-image = "acme/python:3.12"` (at your own risk). TypeScript: Node.js 22.11.0 (Bun 1.1.38 and Deno 2.2.4 experimental). PHP: `php:8.3-cli-alpine`. Java: build in `maven:3.9.9-eclipse-temurin-17`, run in `eclipse-temurin:23-jre-noble`.

## Packaging

- Go: a real Go module (`go mod tidy` after adding imports); when a module is created Dagger attempts to add it to a root `go.work` if one exists; otherwise add it later with `go work use ./path/to/mymodule`. Go vendor directories are not supported.
- Python: `pyproject.toml` + `uv.lock`; remove `uv.lock` to fall back to the pip interface. A pip-tools style `requirements.lock` is installed with `uv pip install -r requirements.lock -e ./sdk -e .`; Poetry users can export with `poetry export --without main -o requirements.lock`.
- TypeScript: installed with `yarn install --production`; devDependencies are not installed. Any Node package manager works if `package.json` exists.
- PHP: `composer install`; needs `composer.json`.
- Java: `mvn clean package` then `java -jar module.jar`; keep `pom.xml`, especially the `maven-compiler-plugin` and `maven-shade-plugin` settings.

## Using a remote module

```shell
dagger -m github.com/kpenfound/dagger-modules/golang@v0.2.0 call \
  build --source=https://github.com/dagger/dagger --args=./cmd/dagger export --path=./build
```

SSH form: `-m git@github.com:kpenfound/dagger-modules/golang@v0.2.0` (needs SSH authentication configured on the Dagger host).

## Checked

2026-11-07

Read extending/modules/modules.mdx in full (live slug /extending/modules; the cited /extending/modules/modules URL is a file path that 404s, fixed in sources) and the partial _dagger_module_init.mdx it imports (init, develop, compat warning, per-SDK default layouts, the generated-files note). All content on the page is inline code blocks, so no snippet files were involved. Confirmed the file-splitting rules per SDK, the Python entry-point configuration and default lookup, the single-file hatchling and setuptools settings, the runtime container images and versions for each SDK, the packaging commands (go mod tidy, uv.lock fallback to pip, requirements.lock install line, poetry export, yarn install --production, composer install, mvn clean package) and the remote module commands. Softened the go.work statement to match the page's 'attempts to add' wording.

Method: documentation only; no commands were run.
