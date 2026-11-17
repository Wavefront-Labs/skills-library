---
id: media-communication.content-creation-and-audience-growth.wordpress.editorial-publishing-workflow
name: editorial-publishing-workflow
category: media-communication
field: content-creation-and-audience-growth
product: wordpress
tags: [wordpress, block-editor, cms, editorial-workflow, publishing, roles, scheduling, wp-cron, categories, tags, taxonomy, blog]
level: practitioner
status: docs-checked
description: "Run a WordPress site as an editorial publication: pick the right user roles, schedule posts reliably given how WP-Cron works, and keep taxonomy and corrections disciplined."
sources:
  - https://wordpress.org/documentation/article/roles-and-capabilities/
  - https://developer.wordpress.org/plugins/cron/
  - https://developer.wordpress.org/advanced-administration/wordpress/wp-config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WordPress editorial publishing workflow

**Goal:** get stories from draft to published repeatably, with the right people able to do the right things and no "oops, that went live" moments. For theme and plugin development see `computing-software.web-development.wordpress.child-themes-plugins-and-hooks`.

## 1. Set roles before you invite anyone

Core roles as described in the WordPress documentation:
- **Administrator**: access to all the administration features.
- **Editor**: can publish and manage posts, including other people's.
- **Author**: can publish and manage their own posts.
- **Contributor**: can write and manage their own posts but cannot publish them.
- **Subscriber**: can only manage their profile.

Give freelancers and new writers Contributor so a human publishes their work, section editors Editor, and Administrator to as few people as possible. The core roles do not include a custom review stage; if you need one, evaluate an editorial-workflow plugin on a staging copy first.

## 2. Scheduling and WP-Cron

Scheduled posts depend on WP-Cron, which checks its list of scheduled tasks on every page load and "is only triggered on page load". A task scheduled for 2:00 PM when no page loads until 5:00 PM runs late, at the next page load. Low-traffic sites therefore miss schedules.

`DISABLE_WP_CRON` set to true in `wp-config.php` turns the built-in handling off entirely, so only do that if something else (such as a server-level scheduler) triggers WordPress cron. The `ALTERNATE_WP_CRON` constant is documented as a workaround often used when scheduled posts do not publish on time, with the warning that it carries risk because it depends on a non-native service.

## 3. Taxonomy discipline

- Categories are a small, deliberate set of sections owned by editors; every post gets one primary category.
- Tags are specific entities or topics. Search existing tags before creating one, merge near-duplicates on a schedule, and delete tags used once.
- Decide permalinks once, before launch; changing later breaks inbound links unless you add redirects.

## 4. Corrections

Do not silently rewrite a published claim: add a visible, dated correction notice. If you change the slug of a live post, add a redirect.

## Verify

- [ ] Each person has the lowest role that lets them do their job.
- [ ] A test post scheduled a few minutes ahead published on time rather than showing a missed schedule.
- [ ] No duplicate tags among the most used.
- [ ] Changed slugs have redirects.

## Checked

2026-11-01. Confirmed against the WordPress Roles and Capabilities documentation, the WP-Cron page of the plugin handbook and the wp-config page (sources above): the five role descriptions, WP-Cron page-load triggering and late runs, DISABLE_WP_CRON and ALTERNATE_WP_CRON. Removed as not confirmed: the editor sidebar and preview menu paths, Pending Review status for contributor posts, Contributors being unable to upload media, the claim that the `wp-cron.php` file should be called by a host cron, SEO plugin field names, taxonomy size numbers, patterns and revisions UI, caching and image-size advice.
Method: documentation only; no commands were run.
