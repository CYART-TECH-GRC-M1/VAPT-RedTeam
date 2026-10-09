# CyGRC VAPT & Red Team Execution Guide

**Project:** CyGRC Platform  
**Document:** VAPT + Red Team execution procedure  
**Purpose:** Practical, repeatable security-testing procedure for the CyGRC application and supporting infrastructure.

> **Authorization:** Perform testing only against systems, hosts, APIs, repositories, accounts, and environments explicitly approved for this engagement. Do not perform destructive, denial-of-service, persistence, credential attacks, or data-exfiltration activity outside the approved scope.

---

## 1. Objectives

### VAPT Team

Focus on identifying and validating vulnerabilities through structured application, API, infrastructure, configuration, source-code, container, and dependency testing.

**Outputs**
- Vulnerability inventory
- Reproduction steps
- Severity/risk rating
- Evidence
- Remediation recommendations
- Retest results

### Red Team

Focus on realistic attack paths and business impact rather than isolated scanner findings.

**Outputs**
- Attack-path narrative
- Initial-access attempts
- Privilege-escalation testing
- Lateral-movement opportunities
- Authentication/authorization bypass attempts
- Sensitive-data access validation
- Detection/control observations
- Attack timeline
- Recommendations

The two tracks should share evidence and findings while avoiding unnecessary duplicate testing.

---

# 2. Scope

## 2.1 In-Scope Components

Confirm the exact scope with the project owner before execution.

Typical CyGRC assessment scope:

- Web frontend
- Backend/API
- Authentication and authorization
- User/session management
- File upload/download functionality
- Database interactions exposed through the application
- Administrative functionality
- RBAC/permission model
- Third-party integrations
- Docker/container configuration
- Kubernetes configuration, if deployed
- CI/CD configuration where explicitly authorized
- Dependencies and package versions
- Secrets/configuration handling
- Exposed services and network interfaces
- Logging and security monitoring

## 2.2 Out of Scope Unless Explicitly Approved

- Production systems
- Third-party systems not owned by the project
- Denial-of-service/stress testing
- Destructive exploitation
- Permanent persistence
- Real-world phishing/social engineering
- Credential stuffing against external services
- Malware deployment
- Data destruction
- Exfiltration of real sensitive information

---

# 3. Engagement Rules

Before testing, document:

| Item | Requirement |
|---|---|
| Target environment | Development / staging / approved test environment |
| Target URLs/IPs | Record exact values |
| API base URL | Record exact value |
| Test accounts | Dedicated accounts |
| Admin account | Dedicated test admin |
| Test data | Synthetic data preferred |
| Testing window | Approved start/end time |
| Source IP | Record tester IPs where applicable |
| Rate limits | Respect application/infrastructure limits |
| Emergency contact | Project owner/security contact |
| Stop condition | Service instability, unintended data exposure, or unauthorized access |

### Stop immediately if

- The application becomes unstable.
- A test starts affecting unrelated systems.
- Real user/customer data is discovered.
- Credentials belonging to unrelated users are exposed.
- A vulnerability could cause irreversible damage.
- Activity leaves the approved scope.

---

# 4. Required Environment

## 4.1 Recommended Workstation

Linux is recommended.

Useful tooling:

- Git
- Docker / Docker Compose
- Python 3
- Node.js/npm
- curl
- jq
- nmap
- dig/nslookup
- openssl
- grep/ripgrep
- ffuf
- httpx
- nuclei
- semgrep
- Trivy
- OWASP ZAP or Burp Suite
- Postman or equivalent API client
- Browser developer tools

Install only tools required for the approved scope.

---

# 5. Repository Preparation

Clone the approved repository:

```bash
git clone <AUTHORIZED_REPOSITORY_URL>
cd <REPOSITORY_DIRECTORY>
```

If required, create a dedicated security branch:

```bash
git checkout -b security/vapt-assessment
```

Create an evidence directory outside the repository:

