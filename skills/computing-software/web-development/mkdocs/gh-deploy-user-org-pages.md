---
id: computing-software.web-development.mkdocs.gh-deploy-user-org-pages
name: gh-deploy-user-org-pages
category: computing-software
field: web-development
product: mkdocs
tags: [user-pages, org-pages, remote-branch, gh-deploy]
level: practitioner
status: docs-checked
description: "Deploy to GitHub User or Organization Pages by running gh-deploy from the dedicated pages repository with --config-file and --remote-branch master."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/deploying-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
User and Organization Pages sites are deployed to the `master` branch of a dedicated repository named for the account. You need local clones of both repositories:

```text
my-project/
    mkdocs.yml
    docs/
orgname.github.io/
```

After verifying changes, change directory into the pages repository and deploy:

```sh
cd ../orgname.github.io/
mkdocs gh-deploy --config-file ../my-project/mkdocs.yml --remote-branch master
```

Why both flags: the config is no longer in the working directory, and the deploy must commit to `master`. You can set the `remote_branch` config instead of the flag.

Gotcha: if you forget to `cd` to the pages repository first, the deploy commits to the `master` branch of your project, which you probably do not want.

## Checked

2026-11-04. Confirmed against Deploying your docs (Organization and User Pages): `master` branch of the dedicated repository, the directory layout, the two-flag command, the `remote_branch` override, and the wrong-directory gotcha. Removed: a generic verify line.

Method: documentation only; no commands were run.
