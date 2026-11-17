---
id: computing-software.cloud-infrastructure-engineering.ansible.collection-development-and-publishing
name: collection-development-and-publishing
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collection-development, collections, galaxy-yml, collection-build, collection-publish, ansible-galaxy, meta-runtime, action-groups, redirects, deprecation, changelog, antsibull-changelog, collection-structure, namespace, galaxy-api-key, private-automation-hub, git-source-collections, requirements-yml, semver]
level: advanced
status: docs-checked
description: "Build and ship an Ansible collection: collection init, galaxy.yml and meta/runtime.yml, roles/plugins layout, changelog fragments, build and publish to Galaxy or a private hub, requirements.yml."
sources: ["Developing collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)", "Collection structure (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)", "galaxy.yml format source (https://github.com/ansible/ansible/blob/devel/lib/ansible/galaxy/data/collections_galaxy_meta.yml)", "Distributing collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_distributing.html)", "antsibull-changelog (https://github.com/ansible-community/antsibull-changelog/blob/main/docs/changelogs.md)", "Testing collections (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_testing.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collection development and publishing

**Goal:** roles, modules and plugins shipped as one versioned artifact with a
namespace, so consumers install `acme.platform:>=2.1,<3` instead of cloning repos.

## 1. Scaffold and layout
```bash
ansible-galaxy collection init acme.platform
```
```
acme/platform/
  galaxy.yml            # name, namespace, version, dependencies, license, tags, repository
  meta/runtime.yml      # requires_ansible, action_groups, plugin_routing (redirects/deprecations)
  README.md  CHANGELOG.rst  changelogs/fragments/
  roles/<role>/         # standard role layout, docs in README + meta/argument_specs.yml
  plugins/modules/  plugins/module_utils/  plugins/filter/  plugins/lookup/  plugins/inventory/  plugins/action/
  playbooks/            # runnable as acme.platform.site (FQCN playbook)
  docs/  tests/         # ansible-test sanity/units/integration
```
galaxy.yml essentials (`namespace`, `name`, `version`, `readme` and `authors` are required):
```yaml
namespace: acme
name: platform
version: 2.1.0
readme: README.md
authors: ["Platform team"]
license: [MIT]
dependencies: {"ansible.posix": ">=1.5.0", "community.general": ">=8.0.0"}
repository: https://git.example/acme/platform
tags: [infrastructure, linux]
build_ignore: [".git*", "tests/output", "*.tar.gz", ".venv"]
```
meta/runtime.yml:
```yaml
requires_ansible: ">=2.15.0"
action_groups:
  platform: [acme.platform.app_deploy, acme.platform.app_facts]
plugin_routing:
  modules:
    old_deploy: {redirect: acme.platform.app_deploy, deprecation: {removal_version: 3.0.0, warning_text: "use app_deploy"}}
```

## 2. Develop in place
Put the checkout at `<collections_path>/ansible_collections/acme/platform` (symlink is fine) so
`ansible-playbook` and `ansible-test` resolve `acme.platform.*` without rebuilding. Inside the
collection reference your own content by FQCN; `module_utils` import as
`from ansible_collections.acme.platform.plugins.module_utils.common import X`.

## 3. Changelog and version
```bash
pip install antsibull-changelog
antsibull-changelog init .         # once
# per change: changelogs/fragments/123-fix-restart.yml  -> {bugfixes: ["app_deploy - no longer restarts twice"]}
antsibull-changelog release        # at galaxy.yml version bump; writes CHANGELOG.rst + changelogs/changelog.yaml
```
Semantic versioning: new modules, plugins, parameters or return values = minor; incompatible changes = major; bug fixes = patch (keep a `plugin_routing` redirect when renaming). A published version cannot be changed or deleted, and a new upload needs a higher version than the latest published one.

## 4. Build, test, publish
```bash
ansible-lint && ansible-test sanity --docker default && ansible-test units --docker default
ansible-galaxy collection build                 # -> acme-platform-2.1.0.tar.gz (respects build_ignore)
ansible-galaxy collection install acme-platform-2.1.0.tar.gz -p /tmp/t && ANSIBLE_COLLECTIONS_PATH=/tmp/t ansible-doc acme.platform.app_deploy   # smoke
ansible-galaxy collection publish acme-platform-2.1.0.tar.gz --token "$GALAXY_API_KEY"   # or --server from ansible.cfg [galaxy] server_list
```
Private hub: configure `[galaxy] server_list = hub` and `[galaxy_server.hub] url=https://hub.example/api/galaxy/ token=...`. The `--token` argument is insecure on a shared host (it exposes the secret on the command line); prefer the token in the server configuration. Tag the git commit `v2.1.0`; CI publishes on tag.

## 5. Consumers
```yaml
# requirements.yml
collections:
  - {name: acme.platform, version: ">=2.1.0,<3.0.0"}
  - {name: https://git.example/acme/platform.git, type: git, version: v2.1.0}   # straight from git, needs galaxy.yml
  - {name: ./acme-platform-2.1.0.tar.gz, type: file}
```
`ansible-galaxy collection install -r requirements.yml -p collections/` then `collections_path = ./collections` in `ansible.cfg`.
Dependencies in `galaxy.yml` are collections that must be installed for the collection to be usable, resolved by `ansible-galaxy` (not pip); document Python dependencies in the README.

## Gotchas
- Use a full semantic version (`2.1.0`, not `2.1`).
- `build_ignore` (or manifest directives) controls what is packed; add venvs and other local files to it (`tests/output` is already excluded by default).
- `ansible-test` must run from the collection directory, whose path must include `ansible_collections/<ns>/<name>`.
- Renaming a module without `plugin_routing` breaks every consumer's playbook at a minor bump; redirects are free.
- Keep `requires_ansible` honest (test on the minimum ansible-core).

## Verify
- [ ] `ansible-galaxy collection build` produces a tarball whose `tar tzf` shows no `.git`, venv or test output.
- [ ] After installing the tarball to a clean path, `ansible-doc` renders every module and role argument spec.
- [ ] `ansible-test sanity --docker default` is clean and `antsibull-changelog lint` passes.
- [ ] A consumer project with `version: ">=2.1.0,<3.0.0"` installs the published version from the hub.

## Checked

Checked 2026-10-26 against ansible-documentation devel (collection structure, creating, distributing, testing pages; installing snippets), ansible-core `collections_galaxy_meta.yml` (required keys) and the antsibull-changelog docs. Confirmed: layout and `meta/runtime.yml` keys (`requires_ansible`, `plugin_routing`, `action_groups`), FQCN playbooks (ansible-core 2.11+), `--token`/`--server` for publish, semantic versioning rules, antsibull-changelog `init`, `release` and `lint`, requirements.yml `type: git` and `type: file`, `ansible-test` path rule and `--docker default`. Replaced `ansible-doc -M` with `ANSIBLE_COLLECTIONS_PATH`. Removed unconfirmed hub staging, role dependency, build error, import-failure and lint claims.

Method: documentation only; no commands were run.
