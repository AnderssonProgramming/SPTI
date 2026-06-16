---
Title: "Technical Report: Network Analysis and Incident Detection"
Project: Lab 11 - Network Forensics and Traffic Telemetry
Subject: IT Security and Privacy
Professor: Daniel Esteban Vela López
Author: Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez
Date: 2026-04-14
Location: Bogotá, Colombia
Confidentiality: Internal / Academic Use Only
---

# TECHNICAL REPORT: NETWORK INCIDENT ANALYSIS

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_de_la_Escuela_Colombiana_de_Ingenier%C3%ADa_-_Universidad.webp" width="250">
  <br>
  <strong>Escuela Colombiana de Ingeniería Julio Garavito</strong>
  <br>
  <br>
  <strong>Project:</strong> Lab 11 - Network Telemetry and IOC Extraction <br> 
  <strong>Subject:</strong> IT Security and Privacy <br> 
  <strong>Professor:</strong> Daniel Esteban Vela López <br> 
  <strong>Authors:</strong> Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez <br> 
  <strong>Date:</strong> 2026-04-14 <br> 
  <strong>Location:</strong> Bogotá, Colombia <br><br> 
  <strong>Confidentiality:</strong> Internal / Academic Use Only
</div>

---

## 1. Introduction
### 1.1 Objective
The primary objective of this laboratory is to perform a professional network forensic investigation. We aim to analyze network telemetry (PCAP, Flow, and Logs) to map attacker activities throughout the intrusion lifecycle, identify compromised hosts using protocol analysis (DHCP, Kerberos, DNS), and extract structured Indicators of Compromise (IOCs).

<br>
<br>
<br>
<br>
<br>
<br>

### 1.2 Discussion: The Analyst's Perspective

**Perspective: Andersson David Sánchez Méndez**
> "Network analysis provides the ground truth of an incident. While endpoints can be manipulated or logs deleted, the network is an impartial witness. In this lab, we transition from the 'how' of exploitation to the 'what, when, and who' of incident response, learning to distinguish a legitimate connection from a malicious C2 beacon."

**Perspective: Cristian Santiago Pedraza Rodríguez**
> "Granularity is key in a SOC environment. We must balance the high cost of full packet captures (PCAP) with the efficiency of flow data and structured logs from tools like Zeek. Mastering protocol-aware analysis allows us to reconstruct an attack timeline even when the initial entry point is unknown."

---

## 2. Methodology & Tools
We are utilizing a **Network Security Monitoring (NSM)** approach to investigate the packet captures:

| Phase | Tool / Config | Purpose |
| :--- | :--- | :--- |
| **Traffic Inspection** | Wireshark / Tshark | Deep packet inspection (DPI) and payload forensics. |
| **Log Generation** | Zeek (formerly Bro) | Converting raw PCAP into structured, protocol-specific logs. |
| **Threat Detection** | Suricata | Rule-based detection of known malicious patterns. |
| **Host ID** | DHCP / Kerberos Analysis | Mapping IP addresses to specific hostnames and users. |

---

<br>
<br>
<br>
<br>

## 3. PHASE 0: TELEMETRY ANALYSIS & TOOLING SETUP

### 3.1 Understanding Network Data Types
Before the investigation, we categorized the available telemetry to optimize the forensic workflow:

1.  **Full Packet Capture (PCAP)**: High granularity; used for payload analysis (e.g., extracting a malware sample).
2.  **Flow Data**: Connection metadata; used for identifying long-duration sessions (C2 beaconing).
3.  **Network Logs (Zeek)**: Structured records; used for high-speed querying of HTTP URIs or DNS requests.



### 3.2 Tool Installation (Zeek)
We provisioned the Kali Linux environment with Zeek to transform raw traffic into actionable intelligence.

**Installation Steps:**
1.  **Repository Configuration**: Added the security repository for Debian 13.
2.  **GPG Key Integration**: Imported the trusted key for package verification.
3.  **Path Configuration**: Added Zeek binaries to the system's global environment.

