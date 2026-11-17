---
id: creative-arts.animation.blender.freestyle-python
name: freestyle-python
category: creative-arts
field: animation
product: blender
tags: [blender, freestyle-python, freestyle-scripting, freestyle, style-modules, npr, python]
level: advanced
status: docs-checked
description: "Script Freestyle line styles in Python: Python Scripting control mode, style modules, predicates, chaining and shaders, plus scripting Parameter Editor settings via bpy."
sources:
  - https://docs.blender.org/manual/en/latest/render/freestyle/python.html
  - https://docs.blender.org/api/current/freestyle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# freestyle-python

Goal: line behaviour the Parameter Editor cannot express, or automated line-set setup across many files.

## Python Scripting mode (style modules)

View Layer Properties → Freestyle → *Control Mode: Python Scripting*. Style modules are stored in the blend-file as text data-blocks; load an external file in the Text Editor first, then pick it in the style module stack. Input is a view map (detected feature edges), output is stylized strokes.

```python
from freestyle.types import Operators
from freestyle.predicates import QuantitativeInvisibilityUP1D, NotUP1D, TrueUP1D
from freestyle.chainingiterators import ChainSilhouetteIterator
from freestyle.shaders import ConstantThicknessShader, ConstantColorShader, SamplingShader

Operators.select(QuantitativeInvisibilityUP1D(0))                           # visible edges
Operators.bidirectional_chain(ChainSilhouetteIterator(), NotUP1D(QuantitativeInvisibilityUP1D(0)))
shaders = [SamplingShader(5.0), ConstantThicknessShader(3), ConstantColorShader(0.1, 0.1, 0.1, 1.0)]
Operators.create(TrueUP1D(), shaders)
```

Pipeline of five operators: selection `Operators.select()`, chaining `Operators.chain()` / `Operators.bidirectional_chain()`, splitting `Operators.sequential_split()` / `Operators.recursive_split()`, sorting `Operators.sort()`, and stroke creation `Operators.create()` (always last, takes a predicate and a list of shaders). Blender ships sample style modules to start from.

Custom shaders subclass `freestyle.types.StrokeShader` and overload `shade()`. See the Freestyle Python API reference for the predicate, function, iterator and shader classes.

## Reading Parameter Editor settings (bpy)

```python
import bpy
fs = bpy.context.view_layer.freestyle_settings   # mode, crease_angle, as_render_pass, linesets
for ls in fs.linesets:
    ls.select_by_visibility = True
    ls.visibility = 'VISIBLE'                     # items include VISIBLE, HIDDEN, RANGE
    ls.select_silhouette = True
    ls.select_border = True
    ls.select_crease = False
    ls.linestyle.thickness = 2.5
    ls.linestyle.thickness_modifiers.new("Taper", 'ALONG_STROKE')
```

`FreestyleSettings.mode` selects Parameter Editor or Python Scripting; the property names above are listed in the Python API.

## Gotchas

- The Parameter Editor line sets are not used while the view layer is in Python Scripting mode (the control mode is either/or).

## Verify

Render with the module enabled and compare the strokes with the script.

## Checked

2026-10-27 against the Blender 5.2 manual (Freestyle Python Scripting page) and the current Python API (FreestyleSettings, FreestyleLineSet, FreestyleLineStyle, LineStyleThicknessModifiers.new(name, type), freestyle.types.StrokeShader). Confirmed the five operators, the sample code from the manual and the property names. Removed the unconfirmed install folder for sample styles, the `linesets.new` call, the `linestyle.color` line, error-console behaviour and per-frame performance remarks.
Method: documentation only; no commands were run.
