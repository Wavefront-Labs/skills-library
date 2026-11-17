---
id: computing-software.web-development.eleventy.validate-data
name: validate-data
category: computing-software
field: web-development
product: eleventy
tags: [eleventydataschema, data-validation, zod, schema-check]
level: practitioner
status: docs-checked
description: "Validate data cascade values in Eleventy with the eleventyDataSchema callback and a schema library such as zod, throwing on invalid values."
sources:
  - https://www.11ty.dev/docs/data-validate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The special `eleventyDataSchema` data property (3.0.0-alpha.7+) validates data. It can sit anywhere in the data cascade: front matter, directory data file, global data. Use any validation library; the docs use `zod`.

Each template that receives an `eleventyDataSchema` callback has its data passed in. Throw an error to fail the build.

Example `blog/blog.11tydata.js`: every template in the `blog` folder must have `draft` boolean or undefined.

```js
import { z } from "zod";

export default {
  eleventyDataSchema: function (data) {
    let result = z.object({
      draft: z.optional(z.boolean())
    }).safeParse(data);

    if (result.error) {
      throw new Error(z.prettifyError(result.error));
    }
  }
};
```

Because it is a directory data file, the check applies to every template in the `blog` folder.

## Checked

Method: 2026-11-08 compared against the 11ty website source markdown for the Validate Data page (data-validate). The page is short and every claim matches it; no changes to the technical content.
