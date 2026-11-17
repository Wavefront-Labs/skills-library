---
id: computing-software.web-development.eleventy.custom-tags
name: custom-tags
category: computing-software
field: web-development
product: eleventy
tags: [custom-tags, addliquidtag, addnunjuckstag, template-language-tags]
level: advanced
status: docs-checked
description: "Register low-level custom tags for Liquid and Nunjucks in Eleventy with addLiquidTag and addNunjucksTag when shortcodes are not enough."
sources:
  - https://www.11ty.dev/docs/custom-tags/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Custom tags are unrelated to the collections `tags` feature; the name comes from the upstream template languages. The docs say you probably want shortcodes instead.

**Liquid** (`addLiquidTag`), usage `{% uppercase myVar %}`:

```js
eleventyConfig.addLiquidTag("uppercase", function (liquidEngine) {
  return {
    parse: function (tagToken, remainingTokens) {
      this.str = tagToken.args; // myVar or "alice"
    },
    render: async function (scope, hash) {
      var str = await this.liquid.evalValue(this.str, scope);
      return str.toUpperCase();
    },
  };
});
```

**Nunjucks** (`addNunjucksTag`):

```js
eleventyConfig.addNunjucksTag("uppercase", function (nunjucksEngine) {
  return new (function () {
    this.tags = ["uppercase"];
    this.parse = function (parser, nodes, lexer) {
      var tok = parser.nextToken();
      var args = parser.parseSignature(null, true);
      parser.advanceAfterBlockEnd(tok.value);
      return new nodes.CallExtensionAsync(this, "run", args);
    };
    this.run = function (context, myStringArg, callback) {
      callback(null, new nunjucksEngine.runtime.SafeString(myStringArg.toUpperCase()));
    };
  })();
});
```

See the LiquidJS and Nunjucks docs for the full tag APIs.

## Checked

2026-11-04. Confirmed against the Eleventy Custom Tags page: custom tags are unrelated to collection tags, shortcodes are recommended instead, addLiquidTag and addNunjucksTag with the uppercase examples matching the page. Nothing removed.

Method: documentation only; no commands were run.
