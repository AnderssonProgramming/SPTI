# 🔐 SPTI: IT Security and Privacy

Welcome to the repository for **SPTI** (Seguridad y Privacidad en TI - IT Security and Privacy) at the *Escuela Colombiana de Ingeniería Julio Garavito*.
This comprehensive collection showcases the complete journey through IT security fundamentals, from OSINT and threat modeling to ethical hacking, DevSecOps, and security automation — covering the full spectrum of offensive and defensive cybersecurity disciplines.

---

## 📚 Topics Covered

### 🕵️ Reconnaissance & OSINT

* Open-Source Intelligence techniques and tools
* Maltego graph-based investigation and metadata analysis
* Linux deep dive for security practitioners

### 🧩 Threat Modeling & Security Architecture

* STRIDE methodology and threat modeling frameworks
* Information Security Management Systems (SGSI / ISO 27001)
* Risk management and security architecture principles
* Data protection and privacy legislation (Colombian law)

### 🔬 Exploitation & Vulnerability Research

* Reverse engineering with static and dynamic analysis
* Buffer overflow exploitation and stack smashing
* Ethical hacking methodology and penetration testing
* Cryptography: symmetric, asymmetric, hashing, and PKI
* Malware analysis (static and behavioral)
* Source code vulnerability management (SAST/SCA/DAST)

### 🌐 Network, Web & Forensics

* Network traffic analysis with Wireshark and Suricata
* Web application security (OWASP Top 10, injection, XSS, IDOR)
* Digital forensics and disk image analysis
* Security architecture for enterprise systems

### ⚙️ DevSecOps & Automation

* Shift-Left and Shift-Right security integration
* Security automation pipelines and reconnaissance toolchains
* Real-time monitoring, logging, and threat detection
* Security metrics, KPIs, and incident response within the SSDLC

---

## 🎯 Core Repositories & Seminar Projects

Throughout this course, specialized repositories were developed implementing real security tools and enterprise-grade security pipelines:

### 🔹 1. DevSecOps Command Center
Enterprise-grade DevSecOps monitoring platform securing the **LogiFlow** platform through a full Shift-Left (SAST/SCA) and Shift-Right (DAST/Falco) lifecycle. Features a production monitoring stack with Prometheus, Grafana, and Loki for real-time threat detection.

