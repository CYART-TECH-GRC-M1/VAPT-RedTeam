# Atomic Red Team Test Catalog

**Project:** CyGRC Module 2 — VAPT & Red Team  
**Workstream:** Atomic Red Team & Technique Execution  
**Owner:** Alakati Rithesh Chandra  
**Git Branch:** `feature/redteam-atomic`  
**Catalog Status:** Active — Curated Baseline  

---

## 1. Executive Summary & Workstream Objective

The Atomic Red Team workstream within the CyGRC project provides a structured, repeatable, and safe mechanism for executing unit-level security tests mapped to the MITRE ATT&CK framework. Its primary objective is **detection telemetry validation**: verifying whether defensive monitoring controls (Windows Security Event Logs, PowerShell Script Block Logging, Sysmon, and Endpoint Detection & Response / EDR agents) reliably generate, capture, and alert on adversary techniques.

In accordance with engagement rules and defensive engineering principles:
- Tests prioritize **safe, representative, single-technique behaviors** rather than destructive exploits or multi-stage payloads.
- **Strict separation of concerns:** A successful command execution (`PASS`) is never conflated with successful defensive detection (`DETECTED`).
- Live execution is strictly gated by written authorization, environmental verification, and pre-execution baselines.

---

## 2. Test Catalog Summary Register

| Test ID | Test Name | ATT&CK ID | ATT&CK Tactic | Platform | Elevation | Execution Status | Telemetry Status | Detection Status | Cleanup Status |
|---|---|---|---|---|---|---|---|---|---|
| **RT-AT-001** | NTFS Alternate Data Stream Access | T1059.001 / T1564.004 | Execution / Defense Evasion | Windows | Standard User | **PASS** (Executed) | NOT OBSERVED (Targeted query) | INCOMPLETE | **PASS** (File removed) |
| **RT-AT-002** | System Information Discovery (`systeminfo`) | T1082 | Discovery | Windows | Standard User | **APPROVED CANDIDATE** | Telemetry Model Ready | Pending Execution | Not Applicable (Read-only) |
| **RT-AT-003** | System Owner/User Discovery (`whoami`) | T1033 | Discovery | Windows | Standard User | **APPROVED CANDIDATE** | Telemetry Model Ready | Pending Execution | Not Applicable (Read-only) |
| **RT-AT-004** | Process Discovery (`tasklist`) | T1057 | Discovery | Windows | Standard User | **APPROVED CANDIDATE** | Telemetry Model Ready | Pending Execution | Not Applicable (Read-only) |
| **RT-AT-005** | Indicator Removal: Benign File Deletion | T1070.004 | Defense Evasion | Windows | Standard User | **APPROVED CANDIDATE** | Telemetry Model Ready | Pending Execution | Verified on Execution |
| **RT-AT-006** | Modify Registry: Benign HKCU Test Key | T1112 | Defense Evasion | Windows | Standard User | **APPROVED CANDIDATE** | Telemetry Model Ready | Pending Execution | Rollback Script Verified |
| **RT-AT-007** | PowerShell Encoded Command Execution | T1059.001 | Execution | Windows | Standard User | **APPROVED CANDIDATE** | Telemetry Model Ready | Pending Execution | Not Applicable (Ephemeral) |
| **RT-AT-008** | System Network Configuration Discovery | T1016 | Discovery | Windows | Standard User | **APPROVED CANDIDATE** | Telemetry Model Ready | Pending Execution | Not Applicable (Read-only) |

---

## 3. Detailed Test Specification Sheets

### Test RT-AT-001: NTFS Alternate Data Stream Access

- **Test Name:** NTFS Alternate Data Stream Access
- **Unique Identifier:** `RT-AT-001`
- **MITRE ATT&CK Tactic:** Execution / Defense Evasion
- **MITRE ATT&CK Technique ID:** `T1059.001` (Command and Scripting Interpreter: PowerShell); cross-mapped to `T1564.004` (Hide Artifacts: NTFS File Attributes)
- **Technique Name:** Command and Scripting Interpreter: PowerShell
- **Atomic Red Team Reference:** Test #11 in `T1059.001.yaml`
- **Atomic Test GUID:** `8e5c5532-1181-4c1d-bb79-b3a9f5dbd680`
- **Target Operating System:** Windows 10/11, Windows Server (NTFS volume)
- **Prerequisites:**
  - Active NTFS filesystem drive (e.g., `C:`).
  - Windows PowerShell 5.1 or PowerShell Core installed.
  - Standard user write access to `$env:TEMP`.
