---
id: computing-software.web-development.storybook.visual-testing-chromatic
name: visual-testing-chromatic
category: computing-software
field: web-development
product: storybook
tags: [visual-testing, chromatic, baselines, ui-review, visual-regression]
level: practitioner
status: docs-checked
description: "Run visual regression tests with the Chromatic addon and CI, review diffs and accept baselines."
sources:
  - https://storybook.js.org/docs/writing-tests/visual-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Visual testing with Chromatic

Goal: detect unintended UI changes by comparing story snapshots to baselines (last known good snapshots).

Install the official addon `@chromatic-com/storybook` (by the Storybook maintainers):

```shell
npx storybook@latest add @chromatic-com/storybook
```
Start Storybook and open the new Visual Tests addon panel. Sign in to Chromatic (an account can be created during sign in), pick or create a project, then press the "Catch a UI change" button. That first build creates the baseline snapshots.

Run: after a code change, press the run button in the Visual tests section of the expanded testing widget (sidebar) or in the top right of the Visual Tests addon panel. Stories are sent to the cloud to take snapshots. Changed stories are highlighted in the sidebar; open the story and the panel to see which pixels changed. Accept intentional changes as baselines locally; fix unintended ones and rerun. When done accepting, push the code so baselines sync to the cloud for anyone who checks out the branch.

CI: add a step to your CI workflow to run Chromatic (GitHub Actions, GitLab Pipelines, Bitbucket Pipelines, CircleCI, Travis CI, Jenkins, Azure Pipelines or a custom CI provider) and configure environment variables so CI authenticates with Chromatic (the project token). Changes accepted as baselines in the addon are auto-accepted in CI. Once set up, pull/merge requests get a UI Tests check; make it required in your Git provider.

`chromatic.config.json` options: `projectId` (automatically configured), `buildScriptName` (optional custom Storybook build script), `debug` (optional verbose output), `zip` (optional, recommended for large projects; deploys Storybook to Chromatic as a zip file).

Visual tests compare rendered pixels; snapshot tests compare rendered markup, which can give more false positives.

Verify: a pull request shows the UI Tests status check.

## Checked
Read the whole visual-testing page (storybookjs/storybook docs/writing-tests/visual-testing.mdx) and the page's install snippet chromatic-storybook-add.md on 2026-11-08. Confirmed the addon name, install command, first-build baseline, both run locations, review and accept flow, CI providers, auto-accept, PR check and the four config options. Removed: the `npx chromatic --project-token` command (not on the page) and the "multiple browsers" detail.
Method: docs-only read of cited pages, 2026-11-08
