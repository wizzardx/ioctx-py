# Security Policy

## Reporting a Vulnerability

The ioctx-py team takes security issues seriously. We appreciate your efforts to responsibly disclose your findings and will make every effort to acknowledge your contributions.

### How to Report a Vulnerability

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to [security@example.com](mailto:security@example.com) (replace with your actual security contact email).

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

### What to Include in Your Report

To help us better understand and address the issue, please include the following information in your report:

1. Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
2. Full paths of source file(s) related to the manifestation of the issue
3. The location of the affected source code (tag/branch/commit or direct URL)
4. Any special configuration required to reproduce the issue
5. Step-by-step instructions to reproduce the issue
6. Proof-of-concept or exploit code (if possible)
7. Impact of the issue, including how an attacker might exploit the issue

### Security Update Process

After a security vulnerability is reported:

1. The security team will confirm the vulnerability and determine its impact.
2. The security team will work on a fix and release timeline.
3. Once a fix is prepared, the security team may request additional review from the reporter.
4. A new release addressing the vulnerability will be issued, and the vulnerability will be publicly disclosed.

## Supported Versions

Security updates will be provided for the following versions of ioctx-py:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security Best Practices When Using ioctx-py

When using ioctx-py in security-sensitive contexts, we recommend the following practices:

1. Be cautious when using `RealIO` to execute system commands, especially with user-provided input.
2. Use `ValidatingIO` (when implemented) to restrict IO operations to specific domains and file paths.
3. Avoid storing sensitive information in the trace logs produced by `TracingIO`.
4. When saving and loading recordings from `ReplayIO` (when implemented), validate their source and content.

## Bug Bounty

We do not currently offer a bug bounty program.

## Public Disclosure

We aim to disclose vulnerabilities after they have been addressed. We request that you respect this process and not disclose issues publicly until we have had a chance to release a fix.

Thank you for helping keep ioctx-py and its users secure!