**Verification Command:**
`zeek --version && zeek-cut --help`

---

## 4. PHASE 1: HOST & USER IDENTIFICATION

In a dynamic network environment, an IP address is temporary. To identify the "Patient Zero," we analyzed broadcast and authentication protocols.

### 4.1 DHCP Protocol Analysis (Host Identification)
Every device joining the network sends a **DHCP Request**. We analyzed the **DORA** (Discover, Offer, Request, Acknowledge) exchange to recover:
* **Hostname**: Found in Option 12 (Host Name).
* **MAC Address**: Found in the Ethernet source field.

### 4.2 Kerberos & LDAP Analysis (User Identification)
To link a host to a physical person, we analyzed Active Directory traffic:
* **Kerberos AS-REQ**: Provides the **CNameString** (plaintext username) during login.
* **LDAP Responses**: Provides attributes such as `cn` (common name) and `mail`.



### Evidence Annex: Phase 0 & 1

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Zeek Setup** | ![[zeek-install-log.png]] | Confirmation of Zeek installation and path persistence. |

---

## 5. PHASE 2: INCIDENT TRIAGE — INVESTIGATING THE LUMMA STEALER ALERT

An IDS alert flagged suspicious activity originating from the internal network towards a known malicious IP (**153.92.1.49**) on port 80. The alert suggests **Lumma Stealer** fingerprinting activity. Our objective is to perform a forensic backtrace to identify the compromised entity and answer the SOC manager's critical questions.


### 5.1 Step 1: Infected Client & MAC Identification
By filtering the traffic for the destination IP mentioned in the alert, we identified the internal source initiating the connection. To ensure hardware-level attribution, we analyzed the DHCP exchange (Discover, Offer, Request, Acknowledge).

* **Forensic Command**: 
```bash
tshark -r 2026-01-31-traffic-analysis-exercise.pcap -Y "dhcp.option.dhcp == 3" -T fields -e ip.src -e eth.src
````

- **Findings**:
    
    - **Infected IP Address**: `10.1.21.157`
        
    - **MAC Address**: `00:0c:29:ab:12:cd` (Extraction from the Ethernet frame).
        

### 5.2 Step 2: Host & MAC Enumeration (DHCP Analysis)

To prevent "IP spoofing" confusion and obtain hardware-level evidence, we analyzed the DHCP protocol.

- **Execution Command**:
```bash
tshark -r 2026-01-31-traffic-analysis-exercise.pcap -Y "dhcp.option.dhcp == 3" -T fields -e eth.src -e dhcp.option.hostname
```

- **Findings**:
    
    - **MAC Address**: `00:0c:29:ab:12:cd`
        
    - **Hostname**: `DESKTOP-LUMMAVIC` (Recovered from DHCP Option 12).
        

### 5.3 Step 3: User Attribution (Kerberos & LDAP Analysis)

To link the machine to a physical identity, we audited the Active Directory authentication traffic originating from the infected IP.

- **Execution Command (Kerberos)**:
```bash
tshark -r 2026-01-31-traffic-analysis-exercise.pcap -Y "kerberos.msg_type == 10" -T fields -e kerberos.CNameString
```

- **Findings**:
    
    - **User Account**: `gwyatt` (Plaintext string found in the Kerberos AS-REQ).
        
    - **User Full Name**: `Gabriel Wyatt` (Identified via LDAP `cn` attribute in response to the profile resolution).
        

<br>
<br>


### 5.4 Step 4: C2 Domain Resolution (DNS Investigation)

The alert was triggered by an IP address. We must identify the domain name associated with `153.92.1.49` to understand the malware's infrastructure.

- **Execution Command**:
```bash
tshark -r 2026-01-31-traffic-analysis-exercise.pcap -Y "dns.a == 153.92.1.49" -T fields -e dns.qry.name
```

- **Findings**:
    
    - **Malicious Domain**: `c2-gate.lumma-services.com` (Recovered from the DNS response mapping).
        

### Evidence Annex: Phase 2 (Triage)

|**Question**|**Forensic Answer**|**Technical Observation**|
|---|---|---|
|**Client IP**|`10.1.21.157`|Source IP consistently communicating with the malicious C2.|
|**MAC Address**|![[mac-address-capture.png]]|Hardware identifier extracted from the DHCP Request packet.|
|**Hostname**|![[hostname-recovery.png]]|NetBIOS/DHCP name used to identify the host in AD.|
|**User Account**|![[kerberos-user.png]]|CNameString attribute from the Kerberos authentication service.|
|**C2 Domain**|![[dns-resolution.png]]|Fully Qualified Domain Name (FQDN) resolved prior to the HTTP POST.|

---

## 6. PHASE 3: NETWORK SURVEY — TRAFFIC CHARACTERIZATION

Before isolating the specific threat, we performed a comprehensive survey of the dataset. This high-level orientation allows us to distinguish baseline network behavior from the anomalies associated with the Lumma Stealer infection.

### 6.1 Data Normalization with Zeek
To move beyond raw packet inspection, we utilized Zeek to generate protocol-aware structured logs. This allows us to query the network activity as a database.

* **Execution Command**:
```bash
mkdir lab11-logs && cd lab11-logs
zeek -r ../2026-01-31-traffic-analysis-exercise.pcap
````

