# Level 3 schema: products (applications and crafts)

One file per field: `taxonomy/products/<category>/<field>.yaml`. A product is the third tier —
either an **application** (a specific tool: `blender`, `react`, `autocad`) or a **craft**
(tool-agnostic know-how: `character-design`, `echocardiography`, `storywriting`). It is the
folder a skill file lives in: `skills/<category>/<field>/<product>/<skill>.md`.

```yaml
category: creative-arts
field: animation          # must exist in taxonomy/fields/<category>.yaml
products:
  - id: blender           # kebab-case, stable once skills reference it
    name: Blender
    kind: application     # application = a specific tool; craft = tool-agnostic know-how
    scope: "Headless and interactive Blender work for the animation pipeline: modelling, rigging, lighting, cel-shading, rendering."
    examples: [cel-shading, rigging, lighting, headless automation]
    status: live          # live = has skills on main; draft = proposed, no skills yet
```

## Rules
- `id` unique within the field, kebab-case, stable once any skill uses it; moves follow the
  same `aliases` mechanism as skills.
- Every (category, field, product) triple already live in `skills.index.jsonl` must appear
  with `status: live` — a product carrying real skills can never be silently dropped or
  renamed. (`check.py` enforces this.)
- `kind` is `application`, `craft` or `method`. Naming style may be either tool-named or
  function-named for historical live products (animation predates this schema); new products
  should name the tool for applications and the practice for crafts.
- **`kind: method`** is the recipe genre and is always the product id `methods`, at most one
  per field. Applications and crafts are *ingredients* — they teach how to do one thing. A
  method is the *recipe*: which skills to bundle, in what order, and to what measured
  standard, to reach a named outcome at a named quality tier. It owns no technique of its
  own; every "how" is a link to a skill id. See the Methods section of `CONTRIBUTING.md`
  for the required file shape.
- Depth follows reality: a field may have 3 products or 30. Applications list the tools
  practitioners actually use (including our own `*craft` CLIs); crafts carve the field's
  know-how into teachable areas.
- Products never re-litigate Level 1 or Level 2 boundaries: a product sits inside exactly the
  field its file belongs to.

## Checking
`python taxonomy/products/check.py` — validates file/key consistency, id uniqueness, kinds,
that each file's field exists at Level 2, and live-product protection. Fields without a
products file yet are reported as a count, not an error (Level 3 fills in gradually).
