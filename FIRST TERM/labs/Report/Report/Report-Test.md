---
Title: "Technical Quiz: Report Analysis and Evidence"
Project: Lab 03 - Metasploitable 2 Reconnaissance
Subject: IT Security and Privacity
Professor: Daniel Esteban Vela López
Author: Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez
Date: 2026-02-10
Location: Bogotá, Colombia
Confidentiality: Internal / Academic Use Only
---

# TEST YOURSELF: TECHNICAL REPORTING AND EVIDENCE ANALYSIS

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_de_la_Escuela_Colombiana_de_Ingenier%C3%ADa_-_Universidad.webp" width="250">
  <br>
  <strong>Escuela Colombiana de Ingeniería Julio Garavito</strong>
  <br>
  <br>
  <strong>Project:</strong> Lab 03 - Metasploitable 2 Reconnaissance <br> 
  <strong>Subject:</strong> IT Security and Privacity <br> 
  <strong>Professor:</strong> Daniel Esteban Vela López <br> 
  <strong>Authors:</strong> Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez <br> 
  <strong>Date:</strong> 2026-02-10 <br> 
  <strong>Location:</strong> Bogotá, Colombia <br><br> 
  <strong>Confidentiality:</strong> Internal / Academic Use Only
</div>

---

## 1. Structure: Report Sections and Differences

### 1.1 Essential Sections in a Pentest Technical Report
A professional technical report must contain, at a minimum, the following sections to be actionable:
- **Executive Summary:** A high-level overview for management.
- **Scope & Methodology:** Testing boundaries and techniques used.
- **Vulnerability Summary Table:** A quick inventory of findings categorized by severity.
- **Detailed Findings:** Technical description, reproduction steps, impact, and evidence for each vulnerability.
- **Remediation & Recommendations:** Specific steps to mitigate the identified risks.
- **Appendices/Logs:** Raw tool outputs (e.g., Nmap scans) that support the analysis.



### 1.2 Difference: Technical vs. Executive Report
The key difference lies in the **audience and purpose**:
- **Executive Report:** Designed for strategic decision-making. It avoids excessive technical jargon and focuses on **business risk**, the budget required for fixes, and the impact on operational continuity.
- **Technical Report:** Designed for system administrators and developers. It focuses on the **"how"**, providing exact commands, software versions, traffic captures, and precise details that allow the IT team to replicate and patch the vulnerability.

---

## 2. Evidence: Integrity and Verification

### 2.1 Importance of SHA256 Hashing
Calculating the SHA256 hash is vital to ensure **evidence integrity** and **non-repudiation**. In a forensic or legal audit context, the hash acts as a unique digital fingerprint. If a client or third party questions the veracity of the data, the hash proves that the file presented is exactly the same as the one generated during the test.

### 2.2 Consequences of Altered Evidence
If the evidence were altered (even by a single bit), the SHA256 hash would change drastically. This would result in:
1. **Loss of Credibility:** The report would lose all professional validity before a client or a court of law.
2. **Technical Inaccuracy:** Recommendations could be based on false data, leading to ineffective remediations.
3. **Legal Issues:** In compliance audits (such as PCI-DSS), altering logs or reports can lead to severe penalties and legal liabilities.
<br>
<br>
<br>

---

## 3. Practice: Finding Entry - Port 21 (Anonymous FTP)

### Finding: Unrestricted Anonymous FTP Access

**Summary:**
The FTP service allows users to log in with the "anonymous" account without providing a password. This configuration permits unauthenticated users to browse or potentially upload/download files from the server.

**Technical Description:**
During the scanning phase, the Nmap script `ftp-anon` detected that the FTP service on port 21 permits anonymous logins. This is often caused by a misconfiguration in the `vsftpd.conf` file (specifically the parameter `anonymous_enable=YES`). 

**Impact:**
- **Information Disclosure:** Attackers can steal sensitive data hosted on the FTP share.
- **Service Enumeration:** Attackers gain insights into the file structure.
- **Note on Write Permissions:** Manual testing confirmed that while read access is granted, write permissions are restricted, mitigating the risk of unauthorized file uploads.

**Attached Evidence:**

**Capture 1: Vulnerability Detection**
![[nmap-anonymous-access.png]]
*Figure 1: Nmap output confirming that the service vsFTPd 2.3.4 allows anonymous login (Code 230).*

**Capture 2: Successful Exploitation (Information Disclosure)**
![[ftp-successful-login-ls.png]]
*Figure 2: Manual connection from Kali Linux using 'anonymous' credentials, providing a full directory listing (ls).*

**Capture 3: Write Permission Test (Impact Analysis)**
![[ftp-error-message-risk.png]]
*Figure 3: Attempting to upload a file (put) and create a directory (mkdir). The 'Permission denied' errors confirm that the impact is limited to unauthorized data access.*

**Capture 4: Connection Status**
![[ftp-status.png]]
*Figure 4: Detailed connection status showing the 'tnftp' client configuration and active session parameters.*

**Recommendation:**
1. **Disable Anonymous Login:** Set `anonymous_enable=NO` in the FTP configuration.
2. **Implement Secure Protocols:** Transition from FTP to SFTP (Port 22) for encrypted transfers.

---