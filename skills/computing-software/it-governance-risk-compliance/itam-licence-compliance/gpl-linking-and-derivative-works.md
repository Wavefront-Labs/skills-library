---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.gpl-linking-and-derivative-works
name: gpl-linking-and-derivative-works
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [gpl-linking-and-derivative-works, gpl-obligations-and-faq, static-linking, dynamic-linking, derivative-work, plugins, separate-process, system-library-exception, aggregation, itam-licence-compliance]
level: advanced
status: docs-checked
description: "Analyse static and dynamic linking, plugins, separate processes and APIs to judge whether a combination is one GPL work."
sources:
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linking, plugins and derivative works under the GPL

Goal: reasoned linking decisions.

FSF position (GPL FAQ):
- Linking a GPL-covered work statically or dynamically with other modules makes a combined work, and the GPL covers the whole combination.
- Modules in the same executable are definitely one program; modules designed to run linked in a shared address space almost surely are.
- Pipes, sockets and command-line arguments are mechanisms normally used between separate programs, so modules using them are normally separate. Intimate exchange of complex internal data structures can still make them one program.
- Plugins depend on how the host invokes them. Simple fork and exec without intimate communication gives separate programs. Dynamic linking with shared data structures and function calls between them gives a single combined program. Dynamic linking limited to calling the plugin's main function and waiting for it is a borderline case. Shared memory with complex data structures is about equivalent to dynamic linking.
- If the host and plugins are one program, the plugin must be GPL or GPL-compatible and distributed with source in a GPL-compliant way. If they are separate, the host's licence places no requirement on the plugin and vice versa.
- Both GPLv2 and GPLv3 have a system library exception: libraries that qualify as system libraries are outside the source-distribution requirement even in a linked executable. GPLv3 defines System Libraries in section 1.
- The GCC Runtime Library Exception lets people distribute programs compiled with GCC under terms of their choice even when parts of libgcc, libstdc++ and similar libraries are included in the executable.
- An aggregate (separate programs distributed together) is permitted even when the other licences are nonfree, provided the aggregate licence does not stop users exercising each programme's own rights.

Method:
- Document the interaction mechanism per component (link, plugin, IPC, exec) and what data crosses it.
- For high risk, choose a separate process boundary, replace the library, or get a commercial licence or a copyright-holder exception.
- Seek legal advice: the FAQ says the line between one program and two is a legal question that judges will ultimately decide.

Gotchas:
- Containers change nothing: the single-work versus aggregate analysis is the same inside a container as outside.
- A nonfree driver meant to link with the Linux kernel (GPLv2) is, per the FAQ, a violation because it makes a larger combined work, even though the user assembles the pieces.
- Only the copyright holders can grant an exception for a controlled interface.

Verify: interaction table approved.

## Checked

2026-11-08. Confirmed against the GNU GPL FAQ (gpl-faq.html) entries on static versus dynamic linking, plugins, mere aggregation, containers, the system library exception, the GCC Runtime Library Exception, the nonfree Linux driver question and the controlled-interface exception. Removed or corrected: "plugins usually form one work" (the FAQ says it depends on invocation), "kernel module exceptions are specific to Linux (GPL-only symbols)" (not on the page), "containers are normally aggregation" (the FAQ says containers have no effect), and "courts have not settled the question uniformly" (reworded to the FAQ's statement).
Method: documentation only; no commands were run.