- **Test Objective & Expected Behavior:**
  - Creates a benign temporary text file (`$env:TEMP\NTFS_ADS.txt`), attaches an alternate data stream named `streamCommand` containing a PowerShell command (`Write-Host "Stream Data Executed"`), and executes the stream content using `Invoke-Expression`.
- **Required Permissions & Execution Context:** Standard User (Non-elevated).
- **Approved Execution Command:**
  ```powershell
  Add-Content -Path $env:TEMP\NTFS_ADS.txt -Value 'Write-Host "Stream Data Executed"' -Stream 'streamCommand'
  $streamData = Get-Content -Path $env:TEMP\NTFS_ADS.txt -Stream 'streamCommand'
  Invoke-Expression -Command $streamData
  ```
- **Expected Telemetry & Event Sources:**
  - *PowerShell Script Block Logging:* Microsoft-Windows-PowerShell/Operational Event ID 4104 capturing `Invoke-Expression` and stream execution.
  - *Process Creation:* Windows Security Event ID 4688 / Sysmon Event ID 1 (powershell.exe process execution).
  - *File Alternate Stream Creation:* Sysmon Event ID 15 (FileCreateStreamHash) recording creation of stream `streamCommand` on `NTFS_ADS.txt`.
- **Expected Outcome & Validation Criteria:**
  - Process exit code `0`.
  - Standard output contains exact string: `Stream Data Executed`.
- **Risk Level & Operational Impact:**
  - Risk Level: **Low**.
  - Operational Impact: Writes a single temporary file to `$env:TEMP`; does not touch system directories or modify configuration.
- **Rollback Requirements & Cleanup Procedure:**
  - Cleanup Command:
    ```powershell
    Remove-Item -Path $env:TEMP\NTFS_ADS.txt -Force -ErrorAction SilentlyContinue
    ```
  - Post-Execution Verification:
    ```powershell
    Test-Path -Path "$env:TEMP\NTFS_ADS.txt" # Must return False
    ```