[🔗 View Repository](https://github.com/AnderssonProgramming/devsecops-threat-monitor)

---

### 🔹 2. LogiFlow Cybersecurity Seminar Platform
Monorepo for an AI-powered real-time fleet routing platform — the target system secured throughout the seminar. Implements NestJS, gRPC, WebSockets, n8n automation, and VROOM optimization for Colombian logistics at scale, used as the substrate for all security exercises.

[🔗 View Repository](https://github.com/AnderssonProgramming/logiflow-cybersecurity-seminar)

---

### 🔹 3. Automated Recon Toolkit
Security Automation Pipeline — the final lab of the course. Implements a Python reconnaissance toolchain featuring an `asyncio` port scanner, Nmap XML parsing, and 3-Sigma log anomaly detection. Includes an OPSEC CLI integrating `whois`, `dig`, `nmap`, and `curl` with full audit logging.

[🔗 View Repository](https://github.com/AnderssonProgramming/automated-recon-toolkit)

---

## 📁 Repository Structure

### 📘 FIRST TERM – Foundations of Cybersecurity

**Focus**: Cybersecurity fundamentals, risk management, OSINT, threat modeling, and reverse engineering

#### 🔬 Labs

* **Linux Deep Dive** – Security-oriented Linux administration, command-line mastery, and system hardening
* **OSINT** – Open-source intelligence gathering with Maltego, metadata extraction, and target profiling
* **Report Writing** – Professional security report writing with CherryTree and Obsidian
* **Reverse Engineering** – Static and dynamic binary analysis (v1 and v2 iterations)
* **Threat Modeling** – STRIDE-based threat modeling for real application architectures

**Key Lab Reports**:

* [FIRST TERM/labs/Linux/](FIRST%20TERM/labs/Linux/) – Linux security deep dive and lab report
* [FIRST TERM/labs/OSINT/](FIRST%20TERM/labs/OSINT/) – OSINT investigation report with Maltego graphs
* [FIRST TERM/labs/Reverse-Engineering/](FIRST%20TERM/labs/Reverse-Engineering/) – Reverse engineering analysis (v1 & v2)
* [FIRST TERM/labs/Threat-Modeling/](FIRST%20TERM/labs/Threat-Modeling/) – Threat modeling workshop deliverable

#### 📖 Theory

**Slides**:

* [1. Introduction to Cybersecurity](FIRST%20TERM/theory/slides/1.%20Introduccion%20a%20ciberseguridad.pdf)
* [2. Risk Management](FIRST%20TERM/theory/slides/2.%20Risk%20Management.pdf)
* [3. Security Architecture Principles](FIRST%20TERM/theory/slides/3.%20Security%20Architecture%20Principles.pdf)
* [4. Legislation](FIRST%20TERM/theory/slides/4.%20Legislaci%C3%B3n.pdf)
* [5. SGSI (ISO 27001)](FIRST%20TERM/theory/slides/5%20-%20SGSI.pdf)

**Workshops**:

* [Intro Keralty – Cybersecurity in Practice](FIRST%20TERM/theory/workshops/intro-Keralty/)
* [Risk Management – Keralty Case Study](FIRST%20TERM/theory/workshops/management-risks-Keralty/)
* [Security Architecture Workshop](FIRST%20TERM/theory/workshops/security-architecture/)
* [SGSI Introduction & ISO 27000 Workshop](FIRST%20TERM/theory/workshops/SGSI-introduction/)

**Books & Readings**:

* [EY Cyber Resilience](FIRST%20TERM/theory/books/ey-cyber-resilience-final.pdf)
* [Adding Value With Risk-Based Information Security](FIRST%20TERM/theory/books/Semana4_Adding-Value-With-Risk-Based-Information-Security_joa_eng_0924.pdf)
* [The Inhibitors to Zero Trust](FIRST%20TERM/theory/books/Semana_3_The-Inhibitors-to-Zero_joa_Eng_0524.pdf)

---

### 📗 SECOND TERM – Exploitation & Vulnerability Management

**Focus**: Hands-on offensive security, cryptography, malware analysis, and vulnerability management

#### 🔬 Labs

* **Buffer Overflow** – Stack-based buffer overflow exploitation with Python scripts; understanding memory corruption
* **Cryptography** – Symmetric (AES), asymmetric (RSA), hashing (SHA), and PKI implementation
* **Ethical Hacking** – Full penetration testing lifecycle: reconnaissance, scanning, exploitation, post-exploitation
* **Malware Analysis** – Static and behavioral analysis of malware samples in isolated environments
* **Source Code Vulnerability Management** – SAST/SCA analysis on a vulnerable Node.js/Express/SQLite app with npm audit and vulnerability patching

**Key Lab Reports**:

* [SECOND TERM/labs/Buffer-Overflow/](SECOND%20TERM/labs/Buffer-Overflow/) – Exploit scripts and overflow analysis report
* [SECOND TERM/labs/Cryptography/](SECOND%20TERM/labs/Cryptography/) – Cryptographic implementation and analysis
* [SECOND TERM/labs/Ethical-Hacking/](SECOND%20TERM/labs/Ethical-Hacking/) – Full pentest report with evidence
* [SECOND TERM/labs/Malware-Analysis/](SECOND%20TERM/labs/Malware-Analysis/) – Malware dissection and behavioral report
* [SECOND TERM/labs/Source-Code-Vulnerability-Management/](SECOND%20TERM/labs/Source-Code-Vulnerability-Management/) – Vulnerable Node.js app + SAST/SCA findings

#### 📖 Theory

**Slides**:

* [6. Data Protection](SECOND%20TERM/theory/slides/6.%20Data%20Protection.pdf)
* [7. Security in the Data Lifecycle](SECOND%20TERM/theory/slides/7.%20Security%20in%20the%20Data%20Lifecycle.pdf)
* [8. Software Security](SECOND%20TERM/theory/slides/8.%20Software%20security.pdf)

**Workshops**:

* [Cryptography & Bitwarden Workshop](SECOND%20TERM/theory/workshops/)
* [Security in the Data Lifecycle Workshop](SECOND%20TERM/theory/workshops/)

---

### 📕 THIRD TERM – Advanced Security & DevSecOps

**Focus**: Network security, digital forensics, web application security, security architecture, and DevSecOps automation

#### 🔬 Labs

* **Automation** – Python security automation pipeline with asyncio port scanner, Nmap XML parsing, 3-Sigma anomaly detection, and OPSEC CLI
* **DevSecOps** – Full Shift-Left/Shift-Right pipeline: SAST, SCA, DAST, and runtime monitoring with Falco, Prometheus, Grafana, Loki
* **Digital Forensics** – Disk image acquisition and analysis, file carving, timeline reconstruction, and evidence reporting
* **Network Analysis** – Packet capture analysis with Wireshark, IDS rule writing with Suricata, and log correlation
* **Security Architecture** – Enterprise security architecture design and implementation review
* **Web Application Security** – OWASP Top 10 exploitation: SQL injection, XSS, IDOR, CSRF, authentication bypass

**Key Lab Reports**:

* [THIRD TERM/labs/Automation/](THIRD%20TERM/labs/Automation/) – Recon automation lab report + submission + sample outputs
* [THIRD TERM/labs/DevSecOps/](THIRD%20TERM/labs/DevSecOps/) – DevSecOps pipeline implementation
* [THIRD TERM/labs/Digital-Forensics/](THIRD%20TERM/labs/Digital-Forensics/) – Forensic disk analysis and chain of custody
* [THIRD TERM/labs/Network-Analysis/](THIRD%20TERM/labs/Network-Analysis/) – Network traffic analysis with Suricata logs
* [THIRD TERM/labs/Security-Architecture/](THIRD%20TERM/labs/Security-Architecture/) – Enterprise security architecture design
* [THIRD TERM/labs/Web-Application-Security/](THIRD%20TERM/labs/Web-Application-Security/) – Web vulnerability exploitation report

#### 📖 Theory

**Slides**:

* [9. Security in the Data Lifecycle (Advanced)](THIRD%20TERM/theory/slides/9.%20Security%20in%20the%20Data%20Lifecycle.pdf)
* [10. Network Security and Modern Technologies](THIRD%20TERM/theory/slides/10.%20Network%20Security%20and%20Modern%20Technologies.pdf)

---

## 🏛️ Seminar – Security in Production Systems

The **SEMINAR** folder (excluded from version control) contains presentations from the collaborative seminar covering advanced production security topics:

| Group | Topic |
|-------|-------|
| Grupo 1 | Security Observability & Logging in Applications |
| Grupo 2 | Continuous Monitoring & Threat Detection in Production |
| Grupo 3 | Vulnerability Management in Production (CFFC) |
| Grupo 4 | Incident Response Integrated into the DevSecOps Cycle |
| Grupo 5 | Security Failure Automation & Resolution |
| Grupo 6 | Metrics & KPIs in the SSDLC |
| Grupo 7 | AI & Automation in DevSecOps |

---

## 🧪 Key Learning Components

### 📓 Lab Reports (Obsidian + CherryTree)

Detailed security lab reports written in Obsidian Markdown and CherryTree, documenting methodology, findings, evidence, and remediation recommendations for each hands-on exercise.

### 🔬 Hands-On Exploitation

Practical offensive and defensive exercises covering the full attack lifecycle — from reconnaissance and enumeration to exploitation, post-exploitation, and reporting.

### 🛠️ Security Tools & Pipelines

Real tool implementations: custom Python scanners, Suricata IDS rules, SAST/SCA pipelines, Falco runtime security, and Prometheus/Grafana monitoring stacks.

### 🎓 Theoretical Foundations

Comprehensive slides and workshops covering cybersecurity principles, risk management, legislation (ISO 27001, Colombian data protection law), and enterprise security architecture.

---

## 🧰 Tech Stack & Tools

* `Python 🐍` — Security automation, port scanning, anomaly detection
* `Node.js / Express` — Vulnerable application for SAST/SCA exercises
* `Nmap 🗺️` — Network scanning and host discovery
* `Wireshark / Suricata 🦈` — Packet capture and IDS
* `Falco` — Runtime security monitoring
* `Prometheus / Grafana / Loki 📊` — Security observability stack
* `Maltego 🔗` — OSINT graph investigation
* `Obsidian / CherryTree 📝` — Security report writing
* `Docker 🐳` — Containerized lab environments
* `Metasploit / Burp Suite` — Exploitation frameworks
* `Bitwarden / GPG` — Cryptography and secrets management

---

## 🖼️ Visuals

<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/2092/2092757.png" width="65px" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="65px" style="margin-left: 20px;"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="65px" style="margin-left: 20px;" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" width="65px" style="margin-left: 20px;" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/grafana/grafana-original.svg" width="65px" style="margin-left: 20px;" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/prometheus/prometheus-original.svg" width="65px" style="margin-left: 20px;" />
</p>

---

## 🎓 Course Progression

```
FIRST TERM: Security Foundations
    ↓
OSINT → Threat Modeling → Reverse Engineering → Risk Management
    ↓
SECOND TERM: Exploitation & Vulnerability Management
    ↓
Buffer Overflow → Ethical Hacking → Cryptography → Malware Analysis → SAST/SCA
    ↓
THIRD TERM: Advanced Security & DevSecOps
    ↓
Network Analysis → Web Security → Digital Forensics → DevSecOps → Security Automation
```

---

## 📖 Additional Resources

* `FIRST TERM/theory/books/` — Curated readings on cyber resilience, risk-based security, and Zero Trust
* `FIRST TERM/theory/workshops/` — Industry-partnered workshops with Keralty (healthcare security case study)
* `SEMINAR/` — Advanced production security seminar presentations (7 groups, full SSDLC coverage)
* `THIRD TERM/labs/Automation/submission/` — Automation lab final submission and sample outputs

---

## 📬 Contact

Explore the attack surface, model your threats, automate your defenses, and secure the entire lifecycle.
💌 **[andersson.sanchez-m@mail.escuelaing.edu.co](mailto:andersson.sanchez-m@mail.escuelaing.edu.co)** — Let's build secure systems together!

---

> *"Security is not a product, but a process."* – Bruce Schneier
>
> Know your adversary. Model your threats. Automate your defense. Secure the pipeline. 🔐🛡️
