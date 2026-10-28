# ADR-001: Review-first security incident automation

**Status:** Accepted for reference implementation
**Date:** 2026-10-27

## Context

Security automation that disables accounts or modifies network policy can
produce serious availability and business risk when source signals are wrong,
incomplete or attacker-controlled.

## Decision

The repository implements an offline read-only Python triage library that
returns risk scores and investigation steps. It has no Azure SDK, Graph API
write permissions, cloud secret storage or automated remediation function.
Real containment always requires human approval, scope checks and a separate
well-audited execution channel.

## Consequences

Positive: safe demonstrations and meaningful tests without risking tenant
resources. Limitation: not a live SOAR/Logic Apps integration. Before adding
a live connector, require an ADR, staged testing, least-privilege role
design, retry/idempotency controls and security review.
