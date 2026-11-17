---
id: computing-software.collaboration-platform-administration.mattermost.custom-branding
name: custom-branding
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [custom-branding, site-name, login-page, customization]
level: intro
status: docs-checked
description: "Brand a Mattermost server: enable custom branding, set site name, brand image, brand text and site description with the documented limits."
sources: ["https://docs.mattermost.com/administration-guide/configure/custom-branding-tools.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom branding

Open System Console > Site Configuration > Customization. Set Enable Custom Branding to true, choose a Site Name, upload a Custom Brand Image and enter Custom Brand Text, then Save. Users see the branding on the login page the next time they log in. To remove the image, click the X in its top right corner and Save; Enable Custom Branding must still be true to do this.

Fields:
- Site name: limited to 30 characters or less; shown in the header and footer of the login, team selection, team creation and account creation pages, in email invitations, and replaces "Mattermost" on the About page. It applies site-wide, not per team.
- Custom brand image: shown on the left of the desktop login page. JPG, PNG, TIFF and BMP are supported; recommended 200 to 500 px wide and high and under 2 MB, because it loads for every user logging in on desktop.
- Custom brand text: a tagline or welcome message under the image on desktop login, up to 500 characters, with message Markdown formatting.
- Site description: text under the site name on the login page; defaults to "All team communication in one place, searchable and accessible anywhere"; maximum 1024 characters, no Markdown.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/configure/custom-branding-tools. Removed the unsupported image-size and Terms of Service advice; added the documented 30 character site name limit.

Method: documentation only; no commands were run.