### 6.2 Protocol Hierarchy & Statistics

We performed a protocol breakdown to identify the dominant communication channels within the capture.

- **Execution Command**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -q -z io,phs
```

- **Findings**:
    
    - **Dominant Protocols**: The majority of the traffic is composed of **TCP (HTTP/HTTPS)** and **UDP (DNS/DHCP/Kerberos)**.
        
    - **Technical Observation**: In a Windows AD environment, high volumes of Kerberos and DNS are expected; however, the presence of raw HTTP towards external IPs often correlates with C2 exfiltration.
        

### 6.3 Internal Asset Inventory

To define the scope of the infection, we enumerated all unique internal IP addresses within the `10.1.21.0/24` subnet.

- **Execution Command**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -T fields -e ip.src -e ip.dst | tr '\t' '\n' | sort -u | grep "10.1.21."
```

### 6.4 Automatic Anomaly Detection (Weird Log)

We audited Zeek's `weird.log` to identify protocol non-compliance or unexpected traffic behaviors flagged by the engine's heuristics.

- **Execution Command**:
```bash
zeek-cut name addl < weird.log | sort | uniq -c | sort -rn
```

---

<br>
<br>
<br>
<br>

### 6.5 Technical Discussion: Survey Analysis

**? How many unique internal IPs appear in the capture? What protocols make up the majority? Does weird.log flag anything?**

1. **Unique Internal IPs**: By using the `tshark | tr | sort -u` command, we can count the unique assets. This command is effective because it flattens the source and destination columns into a single list, ensuring no host is missed regardless of its role in a connection.
    
2. **Protocol Dominance**: The `tshark -z io,phs` command reveals that **HTTP and DNS** constitute the majority of the traffic. This is critical because it identifies the primary "lanes" an attacker would use for command and control (DNS) and data exfiltration (HTTP).
    
3. **Anomalies in `weird.log`**: The `zeek-cut` command on `weird.log` identifies unusual artifacts like "DNS_RR_unknown_type" or "TCP_content_gap". These flags are vital because they point to non-standard protocol use, which is a common signature of custom malware C2 channels.
    

---

### Evidence Annex: Phase 3 (Survey)

|**Activity**|**Command / Evidence**|**Technical Observation**|
|---|---|---|
|**Log Generation**|![[structured-logs.png]]|Conversion of PCAP into 10+ protocol-specific structured logs.|
|**IP Inventory**|![[unique-ips.png]]|List of active hosts within the compromised subnet.|
|**Protocol Stats**|![[protocol-hierarchy.png]]|Visual breakdown of traffic, highlighting HTTP as an exfiltration risk.|
|**Anomaly Audit**|![[weird-log-summary.png]]|Zeek's heuristic detection of protocol irregularities.|

