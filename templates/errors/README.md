# QyberHost Error Templates

This directory is organized by scenario so static error themes can be mapped cleanly into the project.

## Categories

- `http-status`: standard HTTP error codes such as `404`, `500`, `503`
- `auth-access`: login, session, verification, and access-related errors
- `maintenance-service`: planned maintenance, emergency maintenance, service unavailable, coming soon
- `hosting-service`: hosting, server, backup, SSL, and provisioning issues
- `billing-order`: payment, invoice, refund, checkout, and order failures
- `security`: blocked access, suspicious activity, firewall, DDoS, region restrictions
- `integration`: third-party API, gateway, webhook, and provisioning integration failures
- `generic`: fallback business error states that do not map to a specific subsystem
- `source`: original imported error theme package and assets

## Notes

- Existing `404` and `maintenance` templates were moved into category folders.
- The imported Erratum package was preserved under `source/erratum-html`.
- Newly created files are starter placeholders and can be replaced with final themed pages.
