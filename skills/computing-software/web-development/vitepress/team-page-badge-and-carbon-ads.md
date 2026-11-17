---
id: computing-software.web-development.vitepress.team-page-badge-and-carbon-ads
name: team-page-badge-and-carbon-ads
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, team-page, vpteammembers, badge-component, carbon-ads, vpteampage, team-members]
level: intro
status: docs-checked
description: "Show team member cards (VPTeamMembers, VPTeamPage), status Badges in headings, and Carbon Ads config."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-team-page.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-badge.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-carbon-ads.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/extending-default-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Team members.** Import components from `vitepress/theme` (from `vitepress/theme-without-fonts` if you dropped Inter):

```html
<script setup>
import { VPTeamMembers } from 'vitepress/theme'
const members = [
  { avatar: 'https://www.github.com/yyx990803.png', name: 'Evan You', title: 'Creator',
    links: [{ icon: 'github', link: 'https://github.com/yyx990803' }] }
]
</script>
# Our Team
<VPTeamMembers size="small" :members />
```

Member fields: `avatar`, `name`, `title`, `org`, `orgLink`, `desc`, `links` (SocialLink[]), `sponsor`, `actionText` (default `Sponsor`). Sizes `small` or `medium` (default `medium`).

**Full team page:** frontmatter `layout: page`, wrap in `<VPTeamPage>`, add `<VPTeamPageTitle>` with `#title` and `#lead` slots, `<VPTeamMembers>`, and sections with `<VPTeamPageSection>` (slots `#title`, `#lead`, `#members`).

**Badge** (globally available) adds status to headings: `### Title <Badge type="tip" text="^1.9.0" />`. Types: `info`, `note`, `tip` (default), `important`, `caution`, `warning`, `danger`; it accepts child content instead of `text`. Recolour with `--vp-badge-<type>-border|text|bg` variables.

**Carbon Ads:** `themeConfig.carbonAds = { code, placement, format: 'classic' | 'responsive' | 'cover' }`; the values build the script URL `//cdn.carbonads.com/carbon.js?serve=${code}&placement=${placement}&format=${format}`.

Verify: the team cards and badges render in a built page.

## Checked

2026-11-08. Read the VitePress docs source pages default-theme-team-page, default-theme-badge, default-theme-carbon-ads, default-theme-config (carbonAds) and extending-default-theme (theme-without-fonts). Confirmed member fields, sizes, the page components and slots, badge types, props and CSS variables, and the Carbon Ads options and URL. Removed the claim that ads show only on doc layout pages, which no page states.

Method: docs-only read of cited pages, 2026-11-08
