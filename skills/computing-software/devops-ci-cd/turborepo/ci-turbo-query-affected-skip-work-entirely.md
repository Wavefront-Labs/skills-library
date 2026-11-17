---
id: computing-software.devops-ci-cd.turborepo.ci-turbo-query-affected-skip-work-entirely
name: ci-turbo-query-affected-skip-work-entirely
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, turbo-query-affected, exit-code, jq, skip-ci, affected-reason, merge-base, shallow-checkout]
level: advanced
status: docs-checked
description: "Use turbo query affected with jq or --exit-code to skip container setup and installs when a package or task is unaffected."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/constructing-ci.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hitting the cache is useful, but you can sometimes skip work entirely, such as lengthy container preparation and dependency installation that would end in a cache hit anyway.

1. **Checkout with enough history.** A shallow checkout makes all packages count as changed. For example clone with `--filter=blob:none --depth=0`. By default `turbo query affected` compares against the merge-base with your default branch.
2. **Check if a package is affected.** The command outputs JSON you can parse with `jq`:

```bash
affected=$(turbo query affected --packages web)
count=$(echo "$affected" | jq '.data.affectedPackages.length')
if [ "$count" -gt 0 ]; then echo "web is affected"; else echo "skipping"; exit 0; fi
```

For a task, `turbo query affected --tasks test --packages docs` and read `.data.affectedTasks.length`. This respects the `inputs` configuration, so only relevant file changes count.

For a binary signal use `--exit-code`: it exits `1` when results are found, `0` when nothing is affected, and `2` on errors:

```bash
turbo query affected --packages web --exit-code
```

3. **Handle the result.** The `length` field says how many packages or tasks are affected; when `0` you can safely skip the rest of the pipeline. The output also has the reason per package (`FileChanged`, `DependencyChanged`), useful for debugging unexpected builds.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/constructing-ci); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
