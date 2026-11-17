---
id: computing-software.devops-ci-cd.bazel.bazel-labels-and-target-patterns
name: bazel-labels-and-target-patterns
category: computing-software
field: devops-ci-cd
product: bazel
tags: [bazel-label, canonical-repo-name, apparent-repo-name, package-name, target-name, relative-labels]
level: intro
status: docs-checked
description: "Read and write Bazel labels correctly: repo, package and target parts, shorthand forms, and common mistakes."
sources: ["https://bazel.build/concepts/labels"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel labels

Full form: `@@myrepo//my/app/main:app_binary` = canonical repo (`@@`), package path, target name. Write `@myrepo//...` for an apparent repo name, which can map to different repos depending on where the label appears. Inside the same repo you can drop the repo: `//my/app/main:app_binary`. Inside the same package you can write `:app_binary` or `app_binary`. If the target name equals the last package component, `//my/app/lib` means `//my/app/lib:lib`.

Common mistake: `//my/app` is `//my/app:app`, not the whole package. In `package_group` specs and `.bzl` files it does name the package, which is why it is encouraged there.

Files: `//my/app/main:testdata/input.txt` names a file under the package directory. A subdirectory with its own BUILD file is a different package, so `testdata/testdepot.zip` is wrong and `//my/app/testdata:testdepot.zip` is right. Never use `..` or leading/trailing/double slashes in a target name.

Main repo from outside: `@@//a/b/c` always means the main repository, while `//a/b/c` inside an external repo means that repo's own package.

Allowed target-name characters are letters, digits and a set of punctuation. Avoid `/` in rule names. Package names may not start or end with `/` or contain `//`, `/./` or `/../`; for Java choose directory names that are valid identifiers. Prefer leaving the root package `//:foo` empty.

## Checked

2026-11-04. Read against the Bazel docs page(s): Labels (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the closing Verify line.
Method: documentation only; no commands were run.
