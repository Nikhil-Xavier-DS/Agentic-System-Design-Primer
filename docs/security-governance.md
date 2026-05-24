# Security and Governance

Agent systems expand the attack surface because models interpret untrusted text and can trigger tools.

Controls:

- Treat retrieved documents and web content as untrusted input.
- Isolate tools with least privilege credentials.
- Require human approval for irreversible or high-impact actions.
- Redact secrets before prompts and logs.
- Use allowlisted tools and typed schemas.
- Store model calls and actions in audit logs.
- Evaluate prompt injection, data exfiltration, and unsafe tool use.
