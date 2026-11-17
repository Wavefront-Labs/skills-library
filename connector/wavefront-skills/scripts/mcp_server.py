#!/usr/bin/env python3
"""MCP server (stdio, no dependencies) exposing the library's drill-in interface to any MCP-capable agent.

    claude mcp add wavefront-skills -- python /path/to/mcp_server.py        # Claude Code
    (other clients: a stdio server entry running this script)

Environment: WAVEFRONT_SKILLS_LOCAL = path to a library checkout (required); WAVEFRONT_SKILLS_EMB optional, for
semantic search (needs fastembed + numpy in the python that runs this). Tools: library_route, library_card,
library_get, library_expand, library_browse, library_report. The tool descriptions are the agent's whole manual,
so they stay short.
"""
import json, os, sys

LOCAL = os.environ.get("WAVEFRONT_SKILLS_LOCAL", "")
sys.path.insert(0, os.path.join(LOCAL, "tools"))

TOOLS = [
    {"name": "library_route", "description": "Before researching or improvising a professional task, ask the library which methods or skills cover it. Returns up to 5 ranked candidates (id, kind, status, score, description) or an empty list when nothing is close enough (then carry on without it).",
     "inputSchema": {"type": "object", "properties": {"task": {"type": "string", "description": "One plain sentence naming the job and the tools involved. No secrets, code or file paths."},
                                                     "context": {"type": "string", "description": "Optional comma-separated tools or platforms already known, e.g. kubernetes,argocd"}}, "required": ["task"]}},
    {"name": "library_card", "description": "A few-hundred-token extract of one skill: goal, gotchas, verify steps, sources. Use before get to decide if the full skill is worth reading.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}},
    {"name": "library_get", "description": "The full skill or method body. Fetch at most two per task, when you are about to use them.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}},
    {"name": "library_expand", "description": "Neighbours of a skill: the skills a method uses, the methods that use a skill, siblings in the same product.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}},
    {"name": "library_browse", "description": "Walk the taxonomy when route finds nothing: '' lists categories, 'category' its fields, 'category.field' its products, 'category.field.product' its skills.",
     "inputSchema": {"type": "object", "properties": {"node": {"type": "string"}, "offset": {"type": "integer"}}}},
    {"name": "library_report", "description": "Say how it went so the library improves: outcome is used | not_useful | wrong | gap (for gap pass the task you could not find coverage for). Stored locally.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}, "outcome": {"type": "string", "enum": ["used", "not_useful", "wrong", "gap"]},
                                                     "task": {"type": "string"}, "note": {"type": "string"}}, "required": ["outcome"]}},
]


def call(lib, name, a):
    if name == "library_route":
        return {"results": lib.route(a["task"], a.get("context"), 5)}
    if name == "library_card":
        return lib.card(a["id"]) or {"error": "no such skill"}
    if name == "library_get":
        g = lib.get(a["id"])
        return g if g else {"error": "no such skill"}
    if name == "library_expand":
        return lib.expand(a["id"]) or {"error": "no such skill"}
    if name == "library_browse":
        return lib.browse(a.get("node", ""), offset=int(a.get("offset", 0)))
    if name == "library_report":
        return lib.report(a.get("id", ""), a["outcome"], a.get("task", ""), a.get("note", ""))
    raise KeyError(name)


def main():
    lib = None
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        mid, method = msg.get("id"), msg.get("method", "")
        if mid is None:                                    # notification: no reply
            continue
        try:
            if method == "initialize":
                res = {"protocolVersion": (msg.get("params") or {}).get("protocolVersion", "2025-06-18"), "capabilities": {"tools": {}},
                       "serverInfo": {"name": "wavefront-skills", "version": "0.3.0"}}
            elif method == "tools/list":
                res = {"tools": TOOLS}
            elif method == "tools/call":
                if lib is None:
                    import librarian
                    lib = librarian.Library(LOCAL)
                p = msg["params"]
                try:
                    out = call(lib, p["name"], p.get("arguments") or {})
                    res = {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}]}
                except Exception as e:
                    res = {"content": [{"type": "text", "text": f"error: {e}"}], "isError": True}
            elif method == "ping":
                res = {}
            else:
                sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"unknown method {method}"}}) + "\n")
                sys.stdout.flush(); continue
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "result": res}) + "\n")
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": str(e)}}) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
