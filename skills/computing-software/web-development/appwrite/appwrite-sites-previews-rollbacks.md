---
id: computing-software.web-development.appwrite.appwrite-sites-previews-rollbacks
name: appwrite-sites-previews-rollbacks
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, sites, previews, rollbacks, git]
level: practitioner
status: docs-checked
description: "Use pull request previews and instant rollbacks to ship and revert Sites deployments without rebuilding."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/previews/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/instant-rollbacks/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/deploy-from-git/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/domains/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: safe releases.

Previews: when Git is connected, a pull request on the GitHub repo produces a preview deployment with its own URL (Deployments tab > ready deployment > Visit). Previews are only for authorized users, meaning members of your Appwrite organization, not the public. Appwrite also generates a branch URL (stable for the branch) and a commit URL (changes per deployment); see the domains page.

Production: pushes to the production branch (usually `main`) create, build and activate a deployment; pushes to other branches create a deployment that is not activated.

Instant rollback: Overview tab > Instant Rollback > Rollback, then pick a previously active, ready deployment. Rollbacks do not delete, modify or re-deploy code; they only change which deployment is served, with zero downtime.

Build triggers: in Settings > Git repository, branch filters and path filters with glob patterns limit which Git changes create automatic deployments.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/sites/previews, products/sites/instant-rollbacks, products/sites/deploy-from-git, products/sites/domains. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the silent-mode claim, the environment-variables gotcha and the invented Verify; branch and commit URL behaviour now backed by the domains page (added to sources); build triggers (branch and path glob filters) described from the deploy-from-git page.

Method: documentation only; no commands were run.
