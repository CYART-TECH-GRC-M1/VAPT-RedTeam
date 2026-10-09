# MITRE ATT&CK Technique Mapping & Detection Validation

**Project:** CyGRC Module 2 — VAPT & Red Team  
**Workstream:** Atomic Red Team & Technique Execution  
**Branch:** `feature/redteam-atomic`  
**Mapping Status:** Baseline Complete — Aligned with MITRE ATT&CK v14+  

---

## 1. Purpose & Overview

This document provides a rigorous, traceable mapping between the curated CyGRC Atomic Red Team catalog tests and the MITRE ATT&CK framework. It establishes the technical criteria required to determine whether adversarial actions produce endpoint telemetry and whether security controls effectively detect those behaviors.

A fundamental tenet of this workstream is that **successful execution does not equal defensive detection**. A technique may execute with exit code `0` while remaining completely invisible to defenders due to unconfigured audit policies, missing event collectors, or overly restrictive SIEM filters.

---

## 2. MITRE ATT&CK Matrix Alignment

| Tactic | Technique ID | Technique Name | Sub-Technique | Test ID | Data Sources |
|---|---|---|---|---|---|
| **Execution** | `T1059.001` | Command and Scripting Interpreter | PowerShell | RT-AT-001 | Command Execution, Script Execution, Process Creation |
| **Discovery** | `T1082` | System Information Discovery | — | RT-AT-002 | Process Creation, OS API / WMI Execution |
| **Discovery** | `T1033` | System Owner/User Discovery | — | RT-AT-003 | Process Creation, Command Execution |
| **Discovery** | `T1057` | Process Discovery | — | RT-AT-004 | Process Creation, Process Access |
| **Defense Evasion** | `T1070.004` | Indicator Removal | File Deletion | RT-AT-005 | File Deletion, File Creation |
| **Defense Evasion** | `T1112` | Modify Registry | — | RT-AT-006 | Windows Registry Modification |
| **Execution** | `T1059.001` | Command and Scripting Interpreter | PowerShell | RT-AT-007 | Script Execution, Process Creation |
| **Discovery** | `T1016` | System Network Configuration Discovery | — | RT-AT-008 | Process Creation, Command Execution |
| **Defense Evasion** | `T1564.004` | Hide Artifacts | NTFS File Attributes | RT-AT-001 | File Modification, Alternate Data Stream Creation |

---

## 3. Comprehensive Technique Mapping & Detection Specifications

### RT-AT-001: NTFS Alternate Data Stream Access (`T1059.001` / `T1564.004`)

- **Tactic:** Execution / Defense Evasion
- **Technique ID & Name:** `T1059.001` (PowerShell) / `T1564.004` (NTFS File Attributes)
- **Simulated Adversary Behavior:** Storing executable PowerShell script blocks inside an NTFS Alternate Data Stream (`NTFS_ADS.txt:streamCommand`) and executing the contents via `Invoke-Expression` without creating a standalone `.ps1` script file on disk.
- **Relevance to CyGRC:** Evaluates whether file integrity and script logging controls can detect execution of hidden payloads designed to bypass standard directory-based file extension filters.
- **Target Telemetry Sources:**
  - `Microsoft-Windows-PowerShell/Operational` (Event ID 4104 — Script Block Logging)
  - `Microsoft-Windows-Sysmon/Operational` (Event ID 15 — FileCreateStreamHash)
  - `Microsoft-Windows-Sysmon/Operational` (Event ID 1 — Process Create)
  - `Security` (Event ID 4688 — Process Creation with command-line auditing)
- **Expected Detection Rules:**
  - *Sigma Rule Concept:* `proc_creation_win_powershell_ads_exec` or `posh_ps_alternate_data_stream`
  - *Detection Logic:* PowerShell script block or command-line matching regex `.*Add-Content.*-Stream.*` or `Get-Content.*-Stream.*` followed by `Invoke-Expression` / `iex`.
