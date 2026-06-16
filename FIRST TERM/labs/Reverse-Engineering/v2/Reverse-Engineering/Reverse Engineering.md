---
Title: "Technical Report: Binary Analysis and Reverse Engineering"
Project: Lab 05 - Software Reverse Engineering
Subject: IT Security and Privacity
Professor: Daniel Esteban Vela López
Author: Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez
Date: 2026-02-24
Location: Bogotá, Colombia
Confidentiality: Internal / Academic Use Only
---

# TECHNICAL REPORT: REVERSE ENGINEERING ANALYSIS

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_de_la_Escuela_Colombiana_de_Ingenier%C3%ADa_-_Universidad.webp" width="250">
  <br>
  <strong>Escuela Colombiana de Ingeniería Julio Garavito</strong>
  <br>
  <br>
  <strong>Project:</strong> Lab 05 - Reverse Engineering <br> 
  <strong>Subject:</strong> IT Security and Privacity <br> 
  <strong>Professor:</strong> Daniel Esteban Vela López <br> 
  <strong>Authors:</strong> Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez <br> 
  <strong>Date:</strong> 2026-02-24 <br> 
  <strong>Location:</strong> Bogotá, Colombia <br><br> 
  <strong>Confidentiality:</strong> Internal / Academic Use Only
</div>

---

## 1. Introduction
### 1.1 Objective
The primary objective of this laboratory is to decompose and analyze a provided ELF binary to understand its logical flow and security mechanisms. By combining static and dynamic analysis, we aim to recover hidden data (passwords) and manipulate the program's execution without having the original source code.

### 1.2 Discussion: The Art of Reverse Engineering
*Before the technical execution, we discussed the strategic importance of choosing the right analysis method for security auditing.*
<br>
<br>
**Perspective: Andersson David Sánchez Méndez**
> "From my perspective, the most critical part of this lab is understanding the **Conditional Jumps** (`je`, `jne`). In reverse engineering, these are the decision points. If we can identify where the program compares our input with the hardcoded key, we have essentially bypassed its security. It's not just about finding a string; it's about understanding the logic that guards it."

**Perspective: Cristian Santiago Pedraza Rodríguez**
> "I find the transition from **Static to Dynamic analysis** fascinating. While `objdump` gives us a cold map of the code, `gdb` allows us to see the 'heartbeat' of the program. I noticed that identifying the function prologue and epilogue is vital to not getting lost in the assembly 'sea'. A good report must translate these low-level instructions into a clear business-risk logic."

---

## 2. Methodology & Tools
We utilized a multi-layered approach to analyze the binary:

| Tool | Purpose | Key Command used |
| :--- | :--- | :--- |
| `file` | Identify architecture and linking | `file passguess` |
| `strings` | Extract hardcoded passwords/text | `strings passguess | less` |
| `objdump` | Static disassembly | `objdump -d passguess` |
| `gdb` | Dynamic debugging and register inspection | `gdb ./passguess` |
| `Cutter/Ghidra` | Visual flowchart and cross-references | *GUI Based* |
| `radare2` | Binary patching (Optional) | `radare2 -w ./passguess` |
<br>

---
<br>
<br>
<br>

## 3. PHASE 0: ENVIRONMENT SETUP & ACQUISITION

### 3.1 Binary Acquisition
In this stage, we transitioned to a "Crackme" challenge scenario. The target binary, `passguess`, was retrieved from an external platform (crackmes.one). This simulates a real-world security audit where the source code is unavailable and the internal logic must be deduced from the compiled file.

### 3.2 Deployment Process
To prepare the analysis environment in Kali Linux, the following steps were performed:
* **Decompression**: The protected archive was extracted using the `unzip` utility, utilizing the challenge password provided by the platform.
* **Permission Management**: Since downloaded files lack execution rights by default, the `chmod +x` command was applied to enable the execution of the `passguess` binary.
* **Verification**: We confirmed the presence of the executable in the workspace.

---

### Evidence Annex: Environment Setup

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Extraction & Permissions** | ![[unzip-crackmes-file.png]] | Successful extraction of the target and application of execution bits. |

---

## 4. PHASE 1: BASIC STATIC INSPECTION (RECONNAISSANCE)

### 4.1 Binary Identification
By executing the `file passguess` command, we determined the fundamental properties required to configure our analysis tools:

* **Format**: ELF 64-bit LSB pie executable.
* **Architecture**: x86-64.
* **Linking**: Dynamically linked.
* **Debug Symbols**: **Not stripped**. This is a critical finding, as keeping symbol names like `main` allows us to navigate the logic much faster than with stripped binaries.

