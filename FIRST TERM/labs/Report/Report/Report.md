---
Title: "Technical Report: Host Scanning and Vulnerability Analysis"
Project: Lab 03 - Metasploitable 2 Reconnaissance
Subject: IT Security and Privacity
Professor: Daniel Esteban Vela López
Author: Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez
Date: 2026-02-07
Location: Bogotá, Colombia
Confidentiality: Internal / Academic Use Only
---

# TECHNICAL REPORT: HOST SCANNING AND ANALYSIS

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_de_la_Escuela_Colombiana_de_Ingenier%C3%ADa_-_Universidad.webp" width="250">
  <br>
  <strong>Escuela Colombiana de Ingeniería Julio Garavito</strong>
  <br>
  <br>
  <br> <strong>Project:</strong> Lab 03 - Metasploitable 2 Reconnaissance <br> <strong>Subject:</strong> IT Security and Privacity <br> <strong>Professor:</strong> Daniel Esteban Vela López <br> <strong>Authors:</strong> Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez <br> <strong>Date:</strong> 2026-02-10 <br> <strong>Location:</strong> Bogotá, Colombia <br><br> <strong>Confidentiality:</strong> Internal / Academic Use Only
</div>

---

## 1. Introduction
### 1.1 Objective
The primary goal of this analysis is to identify active services, open ports, and potential security vulnerabilities within a controlled virtual environment using Metasploitable 2. This report documents the technical findings to recommend mitigation strategies.

### 1.2 Scope
- **Target System:** Metasploitable 2 (Linux-based vulnerable VM).
- **Environment:** Isolated Host-only virtual network.
- **Attacker Machine:** Kali Linux (192.168.106.128).
- **Target IP:** 192.168.106.129.

### 1.3 Discussion: Structure and Purpose of Technical Reports
*Before the technical execution, we analyzed the "Demo Company - Security Assessment Findings Report" to understand professional documentation standards.*

**Perspective: Andersson David Sánchez Méndez**
> "From my perspective, the most critical aspect of the reference report is its **reproducibility and technical depth**. I noticed that the report isn't just a list of problems; it includes a specific 'Assessment Components' section and a clear 'Finding Severity Rating'. This is vital because, as an engineer, I need to know exactly how a vulnerability was found to verify it. The way they categorize findings by impact (Critical, High, etc.) and include specific 'Action' items ensures that the technical team knows where to start patching without ambiguity."

**Perspective: Cristian Santiago Pedraza Rodríguez**
> "What stands out to me is the **balance between the Executive Summary and the Technical Detail**. The reference report follows the principle that 'if it is not documented, it does not exist,' but it also recognizes that not everyone reading it is a sysadmin. By including a 'Confidentiality Statement' and a 'Scope' section, it sets professional boundaries. I found the 'Security Strengths' section particularly interesting; a good report shouldn't just point out what's broken, but also what security controls are actually working."

## 2. Methodology
### 2.1 Techniques
Description of the reconnaissance approach (Black Box, Passive/Active scanning using Nmap Stealth SYN Scan).

### 2.2 Tools
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| Nmap | 7.9x | Network discovery and service enumeration |
| CherryTree | 0.99.x | Hierarchical note-taking and evidence organization |
| Flameshot | 0.12.x | Annotated screenshot capture |
| OpenSSL | 3.x | SHA256 integrity verification |

## 3. Findings

### 3.1 Network Inventory (Scan Results)
* **Target IP:** `192.168.106.129`
* **Status:** Up / Active
* **Latency:** < 0.00052s
* **Nmap Command used:** `sudo nmap -sS -A -T4 192.168.106.129 -oN nmap_scan.txt`

### 3.2 Vulnerability Table
| Port | Service | Version | Short Description | Severity |
| :--- | :--- | :--- | :--- | :--- |
| 21 | FTP | vsftpd 2.3.4 | Backdoored version (CVE-2011-2523) | **Critical** |
| 22 | SSH | OpenSSH 4.7p1 | Accessible service; outdated version | Medium |
| 23 | Telnet | Linux telnetd | Unencrypted management protocol | **High** |
| 80 | HTTP | Apache 2.2.8 | Hosting vulnerable web applications | **High** |
| 445 | SMB | Samba 3.x | Potential for RCE (SambaCry/EternalRed) | **Critical** |
| 3306 | MySQL | 5.0.51a | Database exposed via network | **High** |


