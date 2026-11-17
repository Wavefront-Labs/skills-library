---
id: computing-software.web-development.htmx.htmx-template-fragments
name: htmx-template-fragments
category: computing-software
field: web-development
product: htmx
tags: [htmx, templates, template-fragments, ssr, locality-of-behavior, partials]
level: practitioner
status: docs-checked
description: "Render just part of a server template for htmx partial updates instead of splitting files: the template-fragments idea, a worked example, and known libraries per language."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/essays/template-fragments.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve both a full page and a small partial update from one template file, instead of extracting each partial into its own file.

The problem. A contact detail page shows an Archive or Unarchive button depending on state, inside `<div hx-target="this">`. Clicking a button should re-render only the button. Classic fix: move the button into `archive-ui.html` and `#include` it. Pushed to extremes this yields many small templates that are hard to reason about and hides the feature when you read `detail.html`.

The fix: render a named fragment of the template. Example in Chill templates (the essay's own, early-alpha Java engine), where `#fragment archive-ui ... #end` marks the block:

```html
<div hx-target="this">
  #fragment archive-ui
    #if contact.archived
    <button hx-patch="/contacts/${contact.id}/unarchive">Unarchive</button>
    #else
    <button hx-delete="/contacts/${contact.id}">Archive</button>
    #end
  #end
</div>
```

```java
ChillTemplates.render("/contacts/detail.html", "contact", c);              // whole page
ChillTemplates.render("/contacts/detail.html#archive-ui", "contact", c);   // only the buttons
```

Use the first when rendering the entire detail page and the second when handling the archive/unarchive actions and re-rendering only the buttons. The UI stays in one file, which follows Locality of Behavior.

Known implementations (from the essay; check each library's docs for current syntax)
- Go: standard library `text/template` block actions; templ.
- Java: Thymeleaf; Chill Templates; Quarkus Qute; JStachio (mustache).
- JavaScript: Jeasx.
- PHP: Latte (third argument names the block, `$Latte_Engine->render('path/to/template.latte', ['foo' => 'bar'], 'content')`); Laravel Blade (built in since v9.x); Twig (`$template->renderBlock('block_name', [...])`).
- Python: django-render-block, jinja2-fragments, jinja_partials, chameleon_partials, htmlgenerator, django-template-partials, django-block-fragments.
- .NET: Giraffe.ViewEngine.Htmx. Rust: MiniJinja (`render_block`), Askama (block fragments). Raku: Cro Templates.

## Checked

2026-11-07. Confirmed against the template-fragments essay: the problem and `#include` split, the Chill `#fragment` example and both `ChillTemplates.render` calls, the Locality of Behavior point, and every listed implementation including the Latte, Blade and Twig details. Reworded the page-versus-handler sentence to the essay's wording. Removed the invented Verify step. The essay is from 2022 (updated 2023), so library lists may be out of date.
Method: documentation only; no commands were run.
