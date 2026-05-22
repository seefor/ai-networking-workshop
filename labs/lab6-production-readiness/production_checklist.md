# Production Readiness Checklist for Network Agents

Use this checklist before connecting any AI-assisted workflow to real network systems.

The goal is not to slow you down. The goal is to keep the blast radius small while you learn what the agent is good at and where it still needs guardrails.

## 1. Scope and intent

- [ ] The use case is clearly defined.
- [ ] The agent has a written purpose statement.
- [ ] The agent is not being used where deterministic automation is simpler and safer.
- [ ] The first production evaluation is read-only.
- [ ] The approved device scope is documented.
- [ ] The approved command or API scope is documented.

## 2. Tool safety

- [ ] Every tool has a clear description.
- [ ] Every tool has validated inputs.
- [ ] Unknown devices are rejected.
- [ ] Unsafe commands are blocked.
- [ ] Read-only commands are allowlisted.
- [ ] Configuration commands require explicit human approval.
- [ ] Tool errors are returned as structured data instead of crashing the agent.

## 3. Secrets and access

- [ ] No credentials are hardcoded in code or prompts.
- [ ] Credentials are stored in environment variables or a secrets manager.
- [ ] The service account has least-privilege access.
- [ ] Read-only credentials are used first.
- [ ] Access to production devices is logged.
- [ ] Credential rotation is documented.

## 4. Human approval

- [ ] The agent can recommend actions without executing them.
- [ ] Risky actions require approval before execution.
- [ ] Approval requests include evidence and likely impact.
- [ ] Approval requests include the exact command or change.
- [ ] Approval decisions are logged.
- [ ] A rejected approval stops the workflow safely.

## 5. Observability and audit

- [ ] Every tool call is logged.
- [ ] Logs include timestamp, device, tool, command, user, and result summary.
- [ ] Failed tool calls are logged.
- [ ] Latency is measured for each tool call.
- [ ] Repeated failures create an alert or case.
- [ ] Agent outputs can be traced back to tool evidence.

## 6. Reliability

- [ ] Tool calls have timeouts.
- [ ] Transient failures have bounded retries.
- [ ] Retries use backoff.
- [ ] The agent fails closed when policy checks fail.
- [ ] The agent can handle partial data.
- [ ] The agent clearly reports uncertainty.

## 7. Data quality

- [ ] Tool outputs have predictable schemas.
- [ ] Parsed data is validated before use.
- [ ] Missing fields are handled explicitly.
- [ ] Mock data and production data are labeled.
- [ ] The agent does not invent device facts when tools return no data.

## 8. Testing path

- [ ] Unit tests cover tool wrappers.
- [ ] Lab tests run against mock data.
- [ ] Integration tests run against a sandbox or lab network.
- [ ] Failure scenarios are tested.
- [ ] Bad prompts and bad inputs are tested.
- [ ] A rollback or disable path exists.

## 9. Change control

- [ ] The agent does not bypass existing change management.
- [ ] Any configuration workflow creates a reviewable change request first.
- [ ] Change requests include evidence, commands, expected impact, and rollback notes.
- [ ] Executed changes are tied to a ticket or approved change ID.

## 10. Go/no-go review

Before moving beyond read-only use, answer these questions:

1. What is the worst thing this agent can do with its current permissions?
2. Can we detect that behavior quickly?
3. Can we stop or roll back safely?
4. Do logs explain why the agent made a recommendation?
5. Would we be comfortable showing the audit trail to leadership after an incident?

If the answer to any of those questions is weak, keep the agent in read-only or recommendation-only mode.