```bash
mkdir -p ~/cygrc-security/{recon,scans,evidence,requests,reports}
```

Do not commit discovered secrets, credentials, real sensitive data, or assessment artifacts into the application repository.

---

# 6. Application Setup

Use the project's official setup instructions first.

For Docker-based environments, inspect:

```bash
docker compose config
docker compose ps
docker images
```

Start the approved test environment using the project's documented command, for example:

```bash
docker compose up -d
```

Verify:

```bash
docker compose ps
docker compose logs --tail=100
```

Check exposed ports:

```bash
ss -lntup
```

Record:

- Frontend URL
- Backend/API URL
- API documentation URL
- Database/service ports
- Authentication mechanism
- Test credentials
- Container names
- Relevant environment variables

**Never copy production secrets into a local testing environment.**

---

# 7. Baseline Validation

Before security testing, establish that the application works normally.

Test:

1. Homepage/login
2. Normal user login
3. Admin/test-admin login
4. Logout
5. Password reset, if available
6. Core CRUD operations
7. File upload/download, if available
8. API health endpoints
9. Main application workflows

Example:

```bash
curl -i http://<AUTHORIZED_HOST>/
```

API example:

```bash
curl -i http://<AUTHORIZED_API>/api/health
```

Record HTTP status codes, headers, cookies, redirects, and response behavior.

---

# 8. VAPT Execution Procedure

## Phase 1 - Reconnaissance

Identify the exposed attack surface before exploitation.

Record:

- Domains/subdomains
- IP addresses
- Open ports
- Web technologies
- API endpoints
- Authentication endpoints
- Public files
- Documentation
- JavaScript bundles
- Server headers
- Framework/version information where exposed

Basic service discovery:

```bash
nmap -sV -Pn <AUTHORIZED_HOST>
```

Web technology discovery:

```bash
httpx -u http://<AUTHORIZED_HOST> -title -status-code -tech-detect
```

DNS information:

```bash
dig <AUTHORIZED_DOMAIN>
```

Keep reconnaissance limited to approved assets.

---

# 9. Web Application Testing

Use the OWASP Web Security Testing Guide as a testing framework:

https://owasp.org/www-project-web-security-testing-guide/

## Authentication

Test:

- Weak authentication controls
- Username enumeration
- Brute-force protections
- Password policy
- MFA enforcement, if applicable
- Session invalidation
- Password reset security
- Account lockout/rate limiting

## Authorization

Test:

- Horizontal privilege escalation
- Vertical privilege escalation
- IDOR/BOLA
- Missing function-level authorization
- Administrative endpoint exposure

Example methodology:

1. Log in as User A.
2. Capture an authorized request.
3. Change the object/resource identifier to another test user's resource.
4. Repeat as User B.
5. Confirm whether access is correctly denied.

Use dedicated test accounts and synthetic records.

## Session Management

Check:

- Secure cookie
- HttpOnly
- SameSite
- Session rotation
- Logout invalidation
- Session timeout
- Token expiration
- JWT validation
- Algorithm handling
- Refresh-token behavior

Inspect headers:

```bash
curl -I https://<AUTHORIZED_HOST>/
```

## Input Validation

Where applicable, test for:

- SQL injection
- NoSQL injection
- Command injection
- Template injection
- LDAP injection
- XSS
- Path traversal
- SSRF
- XML-related attacks

Do not treat a scanner finding as exploitable until manually validated.

---

# 10. API Security Testing

Enumerate the API surface from:

- Application traffic
- OpenAPI/Swagger documentation
- Source code
- Frontend JavaScript
- Approved documentation

Maintain an endpoint matrix:

| Method | Endpoint | Auth | Role | Object ID | Expected Result |
|---|---|---|---|---|---|
| GET | /api/... | Yes | User | ID | 200/403 |
| POST | /api/... | Yes | User | N/A | 201/403 |
| PUT | /api/... | Yes | Owner/Admin | ID | 200/403 |
| DELETE | /api/... | Yes | Admin | ID | 204/403 |