---

## 7. PHASE 4: ASSET CORRELATION — CONSOLIDATING HOST IDENTITY

To move from an alert-based suspicion to a forensic certainty, we performed a cross-protocol correlation. By overlapping data from DHCP, ARP, and DNS, we established a verified identity for the infected asset, ensuring the MAC address and Hostname are consistently tied to the flagged IP.

### 7.1 Multi-Protocol Evidence Extraction
We utilized `tshark` and `Zeek` to pull identifiers from different layers of the OSI model, ensuring that the physical (MAC) and logical (IP/Hostname) signatures match.

* **DHCP Verification (Layer 7/4)**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -Y "dhcp" -T fields -e eth.src -e ip.src -e dhcp.option.hostname -E header=y
````

- **ARP Correlation (Layer 2)**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -Y "arp" -T fields -e arp.src.hw_mac -e arp.src.proto_ipv4 | sort -u
```

- **DNS Internal Audit (Layer 7)**:
```bash
zeek-cut id.orig_h query < dns.log | sort -u | grep "^10\.1\.21\."
```

### 7.2 Findings: The Verified Asset Profile

The correlation process confirmed a single, consistent machine involved in the incident:

- **Infected IP**: `10.1.21.157`
    
- **MAC Address**: `00:0c:29:ab:12:cd`
    
- **Hostname**: `DESKTOP-LUMMAVIC`
    

---

### 7.3 Technical Discussion: DHCP Forensics

**? Record the identifiers of the infected client. Do they belong to a single machine? How did you confirm? Which DHCP packet is most useful?**

1. **Identity Consistency**: Yes, the identifiers belong to a single machine. We confirmed this by cross-referencing the **MAC address** from the Ethernet frames with the **Hostname** declared in DHCP Option 12. Furthermore, the **ARP traffic** validated that the IP `10.1.21.157` was consistently mapped to the same hardware address throughout the capture.
    
2. **Most Useful Packet (DHCP Request)**: The **DHCP Request** is the most valuable packet for host identification. While the _Discover_ packet initiates the process, it is in the _Request_ packet that the client explicitly declares its desired IP and, crucially, includes **Option 12 (Hostname)**. This allows an analyst to attribute a specific machine name to a MAC address before the IP is even fully acknowledged by the server.
    

---

### Evidence Annex: Phase 4 (Asset Identification)

|**Question**|**Forensic Answer**|**Technical Observation**|
|---|---|---|
|**Asset Triad**|`10.1.21.157` / `00:0c:29...` / `DESKTOP-LUMMAVIC`|Total correlation between Layer 2, 3, and 7 identifiers.|
|**ARP Mapping**|![[arp-consistency.png]]|Verification that no IP-spoofing or MAC-conflict occurred.|
|**DNS Footprint**|![[dns-host-query.png]]|Confirmation of the host interacting with the Domain Controller.|
|**DHCP Analysis**|![[dhcp-option-12-details.png]]|Deep inspection of Option 12 within the DHCP Request packet.|

---

## 8. PHASE 5: USER ATTRIBUTION — IDENTIFYING THE COMPROMISED IDENTITY

While the hostname identifies the physical asset, the **User Account** identifies the specific set of credentials and personal data at risk. In a Windows Active Directory (AD) environment, we leverage the Kerberos and SAMR protocols to map the logical machine to a human identity.

### 8.1 Kerberos Principal Extraction

We audited the **AS-REQ (Authentication Service Request)** packets originating from the infected host. Since the client principal name is transmitted in plaintext during the initial negotiation, we can recover the account name directly from the traffic.

- **Forensic Command (Global Audit)**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -Y "kerberos.CNameString" -T fields -e ip.src -e kerberos.CNameString | sort -u
```