- **Actual Telemetry Results (Observed):**
  - **Execution:** PASS (Exit code 0, standard output: `Stream Data Executed`).
  - **Event Generation/Collection:** PARTIAL (42 total PowerShell events captured during test window 2026-10-09 20:28:22–20:29:26).
  - **Targeted Query Result:** **NOT OBSERVED** (Zero records matched targeted keywords `NTFS_ADS`, `streamCommand`, `Invoke-Expression` in the exported log slice).
  - **Detection Status:** **INCOMPLETE / NOT CONFIRMED**.
- **Root Cause & Detection Gaps:**
  - PowerShell Script Block Logging (Event 4104) was not configured for *Verbose* / *All script blocks* in local Group Policy, meaning short interactive commands were not captured.
  - Sysmon Event ID 15 was not configured or running on the test host to capture alternate data stream hashes.
- **Defensive Engineering Recommendations:**
  - Enable Group Policy: `Computer Configuration -> Administrative Templates -> Windows Components -> Windows PowerShell -> Turn on PowerShell Script Block Logging`.
  - Deploy Sysmon with configuration capturing stream writes (`<FileCreateStreamHash onmatch="include" />`).

---

### RT-AT-002: System Information Discovery (`T1082`)

- **Tactic:** Discovery
- **Technique ID & Name:** `T1082` — System Information Discovery
- **Simulated Adversary Behavior:** Execution of native Windows discovery utility `systeminfo.exe` to gather OS version, patch status, hardware architecture, and domain configuration.
- **Relevance to CyGRC:** Assesses detection of early-stage discovery activity performed by adversaries to prepare targeted privilege escalation exploits or malware builds.
- **Target Telemetry Sources:**
  - `Security` (Event ID 4688 — Process Creation)
  - `Microsoft-Windows-Sysmon/Operational` (Event ID 1 — Process Create)
- **Expected Detection Logic:**
  - *Sigma Rule:* `proc_creation_win_systeminfo_execution`
  - *Query Logic (Splunk / Sentinel):*
    ```sql
    EventCode=4688 (NewProcessName="*\\systeminfo.exe" OR CommandLine="*systeminfo*")
    ```
- **Validation Criteria:**
  - Execution exit code 0.
  - Event 4688 or Sysmon Event 1 captures process image `systeminfo.exe` and parent process `powershell.exe`.
- **Detection Status:** APPROVED CANDIDATE — Telemetry model verified, pending execution.
- **Defensive Recommendations:**
  - Enable GPO: `Administrative Templates -> System -> Audit Process Creation -> Include command line in process creation events`.
  - Implement behavioral analytics correlating discovery tools (`systeminfo`, `whoami`, `tasklist`) executed within short time windows (reconnaissance bursts).

---

### RT-AT-003: System Owner/User Discovery (`T1033`)

- **Tactic:** Discovery
- **Technique ID & Name:** `T1033` — System Owner/User Discovery
- **Simulated Adversary Behavior:** Invoking `whoami.exe /all` to enumerate current security token, username, group memberships, and assigned privileges.
- **Relevance to CyGRC:** Simulates immediate post-initial-access reconnaissance common in almost all compromise chains.
- **Target Telemetry Sources:**
  - `Security` (Event ID 4688 — Process Creation)
  - `Microsoft-Windows-Sysmon/Operational` (Event ID 1 — Process Create)
- **Expected Detection Logic:**
  - *Sigma Rule:* `proc_creation_win_whoami_execution`
  - *Query Logic:*
    ```sql
    Image="*\\whoami.exe" AND CommandLine="* /all*"
    ```
- **Validation Criteria:**
  - Event captures full command line `whoami.exe /all`.
- **Detection Status:** APPROVED CANDIDATE — Telemetry model verified.
- **Defensive Recommendations:**
  - Alert on non-interactive service accounts or web server accounts (e.g., `DefaultAppPool`, `cygrc-backend`) executing `whoami.exe`.

---

### RT-AT-004: Process Discovery (`T1057`)

- **Tactic:** Discovery
- **Technique ID & Name:** `T1057` — Process Discovery
- **Simulated Adversary Behavior:** Running `tasklist.exe /v` to enumerate all running tasks, process IDs, and memory utilization to identify security monitoring tools and endpoint agents.
- **Relevance to CyGRC:** Identifies whether the defensive stack alerts when an attacker maps running defense agents.
- **Target Telemetry Sources:**
  - `Security` (Event ID 4688)
  - `Sysmon` (Event ID 1)
