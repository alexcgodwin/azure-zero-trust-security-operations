# Incident runbook: network security group rule change

1. Identify the NSG, rule, priority, source/destination, port and direction.
2. Confirm which subnets or NICs the NSG protects and calculate effective rules.
3. Correlate actor and timestamp with a signed Terraform deployment or ticket.
4. Check whether the change opened broad ingress/egress or bypassed inspection.
5. Escalate to network owner; request explicit approval before any rollback.
6. Validate post-change connectivity with a controlled test, then document.
7. Tune allowlisted deployment identities only with expiration and review.

NSG updates may be legitimate during rollouts. Never rollback automatically,
as doing so can break production connectivity or security agents.