Test:

- Missing authentication
- Invalid/expired tokens
- Role bypass
- Object-level authorization
- Mass assignment
- Excessive data exposure
- Rate limiting
- Parameter tampering
- HTTP method manipulation
- CORS
- Error-message leakage
- API versioning issues

Reference:

https://owasp.org/API-Security/

---

# 11. Automated Web Scanning

Automated scanners are coverage tools, not final proof.

## Nuclei

Run only against approved targets:

```bash
nuclei -u https://<AUTHORIZED_HOST> \
  -o ~/cygrc-security/scans/nuclei.txt
```

https://nuclei.projectdiscovery.io/

## OWASP ZAP

Use for:

- Passive scanning
- Spidering
- API testing
- Active scanning where authorized

https://www.zaproxy.org/

## ffuf

Use controlled content discovery:

```bash
ffuf -u https://<AUTHORIZED_HOST>/FUZZ \
  -w <APPROVED_WORDLIST> \
  -rate 50 \
  -of json \
  -o ~/cygrc-security/scans/ffuf.json
```

Keep request rates low enough to avoid service degradation.

---

# 12. Source Code Review

Review backend and frontend code for:

- Hardcoded credentials
- Secrets/API keys
- Broken access control
- Unsafe deserialization
- SQL construction
- Shell command execution
- Path handling
- File upload logic
- SSRF
- Cryptography misuse
- Insecure random generation
- Sensitive logging
- Debug endpoints
- Unsafe CORS
- JWT implementation errors
- Dependency risks

Search for obvious secret candidates:

```bash
rg -n -i "password|passwd|secret|api[_-]?key|token|private[_-]?key" .
```

This produces candidates only. Manually validate every result.

## Semgrep

```bash
semgrep --config auto .
```

Record:

- Rule
- File
- Line
- Finding
- Exploitability
- False-positive decision

https://semgrep.dev/docs/

---

# 13. Dependency and Container Security

Identify package manifests such as:

- package.json
- requirements.txt
- pyproject.toml
- package-lock.json
- yarn.lock
- pnpm-lock.yaml
- go.mod
- pom.xml

For Node.js:

```bash
npm audit
```

## Trivy

Filesystem:

```bash
trivy fs .
```

Container image:

```bash
trivy image <AUTHORIZED_IMAGE>
```

https://trivy.dev/

Check for:

- Critical/high CVEs
- End-of-life packages
- Vulnerable base images
- Secrets
- Misconfigurations

Prioritize vulnerabilities that are reachable and exploitable in the actual deployment.

---

# 14. Docker / Container Review

Inspect:

```bash
docker compose config
docker inspect <CONTAINER>
```

Check:

- Running as root
- Privileged mode
- Host networking
- Excessive Linux capabilities
- Writable sensitive mounts
- Docker socket exposure
- Secrets in environment variables
- Unnecessary ports
- Outdated base images
- Debug services
- Weak health-check configuration

Avoid modifying running containers unless explicitly authorized.

---

# 15. Kubernetes Review

Only if Kubernetes is in scope.

Review:

```bash
kubectl get namespaces
kubectl get pods -A
kubectl get svc -A
kubectl get ingress -A
```

Inspect workloads:

```bash
kubectl get deployment <NAME> -o yaml
```

Check:

- RBAC
- Service accounts
- Privileged containers
- HostPath mounts
- Secrets exposure
- Network policies
- Pod security settings
- Ingress exposure
- Image provenance
- Resource limits

Do not delete, restart, or modify production resources during assessment.

---

# 16. Infrastructure Testing

For approved hosts:

```bash
nmap -sV -sC -Pn <AUTHORIZED_IP>
```

Document:

- Open ports
- Service versions
- Unexpected services
- Administrative interfaces
- TLS configuration
- Exposed databases
- Exposed monitoring/debug interfaces

