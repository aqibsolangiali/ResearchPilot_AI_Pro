# Security Policy — ResearchPilot AI Pro

## Important: current public prototype is not a secure multi-user product

The project currently has **no authentication, per-user permissions or isolated document storage**. It exposes endpoints that can upload, list, search and delete documents from a shared SQLite research library. Anyone with API access may be able to access or remove data from that library, regardless of frontend CORS restrictions.

**Do not upload personal, confidential, copyrighted restricted, unpublished or sensitive PDFs to a public deployment.** Use only synthetic/test documents on a locally controlled instance.

## Immediate deployment guidance

1. **Until protected, suspend/restrict the public backend** in your hosting dashboard (or deploy a separate restricted demonstration backend) to prevent public access to its mutable document endpoints.
2. Do not enable paid LLM API keys on an open backend; a visitor could generate chargeable requests.
3. Store API keys only as server environment variables; never commit real credentials to Git.
4. Treat `CORS_ORIGINS` as browser-access configuration, **not** as authorization.
5. Add authentication and document-level ownership checks before reopening uploads and deletes.

## Required hardening before production

- User login, session management and explicit ownership checks on **every** document and query endpoint.
- Separate storage by user/workspace; private document blobs and durable database persistence.
- Request-rate limits, upload-size and resource limits, PDF safety controls, retention/delete policy.
- Secret handling, audit logs, monitoring, backups and deployment HTTPS.
- Tests for unauthorized reads, uploads, enumeration, search, comparison and deletion.
- Prompt-injection defenses for PDF content and clear warnings for optional external LLM processing.

## Reporting a vulnerability

Do not post secrets, personal PDFs or exploitable vulnerabilities in public GitHub issues. Contact the repository maintainer privately through an appropriate GitHub channel.

This file documents known risk. **It does not implement the safeguards.**
