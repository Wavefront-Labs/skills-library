---
id: engineering-technology.electronics-engineering.fpga-design.timing-constraints-and-closure
name: timing-constraints-and-closure
category: engineering-technology
field: electronics-engineering
product: fpga-design
tags: [fpga-design, fpga, timing-closure, static-timing-analysis, sta, xdc, sdc, vivado, quartus, create-clock, generated-clock, set-input-delay, set-output-delay, clock-groups, false-path, max-delay, cdc, clock-domain-crossing, wns, tns, setup-slack, hold-slack, pipelining, verilog, vhdl]
level: advanced
status: draft
description: "Write FPGA timing constraints and close timing: create_clock, generated clocks, I/O delays, CDC false paths, reading WNS/TNS reports in Vivado or Quartus."
sources:
  - "AMD/Xilinx UG903, Vivado Design Suite User Guide: Using Constraints"
  - "AMD/Xilinx UG906, Vivado Design Suite User Guide: Design Analysis and Closure Techniques"
  - "AMD/Xilinx UG949, UltraFast Design Methodology Guide"
  - "Intel Quartus Prime Timing Analyzer documentation"
  - "Cummings, Clock Domain Crossing (CDC) Design & Verification Techniques Using SystemVerilog (SNUG 2008)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# FPGA timing constraints and closure — constrain everything, then believe the report

**Goal:** a complete, correct constraint set (every clock, every I/O, every crossing
intentionally described) and an implemented design with **WNS ≥ 0 and WHS ≥ 0** that
you can trust because nothing is left unconstrained or falsely excluded.

## 1. Clocks (XDC/SDC syntax; Vivado and Quartus share most of it)
```tcl
create_clock -name sys_clk -period 10.000 [get_ports sys_clk_p]   ;# 100 MHz
create_clock -name rx_clk  -period 8.000  [get_ports rx_clk]      ;# 125 MHz from PHY
```
- Constrain clocks **at the input port**. In Vivado, MMCM/PLL output clocks are
  derived automatically from the input constraint; in Quartus use
  `derive_pll_clocks` (and `derive_clock_uncertainty`) in the SDC.
- Clocks you make in fabric (counters, dividers — avoid if you can; use clock enables)
  need `create_generated_clock -source ... -divide_by N` on the register output.
- Run `report_clocks` and confirm every clock exists with the right period.

## 2. I/O delays
Describe what happens *outside* the FPGA, relative to a clock:
```tcl
# Input: external device launches data on rx_clk; data valid window from its datasheet
set_input_delay -clock rx_clk -max 5.0 [get_ports {rxd[*]}]
set_input_delay -clock rx_clk -min 1.0 [get_ports {rxd[*]}]
# Output: external device needs tsu=2 ns, th=0.5 ns (plus board delay)
set_output_delay -clock tx_clk -max 2.0  [get_ports {txd[*]}]
set_output_delay -clock tx_clk -min -0.5 [get_ports {txd[*]}]
```
- Input -max = external Tco,max + board delay,max; -min = Tco,min + board delay,min.
- Output -max = external tsu + board delay; -min = −(external th) + board delay,min.
- Use IOB registers (`set_property IOB TRUE [get_cells ...]` in Vivado) or I/O
  delay primitives so I/O timing is fixed and repeatable across builds.
- For source-synchronous DDR inputs you need `-clock_fall -add_delay` pairs; follow
  the vendor template (Vivado has XDC templates under Tools › Language Templates).

## 3. Clock-domain crossings — describe them honestly
- Truly asynchronous clocks: `set_clock_groups -asynchronous -group [get_clocks
  sys_clk] -group [get_clocks rx_clk]`. Only do this when **every** crossing between
  them goes through a proper synchroniser (2-FF for single bits, gray-coded pointers
  in async FIFOs, handshakes for buses).
- For gray-coded or handshake buses prefer `set_max_delay -datapath_only <period of
  destination>` on those paths over a blanket false path — it bounds skew between bits.
- Mark synchroniser flops (`ASYNC_REG TRUE` in Vivado) so they are placed together
  and treated correctly by analysis.
- Check with `report_clock_interaction` and `report_cdc` (Vivado) — any "unsafe"
  or "timed (unsafe)" crossing needs a decision.

## 4. Read the report
`report_timing_summary` (Vivado) / Timing Analyzer summary (Quartus):
- **WNS** worst negative setup slack, **TNS** total; **WHS/THS** for hold.
- First look at **"check_timing"**: unconstrained endpoints, no-clock registers,
  missing I/O delays. Zero is the only acceptable count — an unconstrained path
  always "passes".
- Then the worst path: logic levels vs routing delay. Mostly routing → placement/
  congestion/fan-out problem; mostly logic → RTL depth problem.

## 5. Closing timing (in order of payoff)
1. **Fix the RTL**: pipeline long combinational chains, register module boundaries,
   use DSP/BRAM output registers (they're free and big wins), avoid wide muxes.
2. **High fan-out**: replicate registers or `max_fanout` attributes; for resets prefer
   synchronous reset only where needed (many vendors recommend minimising resets).
3. **Tool effort**: implementation strategies (e.g. Vivado's Performance_* strategies),
   `phys_opt_design` post-route, retiming options. Expect a few percent, not miracles.
4. **Floorplan** with Pblocks/LogicLock only when you understand why placement is bad.
5. Hold violations after route are normally fixed by the router; large hold violations
   usually mean a clocking mistake (gated clock, wrong I/O constraint).

## Gotchas
- `set_false_path` to silence a red path is the most common way to ship a bug.
- Gated or logic-generated clocks create skew the tools can't fix — use clock enables
  or BUFGCE-type primitives.
- Constraints that don't match any object are silently dropped in some flows; check
  the critical warnings for "no objects found".
- Timing met at one seed/strategy and failing at another means you are at the edge;
  build in margin (~5–10 % of the period) for designs that will keep growing.

## Verify
- [ ] `check_timing` (or equivalent) shows zero unconstrained endpoints and no missing I/O delays.
- [ ] Every clock appears in `report_clocks` with the correct period and source.
- [ ] Every clock-domain crossing has a synchroniser and a deliberate constraint.
- [ ] WNS ≥ 0 and WHS ≥ 0 after route, at the speed grade you will ship.
- [ ] No unexplained critical warnings about dropped constraints.
- [ ] I/O timing validated on hardware at temperature extremes if margins are thin.
