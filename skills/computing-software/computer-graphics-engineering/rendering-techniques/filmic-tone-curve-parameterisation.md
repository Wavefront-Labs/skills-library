---
id: computing-software.computer-graphics-engineering.rendering-techniques.filmic-tone-curve-parameterisation
name: filmic-tone-curve-parameterisation
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, hdr-tonemapping, filmic-curve, tone-curve, hable-filmic, uncharted2, white-point, tonemapping]
level: advanced
status: docs-checked
description: "Parameterise filmic tone curves: Hable's Uncharted 2 operator and the piecewise power curve with toe, linear and shoulder segments, plus gamma convolution."
sources: ["https://filmicworlds.com/blog/filmic-tonemapping-with-piecewise-power-curves/", "https://filmicworlds.com/blog/filmic-tonemapping-operators/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filmic curve parameterisation

## 1. Shape
A filmic curve simulates the tone curve of film with a shoulder and a toe:
- **Toe**: gives crisper blacks.
- **Linear section**: should look relatively unchanged.
- **Shoulder**: a softer transition into overexposed highlights instead of clipping.

## 2. Hable's Uncharted 2 operator
```glsl
vec3 hable(vec3 x) {
    const float A = 0.15, B = 0.50, C = 0.10, D = 0.20, E = 0.02, F = 0.30;
    return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F;
}
vec3 tonemap(vec3 c) { const float W = 11.2; return hable(c * exposureBias) / hable(vec3(W)); }
```
The author's post uses these defaults with an exposure bias of 2.0 applied inside the tonemap
and scales by 1 / hable(W). Hable himself lists its limits: the controls are "all or nothing"
(you cannot make a plain linear curve), and pushing the parameters gives odd behaviour.

## 3. Hable piecewise power curves (2017)
The curve is three segments (toe, linear, shoulder) joined from four points: the origin, the
start (x0, y0) and end (x1, y1) of the linear section, and a white point W at y = 1. Each segment
has the form:

    y = scaleY * e^(lnA + B * ln((x - offsetX) * scaleX)) + offsetY

Using lnA instead of A avoids floating-point range problems as B grows. The separate scaleX and
scaleY flip a segment left-right or upside down. The linear section is a segment with B = 1. The
toe and shoulder are derived so they match the position and slope of the linear section's
end points. Evaluation picks the segment by comparing x with x0 and x1:
```glsl
struct Segment { float offsetX, offsetY, scaleX, scaleY, lnA, B; };   // filled on the CPU
float evalSegment(float x, Segment s) {
    float x0 = (x - s.offsetX) * s.scaleX;
    float y0 = exp(s.lnA + s.B * log(x0));
    return y0 * s.scaleY + s.offsetY;
}
```
The direct parameters are x0, y0, x1, y1, W, overshootX, overshootY and gamma. Artists get a
second layer of user parameters from which the direct ones are derived on the CPU:
- toeStrength [0-1] and toeLength [0-1]
- shoulderStrength [0-1], shoulderLength (in F stops) and shoulderAngle [0-1]
- gamma

The user-parameter derivation locks the slope of the linear section at 1.0; use an exposure
adjustment before the curve instead of a separate slope control. Hable recommends leaving
toeLength constant and adjusting only toeStrength. His reference code (CC0) is at
github.com/johnhable/fw-public.

## 4. Convolving output gamma
The curve takes linear input and returns linear output. The post shows how to fold a display
gamma into the curve parameters via the chain rule. It is not a perfect approximation, and
there is no reason to do it if you bake to a LUT anyway.

## Gotchas
- A curve that reaches 1.0 only just before its white point can look as if it hits white earlier,
  because the last values map to the final 8-bit steps after gamma. The post's example hits 0.996
  after gamma at a linear 3.25 even though the curve nominally reaches white near 4.0.
- Parameters can be lerped to blend between curves in different areas.

## Verify
- [ ] Plot the curve and check continuity of value and slope at x0 and x1.
- [ ] Highlights roll off without clipping before the white point.

## Checked

Method: docs-checked 2026-11-09 against the two filmicworlds.com posts (piecewise power curves read in full for the sections cited, operators post read for the Uncharted 2 constants). Dropped unconfirmed white-point multiples, mid-grey anchor, hue-preservation advice, modern operator list and LUT sizes.
