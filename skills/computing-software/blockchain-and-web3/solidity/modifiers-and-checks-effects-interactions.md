---
id: computing-software.blockchain-and-web3.solidity.modifiers-and-checks-effects-interactions
name: modifiers-and-checks-effects-interactions
category: computing-software
field: blockchain-and-web3
product: solidity
tags: [sol-modifiers, checks-effects-interactions, modifier-placeholder]
level: practitioner
status: docs-checked
description: "Write modifiers with the _ placeholder and order checks, effects and interactions inside functions."
sources:
  - https://docs.soliditylang.org/en/latest/contracts.html#function-modifiers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modifiers
```solidity
modifier onlyOwner() { require(msg.sender == owner, "not owner"); _; }
function withdraw(uint256 a) external onlyOwner {
    // checks
    require(balance[msg.sender] >= a, "low");
    // effects
    balance[msg.sender] -= a;
    // interactions
    (bool ok,) = msg.sender.call{value: a}(""); require(ok);
}
```
- `_;` marks where the body of the modified function is inserted; code after it runs when the body finishes. `_` may appear several times, and the function returns the value of the final occurrence.
- An explicit `return` in a function body or modifier only leaves that body; control continues after the `_` in the enclosing modifier. A modifier can also choose not to run the body, in which case the return variables hold their default values.
- Several modifiers are listed whitespace-separated and evaluated in the order written. Modifiers cannot implicitly read or change the function's arguments and return values; pass them explicitly.
- Virtual modifiers (overridable) are deprecated and scheduled for removal.
- Order inside a function: checks, then state changes, then external calls. A called contract may call back into yours before the call returns, so update state first so your contract is not open to reentrancy.
- A modifier can implement a mutex (require the flag is clear, set it, run `_;`, clear it); the clear step still runs after a `return` in the body, so reentrant calls cannot enter the guarded function again.

## Verify
- [ ] A reentrancy test confirms the balance is already reduced when the external call occurs.

## Checked

Confirmed against Solidity docs contracts/function-modifiers.rst (placeholder semantics, multiple `_`, return behaviour, ordering, explicit argument passing, mutex example) and contracts/inheritance.rst (virtual modifiers deprecated), plus the external-call warning in control-structures.rst for state-before-calls ordering. Removed the unsupported "heavy modifier logic duplicates bytecode" advice.

Method: docs-checked 2026-11-09 against Solidity docs contracts/function-modifiers.rst, contracts/inheritance.rst and control-structures.rst (raw rst on GitHub).
