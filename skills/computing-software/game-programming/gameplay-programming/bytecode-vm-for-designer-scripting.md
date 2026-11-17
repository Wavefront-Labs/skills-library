---
id: computing-software.game-programming.gameplay-programming.bytecode-vm-for-designer-scripting
name: bytecode-vm-for-designer-scripting
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, bytecode-vm, bytecode, stack-machine, interpreter, scripting-language, modding, game-programming]
level: advanced
status: draft
description: "Build a sandboxed bytecode VM for designer/modder behaviour: stack instruction set, compiling from a language or node graph, limits, and when to embed Lua."
sources: ["https://gameprogrammingpatterns.com/bytecode.html", "https://craftinginterpreters.com/a-virtual-machine.html", "https://www.lua.org/manual/5.4/manual.html#4"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bytecode VM for designer scripting

**Goal:** behaviour defined as data (spells, card effects, mod content) that runs fast, cannot crash
or hack the game, and loads without recompiling (Nystrom, GPP "Bytecode").

## First, consider not building one
Embedding **Lua** (or Luau, Wren, AngelScript) gives a tested VM, debugger and docs. Build your own
only when you need a tiny, fully sandboxed, deterministic instruction set (e.g. card effects that
must run identically in lockstep) or a node-graph target.

## Stack machine core
```cpp
enum class Op : uint8_t { LIT, ADD, SUB, LT, JMP_IF_FALSE, GET_HEALTH, SET_HEALTH, PLAY_SOUND, END };
class VM {
    static constexpr int MAX_STACK = 128;
    int stack_[MAX_STACK]; int sp_ = 0;
    void push(int v) { if (sp_ >= MAX_STACK) throw VMError("stack overflow"); stack_[sp_++] = v; }
    int pop()        { if (sp_ <= 0) throw VMError("stack underflow"); return stack_[--sp_]; }
public:
    void run(const uint8_t* code, size_t len, Game& game, int budget = 10000) {
        for (size_t pc = 0; pc < len && budget-- > 0; ) {
            switch (Op(code[pc++])) {
            case Op::LIT:  push(read_i32(code, pc)); pc += 4; break;
            case Op::ADD:  { int b = pop(), a = pop(); push(a + b); } break;
            case Op::GET_HEALTH: push(game.health(pop())); break;
            case Op::SET_HEALTH: { int amt = pop(), who = pop(); game.setHealth(who, amt); } break;
            case Op::JMP_IF_FALSE: { int t = read_i32(code, pc); pc += 4; if (!pop()) pc = t; } break;
            case Op::END: return;
            default: throw VMError("bad opcode");
            }
        }
    }
};
```
Instructions are high-level game verbs (`GET_HEALTH`, `SPAWN`, `PLAY_SOUND`): the VM can only do
what you expose, which is the sandbox.

## Authoring front end
Designers should not write bytecode. Compile from a tiny text language (recursive-descent parser),
or from a node graph (post-order traversal emits operands then the op). Keep the compiler in tools;
ship bytecode.

## Safety
- Instruction **budget** per run (stops infinite loops), stack bounds, jump targets validated at load
  (inside code, on an instruction boundary), argument ranges clamped in the verbs.
- Version the bytecode format; reject unknown versions.
- Values: start with ints/floats; add a tagged `Value` union only when needed.

## Debugging
Emit a source map (bytecode offset -> source line/node), a disassembler, and a trace mode that logs
each op and the stack. Without these designers cannot fix their content.

## Verify
- [ ] Fuzz random bytes into the loader/VM: it rejects or terminates, never crashes.
- [ ] An infinite loop script stops at the budget with a clear error naming the asset.
- [ ] Same script, same inputs gives identical results on all platforms (if used for lockstep).