TLS inspection:

```bash
openssl s_client -connect <AUTHORIZED_HOST>:443
```

Check:

- TLS version
- Certificate validity
- Certificate hostname
- Weak protocols/ciphers
- HTTP-to-HTTPS redirects
- HSTS

---

# 17. Red Team Execution Procedure

The Red Team simulates a realistic attacker while maintaining strict engagement boundaries.

> **Atomic Red Team Framework:** For unit-level technique execution, telemetry validation, and MITRE ATT&CK detection testing, refer to the dedicated [Atomic Red Team Workstream](docs/redteam/README.md) documentation (`docs/redteam/`).

## Phase 1 - Recon

Identify:

- External attack surface
- Login pages
- API endpoints
- Public documents
- Technology stack
- Potential trust boundaries

**Output:** attack-surface map.

## Phase 2 - Initial Access

Test approved avenues such as:

- Authentication weaknesses
- Authorization weaknesses
- Exposed administrative interfaces
- Vulnerable application functionality
- Misconfigured services
- Valid test credentials where explicitly provided

Do not use real-world credential theft or unauthorized phishing.

## Phase 3 - Establish Objective

Define the agreed objective before exploitation.

Examples:

- Access another test user's data
- Obtain administrative privileges in the test environment
- Demonstrate unauthorized API access
- Access a protected test file
- Demonstrate command execution with a harmless command

A Red Team finding should answer:

**What could an attacker actually achieve?**

## Phase 4 - Privilege Escalation

Test:

- Application role escalation
- Broken RBAC
- Insecure direct object references
- Container privileges
- Excessive service permissions
- Credential exposure

## Phase 5 - Lateral Movement

Only where explicitly authorized.

Check whether compromise of one component permits access to:

- Backend services
- Databases
- Internal APIs
- Administrative services
- Other containers

Use synthetic/test credentials and stop once the agreed objective is demonstrated.

## Phase 6 - Impact Validation

Demonstrate impact minimally.

Examples:

- Read one synthetic record instead of dumping a database.
- Access one protected endpoint instead of extracting all records.
- Demonstrate command execution with a harmless command.
- Demonstrate privilege escalation without persistence.

## Phase 7 - Cleanup

Remove:

- Test accounts created solely for exploitation
- Temporary files
- Temporary tokens
- Test payloads
- Temporary configuration changes

Verify the environment returns to baseline.

---

# 18. Evidence Collection

Recommended structure:

```text
~/cygrc-security/evidence/
├── VAPT-001/
│   ├── request.txt
│   ├── response.txt
│   ├── screenshot.png
│   └── notes.md
├── VAPT-002/
└── RT-001/
    ├── timeline.md
    ├── request.txt
    └── screenshot.png
```

Every finding should contain:

1. Finding ID
2. Title
3. Asset
4. Endpoint
5. Preconditions
6. Test account/role
7. Exact steps
8. Request
9. Response
10. Evidence
11. Impact
12. Severity
13. Remediation
14. Retest status

Never store real secrets in screenshots or reports unless explicitly required and securely handled.

---

# 19. Severity Classification

Use CVSS where technically appropriate:

https://www.first.org/cvss/

| Severity | Meaning |
|---|---|
| Critical | Direct compromise, severe unauthorized access, or catastrophic impact |
| High | Significant compromise or privilege escalation |
| Medium | Meaningful security weakness with limited or conditional impact |
| Low | Limited impact or defense-in-depth issue |
| Informational | Observation/recommendation without direct vulnerability |

Consider:

- Exploitability
- Required privileges
- Required user interaction
- Scope
- Confidentiality impact
- Integrity impact
- Availability impact
- Business impact

Do not inflate severity merely because a scanner labels something "critical."

---

# 20. Finding Template

Use this format for every confirmed issue:

