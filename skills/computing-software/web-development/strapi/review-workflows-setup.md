---
id: computing-software.web-development.strapi.review-workflows-setup
name: review-workflows-setup
category: computing-software
field: web-development
product: strapi
tags: [strapi, review-workflows, stages, content-manager, editorial]
level: intro
status: docs-checked
description: "Set up Strapi review workflows: default four stages and creating a workflow tied to content-types."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/review-workflows.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Review workflows

Path: Settings > Global settings > Review Workflows. For workflows to work in the Content Manager, configure the default one or create a new one.

The default workflow has 4 stages, in this order: To do, Ready to review, In progress, Reviewed. All can be edited, reordered or deleted, and new stages added.

## Create or edit a workflow
1. Click **Create new workflow** (or the edit icon on an existing one).
2. Fill in:

| Setting | Notes |
|---|---|
| Workflow name | unique |
| Associated to | optional; assign to one or more content-types |
| Stages | add review stages (name, colour, roles that can move content out of and into the stage) |
| Required stage for publishing | optional; entries must be exactly at that stage to be published (or choose Any stage) |

A project can have up to 200 workflows, each with up to 200 stages. Deleting a stage moves its entries to the closest previous stage (the next one if it was first); the last stage and the last workflow cannot be deleted. It is an Enterprise feature (CMS Enterprise plan).

Pair with Draft & Publish for publish control (`computing-software.web-development.strapi.draft-publish-states`).

## Checked

2026-11-04: checked against the Strapi docs page Review Workflows (features/review-workflows). Confirmed: path, the four default stages in order, create/edit form fields, plan, the 200 workflow and 200 stage limits, stage deletion behaviour. Added from the page: the Required stage for publishing setting and the stage fields. Removed: the 'rest of the form is in the page' pointer.

Method: documentation only; no commands were run.
