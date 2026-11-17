---
id: computing-software.web-development.docusaurus.i18n-translate-react-code
name: i18n-translate-react-code
category: computing-software
field: web-development
product: docusaurus
tags: [translate-component, translate-function, write-translations, plurals, code-json]
level: practitioner
status: docs-checked
description: "Translate Docusaurus React code with the Translate component and translate(), extract labels with write-translations, static-message rules, and plural forms."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/i18n/i18n-tutorial.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two APIs from `@docusaurus/Translate`: the `<Translate>` component (a JSX element) and the `translate()` function (returns a string, for props such as `alt`).

```jsx
import Translate, {translate} from '@docusaurus/Translate';

<h1><Translate>Welcome to my website</Translate></h1>

<Translate
  id="homepage.visitMyBlog"
  description="Message asking the user to visit my blog"
  values={{blogLink: <Link to="/blog">blog</Link>}}>
  {'You can also visit my {blogLink}'}
</Translate>

<img alt={translate({message: 'Home icon', description: 'Homepage icon alt'})} />
```

A JSX element is an object: in string-only contexts (like `<option>` children) it becomes `[object Object]`, so use `translate()` there. The runtime is deliberately small: only placeholder interpolation, a subset of ICU Message Format. Use a library like react-intl for genders or complex plurals.

Extract labels:

```bash
npm run write-translations -- --locale fr
```

This statically analyzes the code and writes `i18n/fr/code.json` (a map from ID, or the default message when no ID, to `message` and `description`), plus plugin and theme files such as `i18n/fr/docusaurus-theme-classic/navbar.json`. Translate the `message` values. Navbar and footer labels, sidebar category labels and the blog sidebar title are included.

Messages must be static strings. `<Translate>{item.title}</Translate>` cannot be extracted; instead wrap the literals where they are defined.

Plurals: pipe-separated forms ordered zero, one, two, few, many, other, limited to the forms the language has (English: `One post|{count} posts`). Use `usePluralForm().selectMessage(count, translate(...))` from `@docusaurus/theme-common`.

## Checked

2026-11-04: read the Docusaurus i18n tutorial in full. Confirmed Translate and translate(), the object coercion warning, the small ICU subset runtime, write-translations output files, the static message rule and the plural form order and usePluralForm usage. Nothing removed.

Method: documentation only; no commands were run.
