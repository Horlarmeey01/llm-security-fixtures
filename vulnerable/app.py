"""VULNERABLE: assistant that summarizes a document. (OWASP LLM06: Excessive Agency)"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from common import mock_llm

def run_tool(world, tool, args):
    if tool == "read_file":
        return world["files"].get(args[0], "")
    if tool == "send_email":
        body = re.sub(r"\{\{(.+?)\}\}", lambda m: world["files"].get(m.group(1), ""), args[1])
        world["outbox"].append((args[0], body))
    if tool == "delete_file":
        world["files"].pop(args[0], None)

def summarize(world, path):
    doc = run_tool(world, "read_file", [path])
    for tool, args in mock_llm("summarize", doc):   # executes whatever the model asks for
        run_tool(world, tool, args)
    return doc[:40] + "..."