- **Expected Detection Logic:**
  - *Sigma Rule:* `proc_creation_win_tasklist_execution`
  - *Query Logic:*
    ```sql
    Image="*\\tasklist.exe"
    ```
- **Detection Status:** APPROVED CANDIDATE — Telemetry model verified.
- **Defensive Recommendations:**
  - Monitor process reconnaissance command bursts executed from interactive consoles.

---

### RT-AT-005: Indicator Removal: Benign File Deletion (`T1070.004`)

- **Tactic:** Defense Evasion
- **Technique ID & Name:** `T1070.004` — Indicator Removal: File Deletion
- **Simulated Adversary Behavior:** Creating and immediately removing a marker file in `$env:TEMP\art-file-deletion.tmp` using PowerShell `Remove-Item`.
- **Relevance to CyGRC:** Assesses file integrity monitoring and anti-forensics detection capabilities.
- **Target Telemetry Sources:**
  - `Microsoft-Windows-Sysmon/Operational` (Event ID 11 — FileCreate)
  - `Microsoft-Windows-Sysmon/Operational` (Event ID 23 — FileDelete)
  - `Microsoft-Windows-PowerShell/Operational` (Event ID 4104)
- **Expected Detection Logic:**
  - *Sysmon Query:*
    ```xml
    <QueryList>
      <Query Id="0" Path="Microsoft-Windows-Sysmon/Operational">
        <Select Path="Microsoft-Windows-Sysmon/Operational">*[System[(EventID=11 or EventID=23)]] and *[EventData[Data[@Name='TargetFilename'] and (contains(., 'art-file-deletion.tmp'))]]</Select>
      </Query>
    </QueryList>
    ```
- **Detection Status:** APPROVED CANDIDATE — Telemetry model verified.
- **Defensive Recommendations:**
  - Ensure Sysmon Event ID 23 (FileDelete) archiving is enabled for temporary and user profile directories to preserve deleted attacker artifacts for forensic recovery.

---

### RT-AT-006: Modify Registry: Benign HKCU Test Key (`T1112`)

- **Tactic:** Defense Evasion
- **Technique ID & Name:** `T1112` — Modify Registry
- **Simulated Adversary Behavior:** Creating registry key `HKCU:\Software\AtomicRedTeamTest` and value `TestKey` to simulate registry tampering and configuration persistence.
- **Relevance to CyGRC:** Tests registry telemetry auditing without risk to system stability.
- **Target Telemetry Sources:**
  - `Microsoft-Windows-Sysmon/Operational` (Event ID 12 — Registry CreateKey / DeleteKey)
  - `Microsoft-Windows-Sysmon/Operational` (Event ID 13 — Registry SetValue)
  - `Security` (Event ID 4657 — Registry Value Modified)
- **Expected Detection Logic:**
  - *Sysmon Event ID 12/13:*
    ```sql
    EventCode in (12, 13) AND TargetObject="*\\Software\\AtomicRedTeamTest*"
    ```
- **Detection Status:** APPROVED CANDIDATE — Telemetry model verified.
- **Defensive Recommendations:**
  - Enable registry auditing on sensitive persistence keys (e.g., Run/RunOnce, Services, Terminal Server).

---

### RT-AT-007: PowerShell Base64 Encoded Command Execution (`T1059.001`)

- **Tactic:** Execution
- **Technique ID & Name:** `T1059.001` — Command and Scripting Interpreter: PowerShell
- **Simulated Adversary Behavior:** Invoking `powershell.exe` with `-EncodedCommand` passing base64 payload `V3JpdGUtSG9zdCAiSGVsbG8gZnJvbSBBdG9taWMgUmVkIFRlYW0i`.
- **Relevance to CyGRC:** Validates whether logging solutions deobfuscate base64 strings and alert on suspicious script parameter flags.
- **Target Telemetry Sources:**
  - `Security` (Event ID 4688) / `Sysmon` (Event ID 1) capturing `-EncodedCommand`
  - `Microsoft-Windows-PowerShell/Operational` (Event ID 4104) capturing the decoded script block: `Write-Host "Hello from Atomic Red Team"`.
