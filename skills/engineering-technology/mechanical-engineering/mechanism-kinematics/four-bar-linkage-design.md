---
id: engineering-technology.mechanical-engineering.mechanism-kinematics.four-bar-linkage-design
name: four-bar-linkage-design
category: engineering-technology
field: mechanical-engineering
product: mechanism-kinematics
tags: [four-bar-linkage, linkage-design, mechanism-design, kinematics, kinematic-synthesis, grashof, gruebler, kutzbach, degrees-of-freedom, mobility, transmission-angle, toggle-position, crank-rocker, freudenstein, position-analysis, velocity-analysis, vector-loop, matlab, coupler-curve, mechanical-advantage]
level: practitioner
status: gated
description: "Design and analyse a four-bar linkage: mobility, Grashof check, position/velocity solution, transmission angle limits and toggle positions, with MATLAB code."
sources: ["Norton, Design of Machinery (McGraw-Hill)", "Uicker, Pennock and Shigley, Theory of Machines and Mechanisms (Oxford University Press)", "Erdman and Sandor, Mechanism Design: Analysis and Synthesis (Prentice Hall)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Four-bar linkage design — from mobility to a full-cycle check

**Goal:** choose link lengths a (input crank), b (coupler), c (output rocker), d (ground)
that give the required motion, can actually be driven through the full range, and keep a
healthy transmission angle everywhere.

## 1. Mobility first
Gruebler/Kutzbach for planar mechanisms: `M = 3(n - 1) - 2 J1 - J2`, with n links
including ground, J1 full joints (pins, sliders), J2 half joints (cam/roll-slide).
Four-bar: n = 4, J1 = 4 gives M = 1. The formula ignores special geometry (parallel
links), so a result of 0 can still move and 1 can still lock — confirm by simulation.

## 2. Grashof condition — will the crank rotate fully?
Let s = shortest, l = longest, p, q the others.
- `s + l < p + q`: Grashof. Shortest link as crank (adjacent to ground) -> **crank-rocker**;
  shortest as ground -> double-crank (drag link); shortest as coupler -> double-rocker.
- `s + l > p + q`: non-Grashof, all triple-rockers; no link rotates fully.
- `s + l = p + q`: change-point; passes through a flat configuration where the output
  can flip branch. Avoid unless you add a guide.

A motor-driven crank needs Grashof with the crank as the shortest link.

## 3. Synthesis routes
- **Two-position rocker** (crank-rocker with given rocker swing): classic graphical
  construction; quick-return if the two crank positions are not 180 degrees apart.
  Time ratio = alpha/beta of the crank angles for the two strokes.
- **Function generation** (theta4 = f(theta2) at 3 precision points): Freudenstein's
  equation `K1 cos(t4) - K2 cos(t2) + K3 = cos(t2 - t4)` with `K1 = d/a`, `K2 = d/c`,
  `K3 = (a^2 - b^2 + c^2 + d^2)/(2 a c)` — three points give three linear equations in
  K1, K2, K3. Space precision points with Chebyshev spacing to minimise structural error.
- **Path / motion generation** (coupler point through points or poses): dyad synthesis
  or numeric optimisation. Expect to iterate; precision-point solutions often fail
  Grashof or branch checks and need rejecting.

## 4. Position and velocity over the full cycle (MATLAB)
Vector loop `a e^{i t2} + b e^{i t3} - c e^{i t4} - d = 0`, ground along +x.

```matlab
a=40; b=120; c=80; d=100; w2=10;              % mm, rad/s
K1=d/a; K2=d/c; K3=(a^2-b^2+c^2+d^2)/(2*a*c);
t2=linspace(0,2*pi,361);
A=cos(t2)-K1-K2*cos(t2)+K3; B=-2*sin(t2); C=K1-(K2+1)*cos(t2)+K3;
disc=B.^2-4*A.*C;                              % <0 => assembly impossible at that t2
t4=2*atan2(-B-sqrt(disc),2*A);                 % '-' = open branch, '+' = crossed
t3=angle(d+c*exp(1i*t4)-a*exp(1i*t2));
w3=a*w2.*sin(t4-t2)./(b*sin(t3-t4));
w4=a*w2.*sin(t2-t3)./(c*sin(t4-t3));
mu=abs(rad2deg(wrapToPi(t3-t4)));  mu=min(mu,180-mu);   % transmission angle 0..90
assert(max(abs(a*exp(1i*t2)+b*exp(1i*t3)-c*exp(1i*t4)-d))<1e-9)
fprintf('min transmission angle %.1f deg\n', min(mu));
```

The script was re-implemented line by line in NumPy and run: closure error 6e-14 on both branches, `w4` matches a finite-difference derivative to 0.002 rad/s, `disc` stays positive (min 7.1), and the Freudenstein equation is satisfied at a test point. This example is Grashof (40 + 120 < 80 + 100) but its minimum transmission angle is 26.4 degrees, at crank angle 0 (crank collinear with ground, as stated in section 5), so it demonstrates the code and would FAIL the 40-degree rule below.

(`wrapToPi` is from the Mapping Toolbox; replace with `mod(x+pi,2*pi)-pi` if absent.)
The closed form and velocity expressions follow Norton's notation; verify the closure
assertion and a finite-difference check of `w4` when you adapt it.

## 5. Transmission angle and toggles
- Transmission angle mu = angle between coupler and rocker. Keep **mu >= 40 degrees**
  (45 preferred; common textbook guidance (gated: unconfirmed, source is paywalled or blocked)) over the whole cycle; below that, friction and small errors cause
  jamming and huge pin forces. Minimum mu for a crank-rocker occurs when the crank is
  collinear with the ground link.
- **Toggle** (crank and coupler collinear): output is at a limit, output velocity is
  zero and mechanical advantage tends to infinity — useful for clamps, dangerous as an
  unintended dead point when the rocker is the driver.
- `disc < 0` anywhere in the intended range means the linkage cannot assemble there
  (non-Grashof limit).

## 6. Forces and practical layout
Mechanical advantage is proportional to `sin(mu)/sin(nu)` (nu = angle between crank and
coupler) times link ratios. After kinematics, run a kinetostatic analysis with link
masses at speed, then size pins for bearing pressure and links for buckling. Check link
clearance in 3D (links in different planes), and whether stacking/offsets create
twisting moments.

## Verify
- [ ] Mobility M = 1 and Grashof type matches the intended driver.
- [ ] Loop closure error < 1e-9 at every crank angle; velocity matches a finite difference.
- [ ] Minimum transmission angle >= 40 degrees over the working range.
- [ ] No unintended toggle/branch change; `disc >= 0` throughout.
- [ ] Precision points (or swing angle/time ratio) reproduced by the simulation.
