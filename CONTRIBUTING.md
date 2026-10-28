# Contributing

Changes to detections and infrastructure are security-sensitive.

1. Open an issue describing the threat hypothesis, expected signals and possible false positives.
2. Work on a branch, submit a pull request and get an independent reviewer.
3. Include synthetic tests for new detection queries or response logic.
4. Explain cost and permission impact of any new Azure resource.
5. Record an ADR when changing trust boundaries, identity, scope or deployment safety.
6. Avoid secrets, personal data, real production incident records or token material in examples.
7. Never enable automatic containment or subscription-wide Defender tiers by default.
8. CI validates only; deployments require a protected environment and explicit approval.

See docs/DEPLOYMENT.md for operator approval and rollback expectations.
