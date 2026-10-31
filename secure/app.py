"""SECURE: same assistant, with least privilege and human approval."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from common import mock_llm

TASK_TOOLS = {"summarize": {"read_file"}}          # allow-list per task
ALLOWED_PREFIX = "docs/"                            # no access outside docs/
audit_log = []

def run_tool(world, tool, args, approver=lambda t, a: False):
    if tool == "read_file":
        if not args[0].startswith(ALLOWED_PREFIX) or ".." in args[0]:
            raise PermissionError("path outside allowed area")
        return world["files"].get(args[0], "")
    if tool in ("send_email", "delete_file"):       # high-risk: needs human approval
        if not approver(tool, args):
            raise PermissionError(f"{tool} requires approval")
        return None
    raise PermissionError("unknown tool")

def summarize(world, path, approver=lambda t, a: False):
    doc = run_tool(world, "read_file", [path])
    for tool, args in mock_llm("summarize", doc):
        if tool not in TASK_TOOLS["summarize"]:     # blocked: not allowed for this task
            audit_log.append(("blocked", tool, args))
            continue
        run_tool(world, tool, args, approver)
    return doc[:40] + "..."