- **Observed Execution Status:** **PASS** (Executed 2026-10-09T20:28:22+05:30; stdout verified; exit code 0; cleanup confirmed).
- **Observed Telemetry Status:** **NOT OBSERVED** by targeted query (broader event logs contained 42 events, but query returned 0 matches for test parameters; Defender quarantined unrelated adjacent files in the atomic repo).
- **Official References:**
  - [MITRE ATT&CK T1059.001](https://attack.mitre.org/techniques/T1059/001/)
  - [MITRE ATT&CK T1564.004](https://attack.mitre.org/techniques/T1564/004/)
  - [Atomic Red Team T1059.001](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1059.001/T1059.001.md)

---

### Test RT-AT-002: System Information Discovery via systeminfo.exe

- **Test Name:** System Information Discovery via systeminfo.exe
- **Unique Identifier:** `RT-AT-002`
- **MITRE ATT&CK Tactic:** Discovery
- **MITRE ATT&CK Technique ID:** `T1082`
- **Technique Name:** System Information Discovery
- **Atomic Red Team Reference:** Test #1 in `T1082.yaml`
- **Atomic Test GUID:** `3203ae23-162b-4ba9-a78b-87db9746e53f`
- **Target Operating System:** Windows 10/11, Windows Server 2016+
- **Prerequisites:**
  - Standard Windows installation with `%SystemRoot%\System32\systeminfo.exe` accessible.
- **Test Objective & Expected Behavior:**
  - Simulates adversary situational awareness reconnaissance gathering OS build, hotfix list, BIOS version, memory, and domain membership.
- **Required Permissions & Execution Context:** Standard User (Non-elevated).
- **Approved Execution Command:**
  ```powershell
  systeminfo.exe
  ```
- **Expected Telemetry & Event Sources:**
  - *Process Creation:* Windows Security Event ID 4688 (`New Process Name: C:\Windows\System32\systeminfo.exe`).
  - *Sysmon Process Create:* Sysmon Event ID 1 (`Image: C:\Windows\System32\systeminfo.exe`, `ParentImage: powershell.exe` or `cmd.exe`).
  - *WMI / CIM Query Activity:* Microsoft-Windows-WMI-Activity/Operational Event ID 5857/5858 if WMI queries are initiated.
- **Expected Outcome & Validation Criteria:**
  - Process exit code `0`.
  - Standard output contains detailed OS configuration (e.g., `OS Name:`, `OS Version:`, `Hotfix(s):`).
- **Risk Level & Operational Impact:**
  - Risk Level: **Very Low**.
  - Operational Impact: Completely read-only query; negligible temporary CPU consumption while gathering hardware and hotfix records.
- **Rollback Requirements & Cleanup Procedure:**
  - Cleanup Command: None required (read-only execution).
  - Post-Execution Verification:
    ```powershell
    Get-Process -Name systeminfo -ErrorAction SilentlyContinue # Must return null/empty
    ```
- **Status:** **APPROVED CANDIDATE** (Planned — awaiting lead approval to resume live executions).
- **Official References:**
  - [MITRE ATT&CK T1082](https://attack.mitre.org/techniques/T1082/)
  - [Atomic Red Team T1082](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1082/T1082.md)

---

### Test RT-AT-003: System Owner/User Discovery via whoami.exe

- **Test Name:** System Owner/User Discovery via whoami.exe
- **Unique Identifier:** `RT-AT-003`
- **MITRE ATT&CK Tactic:** Discovery
- **MITRE ATT&CK Technique ID:** `T1033`
- **Technique Name:** System Owner/User Discovery
- **Atomic Red Team Reference:** Test #1 in `T1033.yaml`
- **Atomic Test GUID:** `29849544-fc0b-4876-b6f4-c9233010b9ad`
- **Target Operating System:** Windows 10/11, Windows Server
- **Prerequisites:**
  - `%SystemRoot%\System32\whoami.exe` available.
- **Test Objective & Expected Behavior:**
  - Simulates post-compromise user context identification, enumerating current username, user SID, group memberships, and token privileges.
- **Required Permissions & Execution Context:** Standard User (Non-elevated).
- **Approved Execution Command:**
  ```powershell
  whoami.exe /all
  ```
- **Expected Telemetry & Event Sources:**
  - *Process Creation:* Windows Security Event ID 4688 (`CommandLine: whoami.exe /all`, `TokenElevationType: %%1938` or `%%1936`).
  - *Sysmon Process Create:* Sysmon Event ID 1 (`Image: C:\Windows\System32\whoami.exe`, `CommandLine: whoami.exe /all`).
- **Expected Outcome & Validation Criteria:**
  - Process exit code `0`.
  - Standard output contains USER INFORMATION, GROUP INFORMATION, and PRIVILEGES INFORMATION tables.
- **Risk Level & Operational Impact:**
  - Risk Level: **Very Low**.
  - Operational Impact: Read-only command; zero state modification.
- **Rollback Requirements & Cleanup Procedure:**
  - Cleanup Command: None required.
  - Post-Execution Verification: Verify process termination.
- **Status:** **APPROVED CANDIDATE** (Planned).
- **Official References:**
  - [MITRE ATT&CK T1033](https://attack.mitre.org/techniques/T1033/)
  - [Atomic Red Team T1033](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1033/T1033.md)

---

### Test RT-AT-004: Process Discovery via tasklist.exe

- **Test Name:** Process Discovery via tasklist.exe
- **Unique Identifier:** `RT-AT-004`
- **MITRE ATT&CK Tactic:** Discovery
- **MITRE ATT&CK Technique ID:** `T1057`
- **Technique Name:** Process Discovery
- **Atomic Red Team Reference:** Test #1 in `T1057.yaml`
- **Atomic Test GUID:** `c11e4916-24ba-467a-b9c1-4b2a8d461718`
- **Target Operating System:** Windows 10/11, Windows Server
- **Prerequisites:**
  - `%SystemRoot%\System32\tasklist.exe` available.
- **Test Objective & Expected Behavior:**
  - Simulates adversary process enumeration checking for running security agents, monitoring tooling, database services, or target applications.
- **Required Permissions & Execution Context:** Standard User (Non-elevated).
- **Approved Execution Command:**
  ```powershell
  tasklist.exe /v
  ```
- **Expected Telemetry & Event Sources:**
  - *Process Creation:* Windows Security Event ID 4688 (`New Process Name: C:\Windows\System32\tasklist.exe`).
  - *Sysmon Process Create:* Sysmon Event ID 1 (`Image: C:\Windows\System32\tasklist.exe`, `CommandLine: tasklist.exe /v`).
- **Expected Outcome & Validation Criteria:**
  - Process exit code `0`.
  - Output contains running processes, Session names, PID, and User Name.
- **Risk Level & Operational Impact:**
  - Risk Level: **Very Low**.
  - Operational Impact: Read-only process table snapshot.
- **Rollback Requirements & Cleanup Procedure:**
  - Cleanup Command: None required.
  - Post-Execution Verification: Verify process termination.
- **Status:** **APPROVED CANDIDATE** (Planned).
- **Official References:**
  - [MITRE ATT&CK T1057](https://attack.mitre.org/techniques/T1057/)
  - [Atomic Red Team T1057](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1057/T1057.md)

---

### Test RT-AT-005: Indicator Removal: Benign File Deletion

- **Test Name:** Indicator Removal: Benign File Deletion
- **Unique Identifier:** `RT-AT-005`
- **MITRE ATT&CK Tactic:** Defense Evasion
- **MITRE ATT&CK Technique ID:** `T1070.004`
- **Technique Name:** Indicator Removal: File Deletion
- **Atomic Red Team Reference:** Test #1 in `T1070.004.yaml`
- **Atomic Test GUID:** `b6be29e8-323b-47eb-ba68-d069415518b2`
- **Target Operating System:** Windows 10/11, Windows Server
- **Prerequisites:**
  - Write and delete permissions in `$env:TEMP`.
- **Test Objective & Expected Behavior:**
  - Creates a dedicated marker file in `$env:TEMP` and immediately deletes it to test endpoint file-deletion auditing and anti-forensics tracking.
- **Required Permissions & Execution Context:** Standard User (Non-elevated).
- **Approved Execution Command:**
  ```powershell
  New-Item -Path "$env:TEMP\art-file-deletion.tmp" -ItemType File -Value "Atomic Test Marker" -Force | Out-Null
  Remove-Item -Path "$env:TEMP\art-file-deletion.tmp" -Force
  ```
- **Expected Telemetry & Event Sources:**
  - *Sysmon File Create:* Sysmon Event ID 11 (`TargetFilename: ...\art-file-deletion.tmp`).
  - *Sysmon File Delete:* Sysmon Event ID 23 (FileDelete: archived or recorded).
  - *PowerShell Script Block Logging:* Microsoft-Windows-PowerShell/Operational Event ID 4104 (`Remove-Item`).
- **Expected Outcome & Validation Criteria:**
  - Execution completes with exit code `0`.
  - File exists transiently and is deleted immediately upon command completion.
- **Risk Level & Operational Impact:**
  - Risk Level: **Low**.
  - Operational Impact: Strictly scoped to a dedicated `.tmp` marker file in the temporary directory. No legitimate system files or logs are touched.
- **Rollback Requirements & Cleanup Procedure:**
  - Cleanup Command:
    ```powershell
    if (Test-Path "$env:TEMP\art-file-deletion.tmp") { Remove-Item "$env:TEMP\art-file-deletion.tmp" -Force }
    ```
  - Post-Execution Verification:
    ```powershell
    Test-Path -Path "$env:TEMP\art-file-deletion.tmp" # Must return False
    ```
- **Status:** **APPROVED CANDIDATE** (Planned).
- **Official References:**
  - [MITRE ATT&CK T1070.004](https://attack.mitre.org/techniques/T1070/004/)
  - [Atomic Red Team T1070.004](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1070.004/T1070.004.md)

---

### Test RT-AT-006: Modify Registry: Benign HKCU Test Key

- **Test Name:** Modify Registry: Benign HKCU Test Key
- **Unique Identifier:** `RT-AT-006`
- **MITRE ATT&CK Tactic:** Defense Evasion
- **MITRE ATT&CK Technique ID:** `T1112`
- **Technique Name:** Modify Registry
- **Atomic Red Team Reference:** Test #1 in `T1112.yaml`
- **Atomic Test GUID:** `c27c6242-780c-4395-9654-e461f03ce37c`
- **Target Operating System:** Windows 10/11, Windows Server
- **Prerequisites:**
  - Write access to the current user registry hive (`HKEY_CURRENT_USER`).
- **Test Objective & Expected Behavior:**
  - Creates a dedicated test registry key `HKCU:\Software\AtomicRedTeamTest` and sets a string value `TestKey` = `ExecutionValidation` to validate endpoint registry auditing.
- **Required Permissions & Execution Context:** Standard User (Non-elevated; strictly isolated to `HKCU`).
- **Approved Execution Command:**
  ```powershell
  New-Item -Path "HKCU:\Software\AtomicRedTeamTest" -Force | Out-Null
  Set-ItemProperty -Path "HKCU:\Software\AtomicRedTeamTest" -Name "TestKey" -Value "ExecutionValidation"
  ```
- **Expected Telemetry & Event Sources:**
  - *Sysmon Registry Object Creation:* Sysmon Event ID 12 (`EventType: CreateKey`, `TargetObject: ...\Software\AtomicRedTeamTest`).
  - *Sysmon Registry Value Set:* Sysmon Event ID 13 (`EventType: SetValue`, `TargetObject: ...\TestKey`, `Details: ExecutionValidation`).
  - *Windows Security Audit:* Event ID 4657 (if registry auditing policy enabled for user hive).
- **Expected Outcome & Validation Criteria:**
  - Key and property created successfully without permission error.
  - `(Get-ItemProperty -Path "HKCU:\Software\AtomicRedTeamTest").TestKey` returns `ExecutionValidation`.
- **Risk Level & Operational Impact:**
  - Risk Level: **Low**.
  - Operational Impact: Scoped strictly to an isolated custom registry subkey under `HKCU:\Software`. Does not alter any Windows configuration, security policies, or application behavior.
- **Rollback Requirements & Cleanup Procedure:**
  - Cleanup Command:
    ```powershell
    Remove-Item -Path "HKCU:\Software\AtomicRedTeamTest" -Recurse -Force -ErrorAction SilentlyContinue
    ```
  - Post-Execution Verification:
    ```powershell
    Test-Path -Path "HKCU:\Software\AtomicRedTeamTest" # Must return False
    ```
- **Status:** **APPROVED CANDIDATE** (Planned).
- **Official References:**
  - [MITRE ATT&CK T1112](https://attack.mitre.org/techniques/T1112/)
  - [Atomic Red Team T1112](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1112/T1112.md)

---

### Test RT-AT-007: PowerShell Base64 Encoded Command Execution

- **Test Name:** PowerShell Base64 Encoded Command Execution
- **Unique Identifier:** `RT-AT-007`
- **MITRE ATT&CK Tactic:** Execution
- **MITRE ATT&CK Technique ID:** `T1059.001`
- **Technique Name:** Command and Scripting Interpreter: PowerShell
- **Atomic Red Team Reference:** Test #15 in `T1059.001.yaml`
- **Atomic Test GUID:** `6d8eb875-9ab7-47ee-bb5c-446755ec56bf`
- **Target Operating System:** Windows 10/11, Windows Server
- **Prerequisites:**
  - Windows PowerShell 5.1+ available.
- **Test Objective & Expected Behavior:**
  - Executes a harmless string output command using the base64 `-EncodedCommand` switch (`V3JpdGUtSG9zdCAiSGVsbG8gZnJvbSBBdG9taWMgUmVkIFRlYW0i`) to evaluate whether the defense logging pipeline deobfuscates script blocks and inspects encoded parameters.
- **Required Permissions & Execution Context:** Standard User (Non-elevated).
- **Approved Execution Command:**
  ```powershell
  powershell.exe -NoProfile -NonInteractive -EncodedCommand V3JpdGUtSG9zdCAiSGVsbG8gZnJvbSBBdG9taWMgUmVkIFRlYW0i
  ```
- **Expected Telemetry & Event Sources:**
  - *Process Creation:* Windows Security Event ID 4688 / Sysmon Event ID 1 (`CommandLine: ... -EncodedCommand V3JpdGUtSG9zdCAiSGVsbG8gZnJvbSBBdG9taWMgUmVkIFRlYW0i`).
  - *PowerShell Script Block Logging:* Microsoft-Windows-PowerShell/Operational Event ID 4104 recording the deobfuscated payload: `Write-Host "Hello from Atomic Red Team"`.
- **Expected Outcome & Validation Criteria:**
  - Process exit code `0`.
  - Standard output prints: `Hello from Atomic Red Team`.
- **Risk Level & Operational Impact:**
  - Risk Level: **Low**.
  - Operational Impact: Completely ephemeral in-memory command; no network or disk changes.
- **Rollback Requirements & Cleanup Procedure:**
  - Cleanup Command: None required (process exits immediately).
  - Post-Execution Verification: Verify process termination.
- **Status:** **APPROVED CANDIDATE** (Planned).
- **Official References:**
  - [MITRE ATT&CK T1059.001](https://attack.mitre.org/techniques/T1059/001/)
  - [Atomic Red Team T1059.001](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1059.001/T1059.001.md)

---

### Test RT-AT-008: System Network Configuration Discovery via ipconfig.exe

- **Test Name:** System Network Configuration Discovery via ipconfig.exe
- **Unique Identifier:** `RT-AT-008`
- **MITRE ATT&CK Tactic:** Discovery
- **MITRE ATT&CK Technique ID:** `T1016`
- **Technique Name:** System Network Configuration Discovery
- **Atomic Red Team Reference:** Test #1 in `T1016.yaml`
- **Atomic Test GUID:** `af9908f5-3006-4993-9c86-cb89694ce2ec`
- **Target Operating System:** Windows 10/11, Windows Server
- **Prerequisites:**
  - `%SystemRoot%\System32\ipconfig.exe` available.
- **Test Objective & Expected Behavior:**
  - Simulates network environment discovery enumerating IPv4/IPv6 addresses, subnet masks, default gateways, and DNS servers.
- **Required Permissions & Execution Context:** Standard User (Non-elevated).
- **Approved Execution Command:**
  ```powershell
  ipconfig.exe /all
  ```
- **Expected Telemetry & Event Sources:**
  - *Process Creation:* Windows Security Event ID 4688 (`CommandLine: ipconfig.exe /all`).
  - *Sysmon Process Create:* Sysmon Event ID 1 (`Image: C:\Windows\System32\ipconfig.exe`, `CommandLine: ipconfig.exe /all`).
- **Expected Outcome & Validation Criteria:**
  - Process exit code `0`.
  - Standard output displays network adapter configuration.
- **Risk Level & Operational Impact:**
  - Risk Level: **Very Low**.
  - Operational Impact: Read-only network stack query.
- **Rollback Requirements & Cleanup Procedure:**
  - Cleanup Command: None required.
  - Post-Execution Verification: Verify process termination.
- **Status:** **APPROVED CANDIDATE** (Planned).
- **Official References:**
  - [MITRE ATT&CK T1016](https://attack.mitre.org/techniques/T1016/)
  - [Atomic Red Team T1016](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1016/T1016.md)

---

## 4. Execution Rules & Safety Controls

1. **Authorization Gate:** Testing may only occur against explicitly approved hosts, accounts, and testing windows documented in `docs/redteam/engagement-scope.md`.
2. **Blast-Radius Containment:** All tests in this catalog require only standard user privileges (`Elevation required: No`). Do not run tests under administrative or SYSTEM privileges unless explicitly authorized with a separate safety assessment.
3. **Single-Technique Isolation:** Execute exactly one test at a time. Never execute automated batches or multi-stage chains without intermediate log checks and cleanup validation.
4. **Independent Evidence Validation:** Separate execution success (`PASS` exit code) from event generation, collection, and detection. A successful command execution does not mean defense detection occurred.
5. **No Production Execution:** Never execute atomic tests against production environments or third-party networks.
6. **External Evidence Retention:** Retain raw transcripts, event CSVs, and screenshots outside the Git repository in `C:\Users\alaka\cygrc-security\evidence\redteam\`. Do not commit raw logs containing credentials or PII.
7. **Immediate Stop Condition:** Pause execution immediately if any of the following occur:
   - System instability or service degradation.
   - Unexpected security alerts (such as third-party malware detections outside test scope).
   - Any test leaves residual files that cannot be cleaned up via documented rollback steps.

---

## 5. Workstream Status & Operational Gate

- **RT-AT-001 (Executed):** Execution returned exit code `0` (`PASS`). Temporary file was cleaned up (`PASS`). Targeted event query did not observe test-specific telemetry (`NOT OBSERVED`). Microsoft Defender quarantined unrelated tool artifacts in the adjacent atomic repository.
- **Live Testing Status:** **PAUSED** pending team-lead review of the Defender quarantine findings and formal authorization of dedicated sandbox execution environments.
- **Candidate Tests RT-AT-002 through RT-AT-008:** Curated, fully mapped, and ready for controlled execution once authorization is confirmed.
