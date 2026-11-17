---
id: computing-software.cloud-infrastructure-engineering.docker.cookiecutter-and-copier-container-project-generators
name: cookiecutter-and-copier-container-project-generators
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, cookiecutter, copier, cruft, project-generator, project-templates, golden-path, dockerfile-templates, jinja-raw]
level: practitioner
status: docs-checked
description: "Build org-standard container project generators with cookiecutter hooks, or copier and cruft templates that can update existing projects."
sources: ["https://cookiecutter.readthedocs.io/en/stable/advanced/hooks.html", "https://copier.readthedocs.io/en/stable/", "https://copier.readthedocs.io/en/stable/updating/", "https://cruft.github.io/cruft/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cookiecutter and copier generators for container projects

`docker init` writes a fixed set of files once. An org template adds your base images,
non-root user, healthcheck, labels, Compose dev stack and CI pipeline, and (with copier or
cruft) lets existing projects pull template updates later.

## Cookiecutter hooks
Put `pre_gen_project` and `post_gen_project` scripts (`.py` or `.sh`) in the template's `hooks/`
directory. Both run in the root directory of the generated project, so relative paths find
generated files, and both support Jinja rendering.
- `pre_gen_project`: validate template variables (for example reject a slug that is not a
  valid name) before anything is written.
- `post_gen_project`: remove files that do not apply to the chosen options (for example
  Dockerfile variants for unselected languages).

## Jinja vs your own `{{ }}`
GitHub Actions `${{ github.sha }}`, Go templates in `docker inspect -f '{{.Id}}'` and Helm
templates collide with Jinja. Wrap such blocks in Jinja's `{% raw %}...{% endraw %}`, or check
the cookiecutter and copier docs for the option that copies chosen files without rendering.

## Copier: templates that update
A template is a Git repository with a `copier.yml` whose top-level keys are questions
(for example `project_name: {type: str, help: ...}`); answers are recorded in
`.copier-answers.yml` via a `{{_copier_conf.answers_file}}.jinja` file in the template.
```bash
copier copy gh:org/tpl-service ./orders-api   # gh: expands to https://github.com/
copier update                                  # inside the generated project
```
Updating works best when the destination has a valid `.copier-answers.yml`, the template is
versioned in Git with tags, and the destination is a clean Git repo. `copier update` reads the
tags, compares them using PEP 440 and checks out the latest one; add `--vcs-ref=HEAD` for the
latest commit. Conflicts are handled with `--conflict inline` (default, merge-style markers) or
`--conflict rej` (`.rej` files); add a pre-commit hook that blocks committing either.

## Cruft: updates for cookiecutter templates
- `cruft create <url>` creates a project from a cookiecutter template.
- `cruft update` (in the project root) pulls template changes.
- `cruft check` exits with code 1 when the project is out of date; run it in CI to stop drift.
- `cruft diff --exit-code` exits non-zero if any diff is found.

## Verify
Generate a project from the template for each variant you offer, then build and run it
yourself; the cited docs do not cover container testing. Confirm `copier update` on an older
project produces a reviewable diff.

## Checked

Checked 2026-11-09 against the cookiecutter hooks page, the copier home and updating pages and the cruft docs. Removed because the pages read did not confirm them: the `cookiecutter.json` example including `_copy_without_render`, the `--no-input` command, copier's `_subdirectory`, `_skip_if_exists` and `_exclude` keys, and the hadolint, Renovate and `docker compose config` test recipe. The `docker init` source was not read.

Method: docs-checked 2026-11-09 against cookiecutter hooks, copier home and updating, and cruft pages.
