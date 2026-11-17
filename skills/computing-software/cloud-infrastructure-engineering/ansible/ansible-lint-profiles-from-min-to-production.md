---
id: computing-software.cloud-infrastructure-engineering.ansible.ansible-lint-profiles-from-min-to-production
name: ansible-lint-profiles-from-min-to-production
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-lint, lint-profiles, production-profile, shared-profile, progressive-adoption, ci-quality-gate]
level: practitioner
status: docs-checked
description: "Adopt ansible-lint profiles stepwise (min, basic, moderate, safety, shared, production) on an existing codebase, gating CI at a profile and ratcheting up without a big-bang fix."
sources: ["ansible-lint profiles (https://ansible.readthedocs.io/projects/lint/profiles/)", "ansible-lint configuration (https://ansible.readthedocs.io/projects/lint/configuring/)", "ansible-lint usage (https://ansible.readthedocs.io/projects/lint/usage/)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ansible-lint profiles: min to production

Goal: turn on linting for a large legacy repo without a 4,000-finding wall, and raise the bar
in controlled steps until it meets `production`.

## The ladder (each includes the ones before)
| Profile | Adds, roughly |
|---|---|
| `min` | Things that break execution: syntax, load errors, schema |
| `basic` | Common coding issues and standard style: `command-instead-of-module`, `command-instead-of-shell`, `deprecated-module`, `jinja`, `key-order`, `name`, `partial-become`, `role-name`, `schema`, `var-naming`, `yaml` |
| `moderate` | Readability: `name[template]`, `name[casing]` (`name[imperative]` and `spell-var-name` are listed as not yet implemented) |
| `safety` | Non-determinism and risk: `avoid-implicit`, `latest`, `package-latest`, `risky-file-permissions`, `risky-octal`, `risky-shell-pipe` |
| `shared` | Packaging and publishing: `galaxy`, `ignore-errors`, `meta-incorrect`, `meta-no-tags`, `meta-runtime`, `no-changed-when`, `no-handler`, `no-relative-paths` |
| `production` | Bar for AAP validated or certified content: `fqcn` (other listed rules such as `sanity` are not yet implemented) |
Exact rule membership changes between ansible-lint releases; see it for your version:
```bash
ansible-lint --list-profiles      # short form: -P
```

## Rollout
1. Pin the tool version (in requirements and the pre-commit `rev:`) so new releases don't move the goalposts mid-sprint.
2. Start at the profile that passes today:
```yaml
# .ansible-lint
profile: min
exclude_paths: [.cache/, collections/ansible_collections/]
```
3. Generate a baseline for the next level instead of fixing everything at once:
```bash
ansible-lint --profile basic --generate-ignore    # writes .ansible-lint-ignore (file + rule per line)
```
New code must pass `basic`; existing violations are tracked in the ignore file and burned down.
4. Use `ansible-lint --fix` (rules with transforms include `fqcn`, `yaml`, `key-order`, `no-free-form`, `jinja`) per rule in separate PRs to keep reviews readable: `ansible-lint --fix=fqcn`.
5. When the ignore file is empty, bump `profile:` and repeat.

## CI gate
```yaml
- uses: ansible/ansible-lint@main   # GitHub Action from the ansible-lint repository; pin a release tag or SHA in real use
```
Or `ansible-lint --profile production --strict` (`--strict` returns non-zero on warnings as well as errors).
The `production` profile is the bar for content going into Ansible Automation Platform as validated or certified content.

## Gotchas
- `profile:` in config and `--profile` on CLI: a scalar passed on the command line overrides the file; make CI read the config only.
- `skip_list` hides violations from the output; the ignore file keeps them visible as warnings, so prefer it (or `# noqa: rule` with a reason).
- `warn_list` rules don't fail the run — people stop reading them; keep it short.
- Opt-in rules (for example `no-log-password`, `no-same-owner`, `name[prefix]`) are not loaded automatically; add them to `enable_list`.

## Verify
- [ ] `ansible-lint` in CI fails a PR that introduces a new `basic` violation in a file that was clean before.
- [ ] The `.ansible-lint-ignore` line count trends down.

## Checked
Checked 2026-10-23 against the ansible-lint documentation source on GitHub (profiles.md, configuring.md, usage.md, cli.py; latest release v26.10.1): the rule list of each profile and which entries are not yet implemented, `--list-profiles`/`-P`, `--strict`, `--generate-ignore`, `--fix` rules, CLI-versus-file precedence, opt-in rules and the ansible/ansible-lint GitHub Action (action.yml exists in the repository). Removed the unconfirmed pinned version `25.x`, the `@v25` tag and the sentence about private hub certification. The Red Hat certified-content source entry was replaced by the profiles page, which states the production-profile purpose.
Method: documentation only; no commands were run.
