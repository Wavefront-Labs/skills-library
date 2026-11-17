---
id: computing-software.web-development.docusaurus.config-categories-and-site-config
name: config-categories-and-site-config
category: computing-software
field: web-development
product: docusaurus
tags: [site-metadata, custom-fields, use-docusaurus-context, site-config, deployment-config]
level: practitioner
status: docs-checked
description: "The groups of fields in docusaurus.config.js, adding customFields, and reading siteConfig in React components with useDocusaurusContext."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Config fields fall into groups:

- Site metadata: `title`, `url`, `baseUrl`, `favicon`. Used for titles, tab icon, social sharing and for generating correct static file paths.
- Deployment: `projectName`, `organizationName`, optionally `deploymentBranch`; used by `docusaurus deploy`.
- Themes, plugins, presets: the `themes`, `plugins` and `presets` fields.
- Custom fields.

Docusaurus guards the config file from unknown fields. Put your own data in `customFields`:

```js title="docusaurus.config.js"
export default {
  customFields: {
    image: '',
    keywords: [],
  },
};
```

The config object is available to every component through React context as `siteConfig`:

```jsx
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const Hello = () => {
  const {siteConfig} = useDocusaurusContext();
  const {title, tagline} = siteConfig;
  return <div>{`${title} · ${tagline}`}</div>;
};
```

If a value is only needed client-side, create your own JS file and import it as an ES module instead of putting it in the config.

## Checked

2026-11-04: read the Docusaurus configuration page in full. Confirmed the field groups, customFields, and siteConfig via useDocusaurusContext. Nothing removed.

Method: documentation only; no commands were run.
