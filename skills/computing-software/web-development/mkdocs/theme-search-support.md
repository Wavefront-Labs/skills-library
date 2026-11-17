---
id: computing-software.web-development.mkdocs.theme-search-support
name: theme-search-support
category: computing-software
field: web-development
product: mkdocs
tags: [theme-search, search-index-json, include-search-page, search-index-only]
level: advanced
status: docs-checked
description: "Support the search plugin in a custom MkDocs theme: guard markup, base_url script, required element IDs, theme options and the index JSON layout."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Users can disable the plugin, so wrap search markup:

```django
{% if 'search' in config.plugins %}
    search stuff here...
{% endif %}
```

For the plugin's bundled lunr.js search, the theme provides:

```django
<script>var base_url = {{ base_url|tojson }};</script>

<form action="search.html">
  <input name="q" id="mkdocs-search-query" type="text" >
</form>
<div id="mkdocs-search-results"></div>
```

The IDs `mkdocs-search-query` and `mkdocs-search-results` are required.

Options in `mkdocs_theme.yml`:
- `include_search_page`: true builds a dedicated `search/search.html` (readthedocs theme does this); false/undefined means the theme shows results itself (the mkdocs theme uses a modal).
- `search_index_only`: true/undefined means only the index is produced and the theme implements search; false makes the plugin add its templates and scripts.

Index file: `search/search_index.json` in `site_dir`, with up to `config`, `docs` (location, title, text) and `index` (only if `prebuild_index`; themes must tolerate it missing).

## Checked

2026-11-04. Confirmed against the MkDocs Developing Themes page (Search and themes: plugin guard, `base_url` script, element IDs, `include_search_page`, `search_index_only`, `search/search_index.json` layout, `prebuild_index`). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
