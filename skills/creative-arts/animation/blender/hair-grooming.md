---
id: creative-arts.animation.blender.hair-grooming
name: hair-grooming
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-cards, clumps, curves, geometry-nodes, stylized, toon, cel, silhouette, riggable, solidify, outline, grooming, npr]
level: advanced
status: docs-checked
description: "Stylized cel hair in Blender as modeled cards, clumps and curve geometry that outlines cleanly and stays riggable, not photoreal particle hair."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/curves/properties/geometry.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/shading.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hair-grooming

Style and number guidance in this skill (card subdivisions, thickness, clump counts, colour counts, per-lock bone counts) is practice for a cel look, not documented by the Blender manual; only tool names, menu paths and properties were checked against it.

Goal: build hair that reads as *shapes* — bold clumps and chunks with a clean silhouette — for a cel look, where the inverted-hull outline must trace the hair as crisp lines and the 3-tone ramp fills it with flat bands. This is modeled/curve hair, deliberately **not** photoreal strand-particle hair. Dynamics (wind, swing, sim) are a separate concern; this skill is the static, riggable groom. Shading of the hair is owned by `creative-arts.animation.blender.cel-shading`; the head it sits on comes from `creative-arts.animation.blender.character-modeling`.

## Why not particle/strand hair for cel

Blender's strand hair (the new Curves object with interpolated children, or legacy particles) makes thousands of fine strands. Under the cel pipeline this fails three ways:

1. The **inverted-hull outline** would try to outline every strand → a black fuzzy mess, or you disable it on hair and lose the toon line entirely.
2. Shader-to-RGB + 3-tone ramp on fine strands gives noisy, aliased, crawling bands.
3. Thousands of strands don't **rig or pose** predictably for a reused locked asset.

Cel hair is therefore **geometry you control**: a small number of readable chunks, each a surface the outline can wrap and the ramp can fill with 2–3 flat bands. Think Disney/feature stylization — hair as sculpted masses — rather than fur.

## Three construction methods (choose per character)

**1. Hair cards (mesh ribbons / planes).**
Flat or lightly curved quad strips, grouped into overlapping clumps.

- Build one card: a plane, subdivided lengthwise 4–6 cuts so it bends smoothly, tapered to a point at the tip.
- Curve it over the skull with `Proportional Edit` or a lattice; duplicate and vary to build clumps, then clumps into the whole head.
- Give each card real thickness with a `Solidify` modifier (small, e.g. 2–4 mm) so the outline wraps a solid edge instead of a zero-thickness plane (a single-sided plane outlines as a thin sliver or flickers). Alternatively model the card as a thin closed slab from the start.
- Best for: anime-ish chunky hair, fringe, spikes, anything with crisp card silhouettes.

**2. Curve-based geometry (Bézier/NURBS with bevel).**
Draw the flow as curves, convert to tube/ribbon geometry.

- Add a `Curve`, draw the strand flow along the head. Set the curve's **Geometry > Bevel** to a small round or a custom profile (a flat ribbon profile for strands, a round profile for cords/braids), and **Taper Object** or the Bevel `Taper` to thin the tips.
- `Object > Shade Smooth` + `Object > Shade Auto Smooth` (adds a Smooth by Angle modifier pinned last); convert to mesh (`Object > Convert > Mesh`) when you need to edit topology or rig heavily.
- Best for: flowing locks, braids, ponytails, anything with long clean sweeps where you want to art-direct the *line*.

**3. Geometry Nodes instanced clumps (procedural, art-directed).**
A GN setup that instances a reusable clump mesh along guide curves or over the scalp.

- Groom guide curves (a handful, hand-placed) in the Curves object; in a GN modifier, `Instance on Points`/`Curve to Mesh` a stylized clump profile, with `Rotation`/`Scale` randomised slightly for variation.
- Keeps the groom editable (change the clump, whole head updates) and light — ideal for a **locked reused asset**: the clump mesh and guide curves are the editable source, the output is deterministic.
- `Curve to Mesh` with a flat/round profile curve gives ribbon or tube chunks directly; feed a `Set Curve Radius` driven by a taper for pointed tips.
- Best for: consistent, reusable, moderately complex grooms you want to tweak globally.

For this series, a common hybrid: **big hero shapes as hair cards / curve ribbons** (fringe, silhouette-defining locks) plus **GN clumps** for filler mass, all merged into a few outline-friendly chunks.

## Shaping the silhouette

Hair silhouette *is* the character read in cel — it's often more recognisable than the face. Rules:

- Design the **hero shapes first**: 3–6 big masses (fringe, side sweeps, back mass, a cowlick). Nail those in silhouette before any filler.
- Keep **clean, closed silhouettes** per clump — a tip that tapers to a crisp point, a clump edge that reads as one line. Avoid stray thin wisps; the outline either misses them (gaps) or outlines them into noise.
- **Overlap clumps in layers** (under-mass, mid, top/fringe) so the outline draws satisfying internal lines between layers, not a single blobby hull.
- Carve **negative space** deliberately — the gaps between locks are part of the shape; the outline will draw them.
- Check silhouette with a flat dark matcap orbit, same as a sculpt (ties to `creative-arts.animation.blender.organic-sculpting`).

