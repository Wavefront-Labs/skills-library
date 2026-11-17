---
id: computing-software.collaboration-platform-administration.mattermost.email-template-customization
name: email-template-customization
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [email-templates, templates-folder, i18n-strings, email-footer]
level: advanced
status: docs-checked
description: "Customise Mattermost email templates: where template and i18n files live, restart and upgrade cautions, and the email footer props."
sources: ["https://docs.mattermost.com/administration-guide/configure/email-templates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customising email templates

Mattermost sends templated emails for specific events, and most deployments never change them. When customisation is needed, templates are in the templates folder of the server directory and the text for each prop is in the i18n folder; the documentation lists every available prop per email together with a short description and the i18n string key, and tells you to check the i18n strings for the exact wording.

Cautions:
- Props differ between templates and are not interchangeable unless you also change server code.
- Back up your changes to templates and i18n before upgrading the server, otherwise customisations can be lost.
- From Mattermost v11.3, changes to HTML templates need a server restart to take effect.

Example, the email footer, appended to all outgoing emails, has props Footer (message intro, key api.templates.email_footer), Organization (api.templates.email_organization), EmailInfo1, EmailInfo2 and EmailInfo3 (the three footer lines, keys api.templates.email_info1 to email_info3) and SupportEmail (no i18n key). Other templates, such as the one sent when a username changes (SendChangeUsernameEmail), list props like SiteURL, Title and Info in the same way.

Workflow: find the template, read its props table, change the matching i18n strings rather than inventing new props, restart, and send a test email through the SMTP setup to confirm the result renders.

## Checked

Confirmed against the Email templates page: templates and i18n folders, the three cautions including the v11.3 restart note, the email footer prop table and i18n keys, and the SendChangeUsernameEmail props. The workflow paragraph is the author's advice.

Method: docs-checked 2026-11-09 against the full administration-guide/configure/email-templates page (source rst from the mattermost/docs repo).
