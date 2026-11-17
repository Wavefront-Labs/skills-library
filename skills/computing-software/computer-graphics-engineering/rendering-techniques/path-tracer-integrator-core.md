---
id: computing-software.computer-graphics-engineering.rendering-techniques.path-tracer-integrator-core
name: path-tracer-integrator-core
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, ray-tracing, path-tracing-integrator, path-tracing, next-event-estimation, russian-roulette, monte-carlo, mis]
level: advanced
status: docs-checked
description: "Write a path tracing integrator the pbrt-v4 way: throughput tracking, next-event estimation with MIS power heuristic, specular bounces and Russian roulette."
sources: ["https://pbr-book.org/4ed/Light_Transport_I_Surface_Reflection/A_Better_Path_Tracer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a path tracer integrator

Structure follows pbrt-v4's `PathIntegrator::Li()` and `SampleLd()`.

## 1. Core loop
```cpp
Spectrum Li(Ray ray, Sampler& s) {
    Spectrum L(0), beta(1);              // radiance, path throughput
    int depth = 0; float p_b = 0, etaScale = 1; bool specularBounce = false;
    LightCtx prev;                       // context of the previous scattering vertex
    while (true) {
        auto si = intersect(ray);
        if (!si) {                                          // escaped: infinite lights
            for (auto& light : infiniteLights) {
                Spectrum Le = light.Le(ray);
                if (depth == 0 || specularBounce) L += beta * Le;
                else {
                    float p_l = lightSampler.PMF(prev, light) * light.PDF_Li(prev, ray.d);
                    L += beta * powerHeuristic(1, p_b, 1, p_l) * Le;
                }
            }
            break;
        }
        Spectrum Le = si->Le(-ray.d);                       // emission from a surface hit
        if (Le) {
            if (depth == 0 || specularBounce) L += beta * Le;
            else {
                float p_l = lightSampler.PMF(prev, si->areaLight) * si->areaLight.PDF_Li(prev, ray.d);
                L += beta * powerHeuristic(1, p_b, 1, p_l) * Le;
            }
        }
        BSDF bsdf = si->getBSDF();
        if (!bsdf) { ray = si->skipIntersection(ray); continue; }   // medium boundary
        if (depth++ == maxDepth) break;
        if (isNonSpecular(bsdf.flags()))
            L += beta * sampleLd(*si, bsdf, s);             // next-event estimation
        auto bs = bsdf.sample_f(wo, s.get1D(), s.get2D());
        if (!bs) break;
        beta *= bs->f * absDot(bs->wi, si->shading.n) / bs->pdf;
        p_b = bs->pdfIsProportional ? bsdf.pdf(wo, bs->wi) : bs->pdf;
        specularBounce = bs->isSpecular();
        if (bs->isTransmission()) etaScale *= sqr(bs->eta);
        prev = *si;
        ray = si->spawnRay(ray, bsdf, bs->wi, bs->flags, bs->eta);
        Spectrum rrBeta = beta * etaScale;                  // Russian roulette
        if (rrBeta.maxComponent() < 1 && depth > 1) {
            float q = std::max(0.f, 1 - rrBeta.maxComponent());
            if (s.get1D() < q) break;
            beta /= 1 - q;
        }
    }
    return L;
}
```

## 2. Next-event estimation (SampleLd)
- Choose a light with the light sampler (probability `sampledLight.p`), then sample a point on it
  (`SampleLi`). Return zero if the sample has no radiance or `pdf == 0`.
- Evaluate `f = bsdf.f(wo, wi) * absDot(wi, shadingNormal)`; return zero if `f` is zero or the
  shadow ray is occluded.
- `p_l = sampledLight.p * ls.pdf`. For a delta light return `ls.L * f / p_l` (no MIS partner).
  Otherwise `p_b = bsdf.pdf(wo, wi)`, `w_l = powerHeuristic(1, p_l, 1, p_b)` and return
  `w_l * ls.L * f / p_l`.
- For a purely reflective or purely transmissive BSDF, pbrt nudges the light-sampling position to
  the correct side of the surface using the ray-origin offset.
- NEE runs only at non-specular vertices; a specular bounce cannot be light-sampled, which is why
  emission found after a specular bounce (or at depth 0) is added with no MIS weight.

## 3. Notes
- Emission found by BSDF sampling is weighted with the power heuristic against the same light's
  sampling pdf (`p_b` against `p_l`), matching the NEE weight above, so each emission is counted
  once.
- Russian roulette uses throughput times `etaScale` (accumulated squared refraction ratios), only
  once `depth > 1`, and divides surviving throughput by `1 - q`.
- pbrt-v4 also offers path regularisation (`bsdf.Regularize()` after the first non-specular
  bounce) as an option; it is off by default.

## Gotchas
- Forgetting the cosine term or the 1/pdf factor gives wrong brightness, not noise.
- Double counting emission when NEE is on and the MIS weights are missing (bright lights).

## Verify
- [ ] NEE on and off converge to the same mean.
- [ ] A white diffuse furnace scene stays within noise of the expected value.

## Checked
2026-11-09. Read: pbr-book 4th edition, "A Better Path Tracer" (PathIntegrator::Li, SampleLd,
MIS weights for escaped rays and area lights, delta-light case, Russian roulette with rrBeta and
etaScale, regularisation option). Corrected: the skill's Russian roulette (depth > 3, floor 0.05)
and light-pdf form did not match pbrt; delta lights were not handled in NEE. Removed: Sobol/Owen
sampler advice, light BVH advice, epsilon ray-offset advice, EXR accumulation, Mitsuba/PBRT
comparison and the 1/sqrt(spp) claim, and the Veach thesis and Rest of Your Life sources (not
read).
Method: docs-checked 2026-11-09 against the pbr-book 4ed A Better Path Tracer chapter.
