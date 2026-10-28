# ADR-002: Explicit opt-in for subscription-wide changes

**Status:** Accepted for reference implementation
**Date:** 2026-10-27

## Context

Defender pricing, AzureActivity diagnostic routes and broad policy changes
can change cost, ingest sensitive records and affect applications outside
the SOC resource group.

## Decision

Defaults are off. Engineers must approve separate Terraform plans for
telemetry, Defender tiers and policy assignments. Policy is audit-only and
SOC resource-group scoped. Entra PIM and subscription-level policy
enforcement remain tenant governance workstreams, not bundled side effects.

## Consequences

Safer defaults and narrower blast radius; more manual tenant setup and an
explicit verification phase before claiming production coverage.