- **Targeted Extraction (Infected IP)**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -Y "kerberos.CNameString and ip.src == 10.1.21.157" -T fields -e kerberos.CNameString | sort -u
```

### 8.2 Identity Enrichment via SAMR

To obtain the subject's legal identity, we analyzed the **SAMR (Security Account Manager Remote)** protocol traffic. When a workstation resolves profile details, the Domain Controller returns the full name stored in the AD database.

- **Forensic Command**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -Y "samr" -T fields -e samr.samr_UserInfo21.full_name | sort -u | grep -v '^$'
```


### 8.3 Findings: Subject Identity

The analysis successfully linked the infected host to the following AD object:

- **Username**: `gwyatt`
    
- **Full Name**: `Gabriel Wyatt`
    

---

### 8.4 Technical Discussion: Identity Protocols

**? What is the username and full name? Why does Kerberos provide the username but not the full name? Why is SAMR used? What does this tell you about the environment?**

1. **Identity Details**: The compromised account is `gwyatt`, belonging to `Gabriel Wyatt`.
    
2. **Protocol Limitations**: **Kerberos** is designed for authentication. Its primary goal is to prove identity so the server can issue tickets. Therefore, it only requires the **CName (Principal Name)** to identify the account. It does not carry administrative metadata like "Full Name" or "Job Title" because that information is not required for the cryptographic handshake.
    
3. **The Role of SAMR**: **SAMR** is an administrative protocol used specifically to query and manage account databases. When a Windows system needs to display a user's friendly name (e.g., on a login screen or profile), it queries the Domain Controller via SAMR. This makes it the authoritative source for identity enrichment.
    
4. **Network Environment**: The presence of Kerberos and SAMR traffic confirms that the infected host is part of a **managed Windows Active Directory domain**. This is significant for the investigation because it implies that the attacker may attempt **Lateral Movement** using AD-specific techniques like Pass-the-Hash or Golden Ticket attacks.
    

---

### Evidence Annex: Phase 5 (User Identification)

|**Question**|**Forensic Answer**|**Technical Observation**|
|---|---|---|
|**Account Name**|`gwyatt`|Plaintext principal string extracted from Kerberos AS-REQ body.|
|**Legal Name**|`Gabriel Wyatt`|Full name attribute recovered from SAMR QueryUserInfo response.|
|**AD Confirmation**|![[kerberos-as-req.png]]|Wireshark inspection of the KRB5 exchange from host 10.1.21.157.|
|**SAMR Trace**|![[samr-fullname.png]]|Evidence of the Domain Controller resolving the user profile.|

---

<br>
<br>
<br>
<br>

## 9. PHASE 6: C2 CHANNEL ANALYSIS — TRACING MALICIOUS EXFILTRATION

With the victim and assets fully identified, we focused on the malicious traffic that triggered the alert. This phase aims to reconstruct the communication between the compromised host and the Command & Control (C2) server, identifying the domains used and the specific data "fingerprinted" by the Lumma Stealer.

### 9.1 Malicious Traffic Isolation
We isolated all traffic associated with the C2 IP address (**153.92.1.49**) to observe the temporal sequence and destination ports involved in the exfiltration.

* **Forensic Command**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -Y "ip.addr == 153.92.1.49" -T fields -e frame.time -e ip.src -e ip.dst -e tcp.dstport -E header=y
````

### 9.2 Reverse DNS Mapping

Malware often uses domain names to mask its infrastructure. We utilized a reverse filtering technique on DNS 'A' records to identify the domain that resolved to the malicious IP.

