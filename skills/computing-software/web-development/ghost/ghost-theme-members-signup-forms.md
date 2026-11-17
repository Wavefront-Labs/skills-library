---
id: computing-software.web-development.ghost.ghost-theme-members-signup-forms
name: ghost-theme-members-signup-forms
category: computing-software
field: web-development
product: ghost
tags: [ghost, theme, members, portal, data-members-form, newsletter-subscription]
level: advanced
status: docs-checked
description: "Build custom Ghost member signup forms with data-members attributes, Portal links and newsletter selection."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/members.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add membership signup to a theme.

Two approaches: use Portal (the embeddable membership UI, which works in any theme and can be opened by links or the `data-portal` attribute, adding classes `gh-portal-open` and `gh-portal-close` to the element for styling) or build custom flows.

Custom signup form:
- Put `data-members-form` on the form element.
- Put `data-members-email` on the email input.
- Optional `data-members-name` on a name input.
- Optional `data-members-error` on an element that shows errors such as too many attempts or a newsletter that no longer exists.
- Newsletter choice: add `data-members-newsletter` to an input. Without a choice a new member is subscribed to the site's default newsletter.

Newsletter details: `data-members-newsletter` takes the newsletter name as its value. Use a `type="hidden"` input to subscribe silently (repeat the input for several newsletters), or checkbox or radio inputs to let the user choose. A dynamic form can loop `{{#get "newsletters"}}{{#foreach newsletters}}` and output `{{name}}` as each value.

Labels: a hidden input with `data-members-label` and a value such as `Early Adopters` applies that label from a specific form.

`data-members-form` accepts optional values: `signin` (sends a signin email to existing members), `signup` (sends a signup email to new members; a signin email if the address is already a member) and `subscribe` (same, with "subscription" wording). `data-members-autoredirect="false"` redirects to the homepage on login; the default true returns the user to the page where they signed up. Forms get the classes `loading`, `success` or `error`.

Portal links can be absolute (`https://example.com/#/portal/signup`, which goes to the homepage and opens a Portal screen) or relative (`#/portal/signup`, which opens Portal on the current page). The page does not list the other Portal screens.

Sign in: sign-in forms send a magic link by default; add `data-members-otc="true"` to the `data-members-form="signin"` form to also offer a one-time code, entered in a Portal modal. Sign out: `<a href="javascript:" data-members-signout>`; use `{{#if @member}}` to switch between sign out and sign in.

Paid checkout: `<a href="javascript:" data-portal="signup/TIER_ID/monthly">` (or `yearly`); the tier data attribute is found in Portal settings at `/ghost/#/settings/portal/edit` in your Admin URL.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 612 lines, code samples inline, no imported snippets): themes/members.mdx. Form attributes, newsletter default and Portal class claims match. Removed as unconfirmed: the claim that the page lists Portal screens and hash paths, the transactional mail dependency, and the Verify step. Added newsletter options, labels, form values, sign-in and sign-out, and checkout buttons from the page. The page's dynamic newsletter example has a stray `=` after `data-members-form`; not copied.
Method: documentation only; no commands were run.