### 4.2 String Discovery & Intelligence Gathering
Static analysis using the `strings` utility revealed several critical information vectors:

* **UI Messages**: We identified the primary interaction prompts: `"Guess The Pass:"`, `"[OK] Password Found"`, and `"[ERROR] Password is incorrect"`.
* **Suspicious Patterns**: Several short, non-standard alphanumeric strings were found, such as `"u3UH"` and **`"7Wtyr"`**. These were flagged as high-probability candidates for the hardcoded password.
* **Metadata**: The binary reveals internal compiler artifacts and names related to standard C libraries.

### 4.3 Static Flowchart Analysis (Disassembly)
Through `objdump -d`, we inspected the raw machine code. Within the `<main>` function, the program's decision-making logic was clearly identified:

1.  **Input Phase**: The program uses `__isoc23_scanf@plt` to capture user input from the terminal.
2.  **Comparison Logic**: A call to `strcmp@plt` was located. This confirms the validation relies on a direct string comparison in memory.
3.  **Branching**: Immediately following the comparison, the `test eax, eax` instruction and a `jne` (jump if not equal) determine whether the flow proceeds to the "Success" block or the "Error" block.

---

### Evidence Annex: Static Analysis

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **File Properties** | ![[file-pasgues.png]] | Confirmation of x64 architecture and non-stripped symbol state. |
| **String Discovery (1)** | ![[strings-part1.png]] | Discovery of UI messages and potential password keys (`u3UH`, `7Wtyr`). |
| **String Discovery (2)** | ![[strings-part2.png]] | Identification of standard C library symbols for string comparison. |
| **String Discovery (3)** | ![[strings-part3.png]] | Inspection of data sections and symbol table structures. |
| **Code Disassembly (1)** | ![[objdump-part1.png]] | Disassembly of the `.plt` section for external function calls. |
| **Code Disassembly (2)** | ![[objdump-part2.png]] | Analysis of dynamic jump slots for I/O operations. |
| **Code Disassembly (3)** | ![[objdump-part3.png]] | Localization of the entry point and initial stack preparation. |
| **Main Logic Analysis** | ![[objdump-part4.png]] | Final mapping of the `main` function and its conditional branching. |

---

## 5. PHASE 2: DECOMPILATION & PSEUDOCODE ANALYSIS (GHIDRA)

### 5.1 Static Analysis with Ghidra
To move beyond raw assembly, we utilized **Ghidra**. This allowed us to perform an auto-analysis that reconstructs a high-level C-like pseudocode.

* **Binary Import**: The `passguess` binary was imported as an x86-64 ELF executable.
* **Function Mapping**: Using the **Symbol Tree**, we navigated directly to the `main` function. The decompiler window translated stack operations into readable logical blocks.

### 5.2 Logical Reconstruction
The decompiled pseudocode revealed the internal structure of the authentication mechanism:

1.  **Variable Initialization**: The program declares a local buffer (`local_118`) of 264 bytes.
2.  **Input Capture**: It calls `printf` for the prompt and `scanf` with `"%255s"`.
3.  **The Comparison Engine**: `strcmp` compares the input against the hardcoded literal: **`"7Wtyr"`**.
4.  **Conditional Branching**: Success triggers if the comparison result is `0`.

### 5.3 Password Extraction & Verification
* **Hardcoded Password**: `7Wtyr`
* **Verification**: Running `./passguess` and entering the key triggered the `[OK]` message.

---

### Evidence Annex: Ghidra Decompilation

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Ghidra Import** | ![[import-binary-file.png]] | Successful loading of the ELF binary into the Ghidra workspace. |
| **Function Tree** | ![[function-main.png]] | Navigation to the `main` symbol to isolate entry point logic. |
| **Pseudocode (1)** | ![[pseudocode-part1.png]] | Initial view of the `scanf` and `printf` interaction blocks. |
| **Pseudocode (2)** | ![[pseudocode-part2.png]] | Identification of the `strcmp` call with the hardcoded "7Wtyr" string. |
| **Successful Bypass** | ![[password-guess.png]] | Execution of the binary confirming "7Wtyr" as the correct credential. |

---

## 6. PHASE 3: DYNAMIC ANALYSIS (GDB)

### 6.1 Execution Control
We used **GDB** to observe the program's behavior in real-time. 