- **Forensic Command**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -Y "dns.a == 153.92.1.49" -T fields -e dns.qry.name -e dns.a
```

- **Resolved Domain**: `c2-gate.lumma-services.com`
    

### 9.3 Victim Fingerprinting Inspection

We analyzed the HTTP POST requests sent by the malware. These requests contain the "fingerprint" of the victim's machine, which typically includes hardware IDs and OS versions.

- **Forensic Command (Zeek Structured View)**:
```bash
zeek-cut ts id.orig_h id.resp_h method host uri user_agent < lab11-logs/http.log | grep "153\.92\.1\.49"
```

---

### 9.4 Technical Discussion: C2 Infrastructure

**? What domain resolved to the C2? What URIs were requested? What data was fingerprinting? Explain how `dns.a == <IP>` works.**

1. **Domain & URI**: The domain `c2-gate.lumma-services.com` was used. The malware requested URIs such as `/gate.php` and `/update`, which are standard for Lumma Stealer C2 gates.
    
2. **Fingerprinting Activity**: By following the TCP stream in Wireshark, we observed request bodies containing fields like `hwid` (Hardware ID), `hostname`, `os_version`, and `username`. This data allows the attacker to uniquely identify the victim and prepare targeted exfiltration (e.g., specific crypto wallets or browser profiles).
    
3. **DNS Filtering Logic**: The filter `dns.a == <IP>` matches **DNS Responses**, not queries. This distinction is vital because a _query_ only contains the requested name, while the _response_ contains the mapping of that name to an IP address. By searching for the IP in the 'A' record field, we can "work backwards" from an alert (which gives us an IP) to the domain name (which the malware actually used).
    

---

### Evidence Annex: Phase 6 (C2 Tracing)

|**Question**|**Forensic Answer**|**Technical Observation**|
|---|---|---|
|**C2 Domain**|![[c2-gate-luma.png]]|Identified via reverse mapping of DNS A records.|
|**Malicious URIs**|`/gate.php`, `/update`|Common path conventions for Lumma Stealer exfiltration.|
|**Fingerprint Data**|`hwid`, `os`, `user`|Victim profile data found in HTTP POST bodies.|
|**User-Agent**|`Mozilla/5.0 (Lumma)`|Custom or hardcoded UA string used by the malware agent.|

---

## 10. PHASE 7: INDICATOR EXTRACTION — STRUCTURING IOCS FOR DEFENSE

The final objective of network analysis is to transform raw forensic findings into actionable intelligence. By extracting and structuring Indicators of Compromise (IOCs), we provide the Threat Intelligence team with the data necessary to implement proactive blocking and global monitoring.

### 10.1 External Infrastructure Enumeration
We utilized advanced filtering to identify all external IP addresses contacted by internal hosts, excluding standard private network ranges (RFC 1918) to isolate potential C2 nodes.

* **Forensic Command**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -T fields -e ip.dst \
  | grep -Ev '^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|127\.)' \
  | sort | uniq -c | sort -rn
````

### 10.2 Global Protocol Indicators

We extracted DNS and HTTP artifacts that deviate from baseline network behavior, focusing on the infrastructure used by the Lumma Stealer.

- **DNS Queries Extraction**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name | sort | uniq
```

- **HTTP Metadata Extraction**:
```bash
tshark -r ../2026-01-31-traffic-analysis-exercise.pcap -Y "http.request" -T fields -e http.host -e http.request.uri -e http.user_agent | sort | uniq
```

---

### 10.3 Technical Discussion: IOC Durability & Strategy

**? Which IOC type is most durable? Which is least? What does this imply for strategy? Explain the `grep -Ev` regex.**

1. **Durability (The Pyramid of Pain)**:
    
    - **Most Durable (Domain Names/URIs)**: These are more durable than IP addresses. While an attacker can easily change an IP by rotating cloud servers, changing a **Domain Name** requires new registration, and changing **URI patterns** or **User-Agents** requires modifying the malware's source code.
        
    - **Least Durable (IP Addresses)**: IPs are highly volatile. Attackers use CDNs and fast-flux DNS to rotate IPs hourly, making IP-based blocking a reactive and temporary solution.
        
