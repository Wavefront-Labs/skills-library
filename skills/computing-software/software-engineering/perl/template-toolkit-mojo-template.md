---
id: computing-software.software-engineering.perl.template-toolkit-mojo-template
name: template-toolkit-mojo-template
category: computing-software
field: software-engineering
product: perl
tags: [perl, mojo-template, html-escaping, perl-templating, template-toolkit-mojo-template]
level: practitioner
status: docs-checked
description: "Render text and HTML with Mojo::Template: tag syntax, vars, auto_escape and the escape marks; Template Toolkit points to its docs."
sources: ["https://docs.mojolicious.org/Mojo/Template"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mojo::Template (and where Template Toolkit fits)

**Goal:** separate presentation from code safely.

```perl
use Mojo::Template;
my $mt = Mojo::Template->new(vars => 1, auto_escape => 1);
say $mt->render(<<'EOT', { name => $name, rows => \@rows });
% for my $r (@$rows) {
<tr><td><%= $r->{id} %></td></tr>
% }
EOT
```

## Syntax (Mojo::Template docs)
- `<% Perl code %>` runs code; `<%= expr %>` inserts the result; `<%== expr %>` inserts the XML-escaped result; `<%# comment %>`.
- Line forms: lines starting with `%` are Perl code, `%=` and `%==` are expression lines treated as `<%= ... %>` and `<%== ... %>`.
- By default `<%=` is NOT escaped and `<%==` is XML-escaped. The `auto_escape` attribute reverses this (`<%=` escaped, `<%==` raw); it is the default in Mojolicious `.ep` templates. The `escape` attribute is the escape callback (default `xml_escape` from Mojo::Util); `escape_mark` is the escape character (default `=`).
- Wrap trusted markup with `b('<div>..</div>')` to exclude it from escaping.
- `=%>` trims whitespace around an expression; a backslash before a newline removes the newline.
- `vars(1)` makes the keys of the hash passed to `render` available as variables (`$title` rather than `$_[0]`); without it, arguments arrive as `@_`.
- `render` compiles and runs the template; `parse` followed by `process('Bender')` passes arguments, as in the docs example.

## Rules
- Turn on `auto_escape` in your own pipeline so a missed escape does not become XSS.
- Template Toolkit (`Template` module): the template-toolkit.org docs landing page was the only source reachable, so its options, filters and escaping defaults are not covered here; read its documentation before relying on them.

## Self-check
- [ ] A name of `<script>` is rendered escaped when it goes through an escaping tag.

## Checked
2026-11-09. Searched the Mojo::Template page for tag syntax, auto_escape, escape, escape_mark, vars, trimming and examples; line-level forms taken from its syntax section. Removed all Template Toolkit specifics (the cited page is a landing page), the caching, path traversal, Text::Template and encoding advice, and the exact output self-check.
Method: documentation only; no commands were run.