1.  **Initialization**: We set a breakpoint at `main` and started the process.
2.  **Logic Mapping**: We used `disassemble main` to find the exact memory address of the `strcmp` call.

### 6.2 Register Inspection
At the `strcmp` call, we inspected the arguments passed via registers:
* **Register `$rdi`**: Contained our test input ("hello").
* **Register `$rsi`**: Contained the hardcoded string **"7Wtyr"**.

### 6.3 Return Value
Checking the **`rax`** register after the call confirmed a non-zero value for non-matching strings, which drives the conditional jump logic.

---

### Evidence Annex: Dynamic Analysis (GDB)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Breakpoint & Run** | ![[gdb-break-run.png]] | Entry point synchronization and initial process execution. |
| **Disassembly Analysis**| ![[deassemble-command.png]] | Identification of memory offsets for critical function calls. |
| **Call Interception** | ![[deassemble-strcmp-command.png]] | Pinpointing the exact address of the `strcmp` logic gate. |
| **Argument Inspection** | ![[xs-rsdi-command.png]] | Memory dump of `$rdi` and `$rsi` showing input vs secret. |
| **Register Status** | ![[info-registers-command.png]] | Capture of the `rax` return value determining the program's path. |

<br>
<br>

---

<br>
<br>
<br>

## 7. PHASE 4: VISUAL FLOW ANALYSIS (CUTTER)

### 7.1 Graphical Mapping
**Cutter** was used to represent the binary's execution as a directed control flow graph.

### 7.2 Functional Decomposition
The **Graph View** visually confirms:
1.  **Input Block**: Initial setup and `scanf`.
2.  **Comparison Junction**: `strcmp` followed by a conditional jump.
3.  **The Fork**: A green/red path splitting into `[OK]` (Success) and `[ERROR]` (Failure).

---

### Evidence Annex: Visual Analysis (Cutter)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Dashboard View** | ![[cutter-dashboard.png]] | Initial analysis phase identifying binary metadata. |
| **Logic Graph** | ![[cutter-graph.png]] | Flowchart showing the input, comparison, and branching paths. |

---

## 8. PHASE 5: BINARY MANIPULATION (RADARE2)

### 8.1 Logic Patching
We used **radare2** to bypass the check entirely. After opening in write mode and analyzing, we mapped the function using `pdf`.

### 8.2 Logic Bypass
By navigating to the conditional jump address, we used `wa jne` to **invert the logic**.

### 8.3 Verification
The patched binary now accepts any input as "correct," proving that client-side validation can be neutralized with a single instruction change.

---

### Evidence Annex: Binary Patching (Radare2)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Write Mode Setup** | ![[binary-write-mode.png]] | Initializing radare2 in read-write mode. |
| **Function Disassembly** | ![[radare-pdf-part1.png]] | Visualizing stack frames in the target block. |
| **Jump Identification** | ![[radare-pdf-part2.png]] | Locating the conditional jump following the comparison. |
| **Instruction Patch** | ![[je-jne-command.png]] | Inverting the logical outcome of the check. |
| **Patch Verification** | ![[test-batched-binary.png]] | Successful bypass using a random string. |
<br>

---
<br>
<br>

## 9. CONCLUSIONS

* **Inherent Insecurity of Hardcoded Secrets**: This lab demonstrates that hardcoded strings (like "7Wtyr") are trivial to extract using static analysis (`strings`, Ghidra). Developers should never store credentials in plaintext within a binary.
* **Effectiveness of Multi-Tool Analysis**: Combining static tools (Ghidra) for logic understanding and dynamic tools (GDB) for real-time register inspection provides a complete view of a system's vulnerability.
* **Binary Fragility**: The successful logic inversion using `radare2` proves that binaries are not immutable. A single byte change (patching a jump) can completely bypass sophisticated validation routines.
* **The Role of Symbols**: Working with a non-stripped binary significantly simplified the identification of `main`. In a real-world scenario, obfuscation and symbol stripping are mandatory first lines of defense.

---

## 10. REFERENCES

* **Eilam, E.** (2011). *Reversing: Secrets of Reverse Engineering*. Wiley Publishing.
* **Radare2 Project**. (2025). *Radare2 Book: Official Documentation*. https://book.rada.re/
* **Ghidra Research**. (2025). *Ghidra User Guide*. National Security Agency.
* **Intel Corporation**. (2024). *Intel® 64 and IA-32 Architectures Software Developer Manuals*.
* **GNU Project**. (2025). *GDB: The GNU Project Debugger*. https://www.gnu.org/software/gdb/