## Keeping it outline-clean

- **Give every piece thickness** (Solidify or modelled slab). Zero-thickness planes make the inverted-hull outline flicker and punch through.
- **Consistent normals** (Edit Mode `Mesh > Normals > Recalculate Outside`, `Shift N`) on all hair geometry — a flipped card outlines black or drops its line (practice).
- **Weld and seal** each clump (`Mesh > Merge > By Distance`) so the hull is watertight per chunk.
- Decide the **outline treatment** with cel-shading: usually the hair shares the character's inverted-hull Solidify outline, so hair thickness and outline thickness must be compatible (hair slab thicker than the outline offset, or the line punches through).
- Keep **tip tapers wider than the outline width** — a tip thinner than the line thickness just becomes a dot.

## Keeping it riggable and consistent (locked asset)

A reused asset gets posed every shot, so the hair must deform predictably:

- **Parent/skin the hair to head and neck bones** so it follows the head rig (ties to `creative-arts.animation.blender.rigging`). For hero locks that should swing a little by hand (no sim), add **1–3 extra bones per lock** and weight the card/curve to them, so an animator can key the swing manually and consistently.
- Keep the **groom's source editable but the shot version stable**: for GN grooms, the guide curves + clump mesh are the source; apply/lock a deterministic output into the asset so it can't re-randomise or break a modifier socket when reopened in a later shot (same discipline as hard-surface locked assets).
- **Name the hair objects/bones consistently** (e.g. `hair_fringe`, `hair_pony`, `DEF-hair_lock_L`) so rigs and shots across the series refer to the same things.
- Keep **poly count low and chunked** — a few dozen clumps, not thousands of strands — so posing is light and the outline stays crisp.

## Shading hair chunks for cel

Hair under the 3-tone ramp wants a *directed* read, not flat colour:

- **Flat base + a ramp that bands along the clump length,** not just by light. A common trick: multiply the Shader-to-RGB cel result by a subtle dark-to-light gradient running root→tip (use a per-card UV V-coordinate, or a `Gradient Texture` mapped to object/clump space) so roots sit a band darker and tips catch highlight — the classic toon hair read. This is the one place hair benefits from a cheap UV (a single straight V per card; see `creative-arts.animation.blender.uv-unwrapping`).
- **Specular as a hard band, not a soft sheen:** add a second, brighter CONSTANT step in the ramp positioned where the top layer faces the key light, giving the crisp "anime highlight" stripe. Keep it on the top clump layer only or it reads muddy.
- **Hue-shift the shadow band** the same way the character shader does (see `creative-arts.animation.blender.cel-shading`) so hair shadow matches skin shadow and the character reads as one lit object.
- Use **1–3 flat colours max** per hair (base, shadow, highlight). More and the layered clumps turn noisy under the ramp.

Decide early whether the highlight is *modelled* (a separate thin clump the ramp lights) or *shaded* (the ramp step). Shaded is cheaper and more consistent across a reused asset; modelled gives a sharper art-directed stripe.

## Contrast with hair-simulation (separate skill)

Everything above is a **static, hand-art-directed, riggable** groom. Dynamics — physics swing, wind, collision, jiggle — belong to a separate hair-simulation skill (Blender cloth/hair physics, or a spring/jiggle rig). On this cel show, prefer **hand-keyed swing on a few lock bones** over sim: it's cheaper, consistent across a reused asset, and the outline stays clean because the geometry count never changes. Reach for real dynamics only when a shot genuinely needs it, and bake the result so the locked asset stays deterministic.

## Verify

A cel hair groom is finished when:

1. **Silhouette test:** flat dark matcap, orbit a full turn — the hair reads as the intended bold shapes at every angle, with crisp tapered tips and deliberate negative space, no stray wisps.
2. **Outline test:** render with the inverted-hull outline on — the hair shows clean continuous lines on its silhouette and between its layered clumps, with no black fuzz, no gaps at tips, and no line punching through a clump (that = thickness < outline offset or a flipped normal).
3. **Cel-fill test:** Shader-to-RGB 3-tone render — each clump fills with stable flat bands that don't crawl or shimmer as the camera moves.
4. **Deform test:** pose the head rig through its extremes (full head turn, big nod) — hair follows the head, hero locks swing only via their intended lock bones, nothing detaches, intersects badly, or breaks a modifier.
5. **Count check:** the groom is a manageable number of chunks (tens), not thousands of strands; `Statistics` confirms it's geometry you can pose, not fur.
6. **Normals clean:** the `Face Orientation` overlay (which shows face backsides in red) shows no red on the outside of any hair piece.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: curve Geometry panel Taper Object and Bevel; Object > Shade Smooth and Shade Auto Smooth (adds Smooth by Angle modifier, pinned last); Mesh > Normals > Recalculate Outside (Shift-N); Mesh > Merge > By Distance; Face Orientation overlay shows backsides in red; Geometry Nodes Instance on Points, Curve to Mesh node pages exist; Hair Node Groups bundled assets (Quick Effects docs). Removed: the "all blue" Face Orientation check (the manual documents only the red backside).
Method: documentation only; no commands were run.
