---
id: computing-software.web-development.storybook.mocking-network-msw
name: mocking-network-msw
category: computing-software
field: web-development
product: storybook
tags: [msw, mock-service-worker, network-mocking, rest-mocking, graphql-mocking]
level: advanced
status: docs-checked
description: "Mock REST and GraphQL requests in stories with Mock Service Worker and the msw-storybook-addon."
sources:
  - https://storybook.js.org/docs/writing-stories/mocking-data-and-modules/mocking-network-requests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mocking network requests with MSW

Goal: make components that fetch data render deterministic stories.

The docs use Mock Service Worker (MSW) with the `msw-storybook-addon` (v3 instructions; v2 projects can migrate with `npx msw-storybook-migrate`).

Setup:
1. Install `msw` and `msw-storybook-addon` if necessary.
2. Generate the worker file if you do not have one (`npx msw init public/`; Angular projects save it in a folder such as `src`).
3. Make sure `staticDirs` in `main.ts` includes the folder with the service worker file.
4. Initialize the addon and register it for all stories in the preview file (a project-level loader in CSF 3, or via the preview config in CSF 4).

Writing stories:
- REST (fetch or other clients) and GraphQL (URQL, Apollo, and others) are both supported by defining handlers per story.
- Define request handlers in `beforeEach` on the story. You can also use `beforeEach` at component or project level to share handlers.
- Create one story for success and one for an error response to cover both states.
- In CSF 3 the `msw` parameter could define handlers per story, component or project.

The page's REST example uses `fetch` and says other clients such as `axios` follow the same principles; its GraphQL example uses Apollo Client (URQL for Svelte).

## Checked

Method: 2026-11-08 read docs/writing-stories/mocking-data-and-modules/mocking-network-requests.mdx from the Storybook repo. Removed an unsupported MSW minimum-version claim, a "service worker missing" gotcha and a Verify step; setup order, `beforeEach` handlers and CSF 3 `msw` parameter match the page. Install and init code snippets were not read.
