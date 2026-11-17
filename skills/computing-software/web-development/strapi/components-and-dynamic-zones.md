---
id: computing-software.web-development.strapi.components-and-dynamic-zones
name: components-and-dynamic-zones
category: computing-software
field: web-development
product: strapi
tags: [strapi, components, dynamiczone, repeatable, schema, preview-image]
level: practitioner
status: docs-checked
description: "Define reusable components and dynamic zones in Strapi schemas, where component files live, and the component preview image."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/models.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Components and dynamic zones

Components cannot be created with CLI tools: use the Content-type Builder or write them by hand. They live in `./src/components`, each inside a subfolder named after its category.

## Component attribute
```json
{
  "attributes": {
    "openinghours": {
      "type": "component",
      "repeatable": true,
      "component": "restaurant.openinghours"
    }
  }
}
```
`component` format is `<category>.<componentName>`; `repeatable` is true or false.

## Dynamic zone
A flexible space for a mixed list of components:

```json
{
  "attributes": {
    "body": {
      "type": "dynamiczone",
      "components": ["article.slider", "article.content"]
    }
  }
}
```

## Preview image
In the component's `info`, optional `preview` is a root-relative path to an image in `public` or an absolute URL. Media Library images (served from `/uploads/`) cannot be used. It must be set manually; omitted or failing images fall back to `icon`.

```json
{
  "info": {
    "displayName": "Hero Section",
    "icon": "layout",
    "preview": "/_component-screenshots/hero-section.png"
  }
}
```

## Checked

Checked 2026-11-04 against the Strapi Models page (components, component preview images, dynamic zones). Nothing removed.

Method: documentation only; no commands were run.