## 3.3 Detailed Findings: Remote Root Compromise via FTP Backdoor

**Summary:**
The target system is running a backdoored version of the FTP service (vsftpd 2.3.4). This vulnerability allows a remote attacker to execute arbitrary commands with **root privileges** without requiring valid credentials.

**Technical Description:**
During the service enumeration phase, Nmap identified `vsftpd version 2.3.4` on port 21/tcp. This specific version, released in 2011, was compromised at the source level to include a malicious backdoor (identified as **CVE-2011-2523**). 

The vulnerability is triggered when a user attempts to log in with a username that contains a smiley face `:)`. This action causes the service to open a listener on port **6200/tcp**, providing an unauthenticated root shell.

**Attached Evidence:**
- **Primary Evidence:** `nmap_scan.txt` (Hash SHA256 verified in section 4.2).
- **Screenshots:** 
![[nmap-kali-to-metasploitable-part1.png]]
*Figure 1: Detailed Nmap scan results identifying critical service versions part 1 .*
![[nmap-kali-to-metasploitable-part2.png]]
*Figure 2: Detailed Nmap scan results identifying critical service versions part 2.*
![[nmap-kali-to-metasploitable-part3.png]]
*Figure 3: Detailed Nmap scan results identifying critical service versions part 3.*

**Recommendations:**
1. **Service Deactivation:** Immediately stop and disable the `vsftpd` service if FTP is not a business requirement.
2. **Patch Management:** Update the FTP server to a secure version (e.g., `vsftpd 3.0.x` or higher).
3. **Secure Alternatives:** Implement SFTP (SSH File Transfer Protocol) over port 22.

## 4. Evidence Analysis

### 4.1 Connectivity and Verification
Before scanning, a connectivity test and interface verification were performed.

**Capture 1: Interface Configuration**
![[ifconfig-kalilinux.png]]
![[ifconfig-metasploitable.png]]
*Analysis: Verification of Attacker (192.168.106.128) and Target (192.168.106.129) network visibility.*

**Capture 2: Connectivity Test (Ping)**
![[ping-kali-to-metasploitable.png]]
![[ping-metasploitable-to-kali.png]]
*Analysis: Successful ICMP Echo Request confirming a stable connection to the target and attacker VM.*

### 4.2 Evidence Integrity (Hashes)
To ensure the integrity of the generated data, a SHA256 hash was calculated for the primary scan output.

**Capture 3: SHA256 Integrity Verification**
![[sha256sum-nmap_scan-file.png]]

| File Name | SHA256 Hash |
| :--- | :--- |
| `nmap_scan.txt` | `37804470200e008a687397e59670087702868019665557760773099908126830` |

> **Note:** Any modification to the `nmap_scan.txt` file will result in a different hash, ensuring the authenticity of this report.

## 5. Conclusions
The Metasploitable 2 host presents a **highly insecure posture**. The presence of multiple legacy services and "Backdoored" software indicates that the system is easily exploitable with automated tools. The lack of encryption on management ports (Telnet) further increases the risk of credential theft.

## 6. Recommendations
1. **Disable Legacy Protocols:** Immediately shut down Port 23 (Telnet) and Port 21 (FTP).
2. **Implement Encryption:** Replace Telnet with SSH (Port 22) and FTP with SFTP.
3. **Patching:** Update the OS and all service versions (Apache, Samba, MySQL).
<br>
<br>
## 7. Appendices
### 7.1 Full Nmap Output
*(Refer to the attached `nmap_scan.txt` for the complete list of scripts).*

## 8. References
- CVE-2011-2523: vsftpd 2.3.4 Backdoor.
- Nmap Documentation: https://nmap.org/book/man.html

---
## Personal Reflection

**Andersson David Sánchez Méndez:**
"In this lab, I learned that professional reporting is just as important as the technical execution. By implementing SHA256 hashes, we guarantee that our evidence remains untampered, which is a standard requirement in real-world audits. Identifying the vsftpd 2.3.4 backdoor reminded me that a single outdated service can compromise an entire infrastructure, regardless of other security layers."

**Cristian Santiago Pedraza Rodríguez:**
"The transition from raw data to a structured report taught me how to categorize risks effectively. Using CherryTree for internal notes and Obsidian for the final delivery allowed us to maintain reproducibility. I now understand that a technical report must provide clear evidence for sysadmins while maintaining an objective tone that accurately represents the business risk found during the scanning phase."

---