```text
Finding ID:
Title:
Severity:
CVSS:
Asset:
Endpoint/Component:

Description:
<What is wrong?>

Preconditions:
<What must be true before exploitation?>

Reproduction:
1.
2.
3.

Request:
<Relevant request>

Response:
<Relevant response>

Evidence:
<Filename/path>

Impact:
<What can an attacker actually do?>

Root Cause:
<Why does the vulnerability exist?>

Remediation:
<Specific fix>

References:
<Relevant OWASP/CWE/CVSS reference>

Retest:
Not Tested / Fixed / Partially Fixed / Not Fixed

Retest Evidence:
<Filename/path>
```

---

# 21. VAPT vs Red Team Work Allocation

## VAPT Members

Primary responsibility:

- Reconnaissance
- Web application testing
- API testing
- Source-code review
- Dependency scanning
- Container scanning
- Infrastructure scanning
- Configuration review
- Vulnerability validation
- CVSS scoring
- Technical remediation recommendations
- Retesting

## Red Team Members

Primary responsibility:

- Attack-surface analysis
- Attack-path development
- Initial-access simulation
- Privilege-escalation testing
- Trust-boundary analysis
- Lateral-movement testing
- Objective/impact validation
- Detection/control assessment
- Attack timeline
- Adversary narrative
- Cleanup and post-operation validation

### Atomic Red Team Workstream

**Owner:** Alakati Rithesh Chandra  
**Branch:** `feature/redteam-atomic`  
**Documentation:** [`docs/redteam/`](docs/redteam/README.md)

Primary responsibility:

- Curate and maintain the Atomic Red Team test catalog aligned with CyGRC endpoints and MITRE ATT&CK.
- Map adversarial techniques to defensive telemetry sources (Windows Event 4688, Sysmon, PowerShell 4104).
- Execute controlled single-technique unit tests in authorized environments following the [Execution Guide](docs/redteam/execution-guide.md).
- Capture cryptographic execution evidence and sanitize repository outputs ([Evidence Index](docs/redteam/evidence-index.md)).
- Verify defensive detection outcomes (differentiating command success from security detection).
- Document and verify complete system restoration and artifact cleanup ([Cleanup Checklist](docs/redteam/cleanup-checklist.md)).
- Deliver workstream completion documentation ([Completion Report](docs/redteam/completion-report.md)).
- Submit all workstream enhancements via Pull Requests to `main`.

## Shared Responsibilities

Both teams should:

- Coordinate scope
- Maintain evidence
- Avoid duplicate testing
- Report confirmed vulnerabilities
- Protect credentials and sensitive data
- Record timestamps
- Immediately escalate critical findings
- Participate in final remediation/retest

---

# 22. Suggested Execution Order

```text
1. Confirm authorization and scope
        ↓
2. Prepare test environment and accounts
        ↓
3. Baseline application functionality
        ↓
4. Reconnaissance
        ↓
5. VAPT automated discovery
        ↓
6. Manual web/API testing
        ↓
7. Source-code/dependency review
        ↓
8. Container/infrastructure review
        ↓
9. Red Team attack-path testing
        ↓
10. Validate business impact
        ↓
11. Evidence consolidation
        ↓
12. Risk scoring
        ↓
13. Remediation report
        ↓
14. Fixes implemented
        ↓
15. Retest
        ↓
16. Final report
```

---

# 23. Daily Execution Checklist

## Start of Day

- [ ] Confirm target environment
- [ ] Confirm testing window
- [ ] Confirm accounts are working
- [ ] Confirm scope
- [ ] Check for application changes
- [ ] Review previous findings
- [ ] Confirm evidence directory

## During Testing

- [ ] Record target
- [ ] Record timestamp
- [ ] Record tester
- [ ] Capture request/response
- [ ] Avoid unnecessary destructive actions
- [ ] Tag findings immediately
- [ ] Stop and escalate critical unexpected impact

## End of Day