- **Expected Detection Logic:**
  - *Sigma Rule:* `proc_creation_win_powershell_encoded_cmd`
  - *Detection Query:*
    ```sql
    CommandLine="* -EncodedCommand *" OR CommandLine="* -enc *"
    ```
- **Detection Status:** APPROVED CANDIDATE — Telemetry model verified.
- **Defensive Recommendations:**
  - Alert on PowerShell processes launched with `-EncodedCommand`, `-WindowStyle Hidden`, or `-ExecutionPolicy Bypass`.

---

### RT-AT-008: System Network Configuration Discovery (`T1016`)

- **Tactic:** Discovery
- **Technique ID & Name:** `T1016` — System Network Configuration Discovery
- **Simulated Adversary Behavior:** Executing `ipconfig.exe /all` to discover network adapter settings, DHCP servers, and DNS resolvers.
- **Relevance to CyGRC:** Assesses detection of network topology discovery.
- **Target Telemetry Sources:**
  - `Security` (Event ID 4688)
  - `Sysmon` (Event ID 1)
- **Expected Detection Logic:**
  - *Sigma Rule:* `proc_creation_win_ipconfig_execution`
  - *Detection Query:*
    ```sql
    Image="*\\ipconfig.exe" AND CommandLine="* /all*"
    ```
- **Detection Status:** APPROVED CANDIDATE — Telemetry model verified.

---

## 4. Analysis of Microsoft Defender Findings During RT-AT-001

During the execution of RT-AT-001 on 2026-10-09 between 20:28:22 and 20:29:26, Microsoft Defender generated the following alerts in `Microsoft-Windows-Windows Defender/Operational`:

| Event ID | Timestamp | Threat Name | Resource Detected | Remediation Action |
|---|---|---|---|---|
| 1116 / 1117 | 20:28:35 / 20:29:13 | `Trojan:Script/Wacatac.H!ml` | `T1059.001\src\Invoke-DownloadCradle.ps1` | Quarantined |
| 1116 / 1117 | 20:28:35 / 20:29:13 | `VirTool:MSIL/SoapHound!rfn` | `T1059.001\bin\SOAPHound.exe` | Quarantined |

### Forensic Analysis & Causation Evaluation:
1. **File Separation:** The commands executed for RT-AT-001 strictly involved `$env:TEMP\NTFS_ADS.txt` and PowerShell alternate stream `streamCommand`. They never invoked, read, or loaded `Invoke-DownloadCradle.ps1` or `SOAPHound.exe`.
2. **Scanner Trigger:** Microsoft Defender's real-time file-system inspection was triggered by disk reads occurring within the cloned upstream Atomic repository folder `C:\AtomicRedTeam\atomic-red-team\atomics\T1059.001\`.
3. **Detection Validity:** These Defender detections represent **static signature detections of inactive files on disk**, not behavioral detections of the NTFS alternate data stream execution.
4. **Engineering Conclusion:** These detections **must not be recorded as successful detection of RT-AT-001**.
5. **Operational Action:** Live execution remains paused until the team lead reviews these findings and dedicated isolated lab environments are provisioned.

---

## 5. Defensive Engineering Recommendations Summary

1. **PowerShell Script Block Logging:** Force-enable Windows Event ID 4104 script block logging across all endpoints to capture dynamic script execution regardless of file obfuscation.
2. **Command-Line Process Auditing:** Configure Group Policy to include complete process command lines in Security Event 4688 logs.
3. **Sysmon Integration:** Standardize on an enterprise Sysmon configuration (e.g., SwiftOnSecurity or Olaf Hartong modular config) to provide high-fidelity logging for FileCreateStreamHash (Event 15), FileDelete (Event 23), and Registry events (Events 12 & 13).
4. **Distinguish Static vs. Behavioral Detections:** Security operations teams must not rely solely on AV signature alerts; behavioral detections for reconnaissance commands and script execution are critical for catching living-off-the-land techniques.