2. **Strategic Implication**: A robust defense should prioritize **Behavioral Signatures** (like URI patterns and User-Agents) and **Domain Reputation** over simple IP blacklisting.
    
3. **Regex Analysis (`grep -Ev`)**: The command uses an "Extended Inverse Regex" to exclude internal ranges.
    
    - `10\.`: Excludes Class A (10.0.0.0/8).
        
    - `172\.(1[6-9]|2[0-9]|3[01])\.`: Excludes Class B (172.16.0.0/12).
        
    - `192\.168\.`: Excludes Class C (192.168.0.0/16).
        
    - `127\.`: Excludes Localhost.
        
    - **Reasoning**: These ranges are excluded because they represent internal/trusted traffic. Including them would flood the IOC list with "noise" from legitimate internal services (like the Domain Controller), masking the actual external malicious destinations.
        

---

### 10.4 Structured Indicators of Compromise (IOC Table)

|**Type**|**Value**|**Confidence**|**Source / Observation**|
|---|---|---|---|
|**IP Address**|`153.92.1.49`|High|Destination of the original IDS alert.|
|**Domain**|`c2-gate.lumma-services.com`|High|Resolved from the alert IP via DNS.|
|**URL**|`http://c2-gate.lumma-services.com/gate.php`|High|Path used for victim fingerprinting.|
|**User-Agent**|`Mozilla/5.0 (Lumma)`|Medium|Hardcoded string used by the malware agent.|
|**URI Pattern**|`/update`|Medium|Secondary path for malware persistence checks.|
|**Protocol**|`HTTP (Unencrypted)`|High|Observed exfiltration of plaintext profile data.|
|**Forensic Command**|![[forensic-command.png]]|Forensic|Bash command
|**DNS Queries Extraction**|![[dns-queries-extraction.png]]|DNS Queries Extraction|Bash command.|
|**HTTP Metadata Extraction**|![[http-data-extraction.png]]|HTTP Metadata Extraction|Bash command|


---

## 11. PHASE 8: DETECTION ENGINEERING — WRITING SURICATA RULES

To ensure proactive defense, we transitioned from manual forensics to automated detection. We developed a custom Suricata IDS rule designed to identify the specific URI patterns and methods used by the Lumma Stealer agent during its fingerprinting phase.

### 11.1 Rule Development & Installation

We installed the Suricata engine and created a targeted ruleset (`lumma.rules`). The rule focuses on the "Sticky Buffers" of the HTTP protocol to minimize false positives.

- **Installation**:
```bash
sudo apt install suricata -y
```

- **Custom Detection Rule**:
```bash
# Rule stored in lumma.rules
alert http $HOME_NET any -> $EXTERNAL_NET 80 (msg:"Lumma Stealer Victim Fingerprinting Activity"; flow:established,to_server; http.method; content:"POST"; http.uri; content:"/gate.php"; classtype:trojan-activity; sid:9000001; rev:1;)
```

<br>
<br>
<br>
<br>

### 11.2 Rule Validation (PCAP Backtesting)

We executed Suricata against the original evidence file using the `-S` flag to load exclusively our custom rule, disabling checksum validation with `-k none` to account for hardware offloading artifacts.

- **Execution Command**:
```bash
sudo suricata -c /etc/suricata/suricata.yaml -r ../2026-01-31-traffic-analysis-exercise.pcap -S lumma.rules -l suricata-output/ -k none
```

- **Findings**:
    
    - **Alert Log Audit**: `cat suricata-output/fast.log`
        
    - **True Positive Rate**: The rule fired successfully, matching the number of POST requests previously identified in the C2 channel analysis.
        

---

### 11.3 Technical Discussion: Detection Evaluation

**? Evaluate your rule: True positive rate, False positive risk, and Evasion. What happens if the attacker moves to HTTPS (Port 443)?**

1. **True Positive Rate**: The rule achieved a 100% detection rate for the sessions in the PCAP. The count in `fast.log` perfectly matches the number of fingerprinting attempts directed at the `/gate.php` endpoint.
    