- [ ] Save evidence
- [ ] Update finding tracker
- [ ] Update attack timeline
- [ ] Clean temporary artifacts
- [ ] Revert approved temporary changes
- [ ] Record blockers
- [ ] Record next steps

---

# 24. Recommended References

### OWASP

Top 10:
https://owasp.org/www-project-top-ten/

Web Security Testing Guide:
https://owasp.org/www-project-web-security-testing-guide/

API Security:
https://owasp.org/API-Security/

Cheat Sheet Series:
https://cheatsheetseries.owasp.org/

### CWE

https://cwe.mitre.org/

### CVSS

https://www.first.org/cvss/

### NIST

https://www.nist.gov/cyberframework

### Nuclei

https://nuclei.projectdiscovery.io/

### ProjectDiscovery

https://projectdiscovery.io/

### Semgrep

https://semgrep.dev/docs/

### Trivy

https://trivy.dev/

### OWASP ZAP

https://www.zaproxy.org/

### Burp Suite

https://portswigger.net/burp

---

# 25. Final Deliverables

## VAPT Report

- Executive summary
- Scope
- Methodology
- Asset inventory
- Vulnerability summary
- Detailed findings
- Severity distribution
- Evidence
- Remediation recommendations
- Retest results
- Appendix/tool output

## Red Team Report

- Executive summary
- Rules of engagement
- Attack surface
- Threat model
- Attack paths
- Timeline
- Initial access
- Privilege escalation
- Lateral movement
- Objective achieved/not achieved
- Detection gaps
- Business impact
- Recommendations
- Cleanup confirmation

## Management Summary

A non-technical summary containing:

- Number of Critical/High/Medium/Low findings
- Most important attack path
- Business impact
- Top remediation priorities
- Current residual risk
- Retest status

---

# 26. Evidence Naming Convention

Use consistent IDs:

```text
VAPT-001
VAPT-002
VAPT-003

RT-001
RT-002
RT-003
```

Evidence filenames:

```text
VAPT-001-request.txt
VAPT-001-response.txt
VAPT-001-screenshot-01.png

RT-001-step-01.png
RT-001-command-output.txt
RT-001-timeline.md
```

Avoid ambiguous names such as:

```text
final.png
new.txt
test2.txt
scan-final-final.txt
```

Humanity has suffered enough from files called `final_final_v2_REAL.docx`.

---

# 27. Rules for Automated Tools

For every automated result:

1. Confirm the target is in scope.
2. Confirm the finding is reproducible.
3. Determine whether exploitation is possible.
4. Remove false positives.
5. Assess actual impact.
6. Assign appropriate severity.
7. Record evidence.
8. Provide a remediation recommendation.

Do not paste raw scanner output into the final report as if it were a validated vulnerability.

---

# 28. Critical Finding Escalation

If a Critical or potentially catastrophic vulnerability is discovered:

1. Stop further exploitation.
2. Preserve minimum necessary evidence.
3. Notify the designated project/security contact.
4. Record the exact affected asset.
5. Describe the demonstrated impact.
6. Do not expand exploitation unless explicitly authorized.
7. Coordinate remediation.
8. Retest after the fix.

---

# 29. Completion Criteria

The engagement is complete when:

- All approved assets have been assessed.
- VAPT test cases have been executed or marked Not Applicable.
- Red Team objectives have been attempted.
- Findings have been validated.
- Evidence is organized.
- False positives are removed.
- Severity has been assigned.
- Remediation recommendations are documented.
- Critical/high issues have been communicated.
- Retesting has been completed where fixes are available.
- Final reports are delivered.
- Temporary testing artifacts have been removed.

---

# 30. Operating Principle

The objective is **not** to produce the largest number of scanner findings.

The objective is to answer:

> **Can an attacker compromise the application, bypass security controls, access unauthorized data, escalate privileges, or reach a meaningful business objective?**

VAPT establishes technical weaknesses.

Red Team testing connects those weaknesses into realistic attack paths.

Together they provide a much more useful security picture than either approach alone.
