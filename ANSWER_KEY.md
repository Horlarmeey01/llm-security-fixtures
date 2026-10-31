# Answer Key: Excessive Agency (OWASP LLM06)

## Verdict
- vulnerable/app.py: VULNERABLE
- secure/app.py: SECURE

## Vulnerability (vulnerable/app.py)
- Location: `summarize()`, the loop that calls `run_tool()` on every model-emitted tool call
- Root cause: The summarize() function executes every tool call the model returns, with no check on whether the task needs it. The agent has read, send and delete powers even though summarizing only needs read. Because the document is untrusted content, hidden instructions inside it get treated as commands, so an attacker can make the agent leak a secret or delete a file.
- Trigger: `docs/vendor_invoice.txt` carries injected instructions (indirect prompt injection)
- Impact: An attacker who can get a document in front of the agent, such as a vendor invoice, can make it email a secret (here, an API key) to an outside address and delete files, without ever having access to the system themselves.
- Related flaws: no path restriction, no recipient check, no human approval

## Fix (secure/app.py)
1. Per-task tool allow-list (`TASK_TOOLS`): least privilege
2. Path restriction on `read_file` (`ALLOWED_PREFIX`)
3. Human approval for high-risk tools (default deny)
4. Audit log of blocked calls

## Residual risk / what a strong reviewer should note
- Prompt injection itself is not prevented: the model still reads and may follow the hidden instructions. The fix only limits what the code will execute.
- The human approval step is a weak point. A tired or rushed reviewer could approve a malicious request, and an approver set to auto-approve would remove the protection.
- The allow-list is static, so if `send_email` were added to the summarize task, the flaw would return.

## Test mapping
   - test_vulnerable_leaks_and_deletes, test_secure_blocks_injection, test_secure_blocks_path_escape, test_benign_doc_works_in_both