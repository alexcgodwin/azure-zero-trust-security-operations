# Incident runbook: unexpected privileged role assignment

**Prerequisite:** AzureActivity connector and consistent operation logging.

1. Verify alert timeframe and operation name; preserve activity correlation ID.
2. Inspect actor principal, IP, resource scope and affected role.
3. Correlate with approved change request and Entra sign-in/session context.
4. Ask subscription security owner whether the assignment was authorized.
5. For confirmed compromise, activate the organization's incident response
   procedure; privileged changes require identity-owner authorization.
6. Validate the assignment was safely removed **by an approved operator**
   and that affected access tokens/sessions have been considered.
7. Record incident timeline, queries, approvals and rule tuning.

False positives: CI service principals, break-glass recovery events,
privileged identity eligible activation, authorized platform provisioning.
Do not auto-disable users or delete assignments based only on the query.
