---
id: computing-software.devops-ci-cd.helm.chart-releaser-github-pages
name: chart-releaser-github-pages
category: computing-software
field: devops-ci-cd
product: helm
tags: [chart-releaser, github-pages, gh-pages, github-actions, publish-chart, repository]
level: practitioner
status: docs-checked
description: "Publish a Helm repository on GitHub Pages using the chart-releaser action, with charts in /charts and output on gh-pages."
sources:
  - https://helm.sh/docs/howto/chart_releaser_action/
  - https://helm.sh/docs/topics/chart_repository/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Chart Releaser Action is a GitHub Action that turns a GitHub project into a self-hosted Helm chart repo using the `helm/chart-releaser` CLI, with charts published through GitHub Pages.

Repository layout the guide prescribes:

- A Git repository under your GitHub organisation (the guide suggests `helm-charts`; other names are fine).
- Chart sources on the `main` branch under a top-level `/charts` directory.
- A `gh-pages` branch to publish the charts. The action creates its changes there, but you may create the branch yourself and add a `README.md` that visitors will see with install instructions.

The charts are then served at `https://<orgname>.github.io/helm-charts`. Suggested README usage text:

```bash
helm repo add <alias> https://<orgname>.github.io/helm-charts
helm repo update
helm search repo <alias>
helm install my-<chart-name> <alias>/<chart-name>
```

Workflow file `.github/workflows/release.yml` on `main` (from the guide):

```yaml
name: Release Charts
on:
  push:
    branches:
      - main
jobs:
  release:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Configure Git
        run: |
          git config user.name "$GITHUB_ACTOR"
          git config user.email "$GITHUB_ACTOR@users.noreply.github.com"
      - name: Run chart-releaser
        uses: helm/chart-releaser-action@v1.6.0
        env:
          CR_TOKEN: "${{ secrets.GITHUB_TOKEN }}"
```

On every push to `main` the action checks each chart; whenever there is a new chart version it creates a GitHub release named for the chart version, attaches the packaged chart artifacts, and creates or updates `index.yaml` with metadata about those releases, which is then hosted on GitHub Pages. So bump `version` in `Chart.yaml` for each chart change you want released. The guide pins `v1.6.0` in the example and says to change it to the latest available version. It notes the action is almost always used together with the Helm chart-testing action and the kind cluster action.

The repository guide's manual alternative: create a `gh-pages` branch, set it as the Pages source in repository settings (with HTTPS enforced), or serve a `docs/` directory instead. Other hosting options it names include GCS buckets, Cloudsmith, JFrog Artifactory, GitLab Package Registry, ChartMuseum, an ordinary web server, and it suggests considering an OCI registry for new repositories.

## Checked

2026-11-08. Checked against the Helm chart releaser action how-to page, read in full (workflow file, action version, release and index.yaml behaviour). Removed unsourced claims.

Method: documentation only; no commands were run.