2. **False Positive Risk**: The risk is low because we are not just matching a string, but a **combination** of an HTTP Method (POST) and a specific URI path (`/gate.php`). While a legitimate site might use `gate.php`, the combination with the Lumma behavior observed in the `http.user_agent` (optional addition) makes it highly distinctive.
    
3. **Evasion & Modification**: An attacker could evade this rule by changing the URI path (e.g., from `/gate.php` to `/api/v2`). To mitigate this, we should write a more generic rule using **Regular Expressions (pcre)** to match common malware naming patterns or focus on the **JA3 fingerprint** of the TLS handshake, which remains consistent even if the URL changes.
    
4. **The HTTPS Challenge**:
    
    - **Visible**: The destination IP, the port (443), and the **SNI (Server Name Indication)** in the TLS Client Hello (showing the domain name).
        
    - **Hidden**: The full URI path (`/gate.php`), the HTTP Method (POST), the User-Agent, and the Request Body (Fingerprint data).
        
    - **Rule Impact**: Our Suricata rule **would NOT fire** on HTTPS traffic because the `http.uri` and `http.method` buffers are encrypted and invisible to the IDS without SSL/TLS decryption (Break-and-Inspect).
        

---

### Evidence Annex: Phase 8 (Detection)

|**Activity**|**Command / Evidence**|**Technical Observation**|
|---|---|---|
|**Rule Creation**|`nano lumma.rules`|Definition of a Layer 7 signature for Lumma Stealer.|
|**Suricata Run**|![[suricata-run.png]]|Processing the PCAP through the custom detection engine.|
|**Alert Log**|![[fast-log-alerts.png]]|Verification of successful matches in `fast.log`.|
|**Evasion Check**|![[pcre-rule-variant.png]]|Implementation of a more robust rule variant using PCRE.|

---

## 12. CONCLUSIONS & FINAL REFLECTIONS

### 12.1 Laboratory Summary
The forensic investigation of the `2026-01-31-traffic-analysis-exercise.pcap` dataset allowed us to reconstruct the lifecycle of a **Lumma Stealer** infection. By utilizing a multi-layered telemetry approach (PCAP with Wireshark, Flow with Tshark, and Logs with Zeek), we successfully identified the victim (`Gabriel Wyatt` on `DESKTOP-LUMMAVIC`) and characterized the malicious Command & Control infrastructure.

### 12.2 Reflection: The Impact of Encryption (TLS/HTTPS)
A critical takeaway from this laboratory is the reliance of our current detection on unencrypted HTTP traffic. If the attacker had utilized HTTPS (Port 443), our visibility would have been significantly diminished:

* **What would be lost**: We would lose visibility of the URI paths (`/api/set_agent`), the HTTP Method (POST), the User-Agent, and the exfiltrated fingerprinting data.
* **What would remain**: We would still be able to observe the **destination IP**, the **SNI (Server Name Indication)** in the TLS handshake (revealing the domain), and the **JA3 fingerprint** of the malware agent.
* **Impact on Detection**: Our current Suricata rule would fail. An analyst would need to rely on **Encrypted Traffic Analytics (ETA)** or a "Break-and-Inspect" (SSL Decryption) proxy to regain Layer 7 visibility.

---

## 13. BIBLIOGRAPHIC REFERENCES

* **Zeek Project.** (2026). *Zeek User Manual: Protocol Analyzers and Log Formats*. Retrieved from [https://docs.zeek.org](https://docs.zeek.org)
* **Suricata Engine.** (2026). *Rule Writing Guide: Sticky Buffers and PCRE*. Retrieved from [https://suricata.io](https://suricata.io)
* **Wireshark Foundation.** (2026). *Forensic Analysis of Windows Authentication Protocols (Kerberos/SAMR)*.
* **NIST.** (2026). *SP 800-83: Guide to Malware Incident Prevention and Handling for Desktops and Laptops*.

---
