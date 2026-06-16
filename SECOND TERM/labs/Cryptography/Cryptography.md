---
Title: "Technical Report: Cryptographic Techniques and Data Integrity"
Project: Lab 06 - Cryptography
Subject: IT Security and Privacy
Professor: Daniel Esteban Vela López
Author: Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez
Date: 2026-03-03
Location: Bogotá, Colombia
Confidentiality: Internal / Academic Use Only
---

# TECHNICAL REPORT: CRYPTOGRAPHY ANALYSIS

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Logo_de_la_Escuela_Colombiana_de_Ingenier%C3%ADa_-_Universidad.webp" width="250">
  <br>
  <strong>Escuela Colombiana de Ingeniería Julio Garavito</strong>
  <br>
  <br>
  <strong>Project:</strong> Lab 06 - Cryptography <br> 
  <strong>Subject:</strong> IT Security and Privacy <br> 
  <strong>Professor:</strong> Daniel Esteban Vela López <br> 
  <strong>Authors:</strong> Andersson David Sánchez Méndez & Cristian Santiago Pedraza Rodríguez <br> 
  <strong>Date:</strong> 2026-03-03 <br> 
  <strong>Location:</strong> Bogotá, Colombia <br><br> 
  <strong>Confidentiality:</strong> Internal / Academic Use Only
</div>

---

## 1. Introduction
### 1.1 Objective
The primary objective of this laboratory is to implement and verify cryptographic techniques to ensure **Confidentiality**, **Integrity**, and **Authenticity**. We aim to analyze the "Avalanche Effect" in hash functions, apply symmetric encryption (AES) for data protection, and manage asymmetric key pairs (RSA/GPG) for secure identification and communication.

<br>
<br>
<br>
<br>
<br>
<br>

### 1.2 Discussion: The Pillars of Trust

**Perspective: Andersson David Sánchez Méndez**
> "In cryptography, the hash is the 'digital DNA'. Understanding that a single bit change—even in a large, multi-line document—completely alters the output is fundamental for detecting unauthorized modifications. It is the first line of defense in verifying that what we downloaded is exactly what the author intended."

**Perspective: Cristian Santiago Pedraza Rodríguez**
> "The transition from classical methods to modern standards like AES and RSA shows how mathematical complexity protects our daily lives. This lab allows us to see how these abstract concepts become practical tools like OpenSSL and GPG to secure data over insecure channels, ensuring that integrity is maintained even in hostile environments."

---

## 2. Methodology & Tools
We utilized a multi-layered cryptographic approach:

| Tool | Purpose | Key Command used |
| :--- | :--- | :--- |
| `sha256sum` | Integrity verification (Secure Standard) | `sha256sum [file]` |
| `md5sum` | Legacy integrity verification | `md5sum [file]` |
| `openssl` | Symmetric and Asymmetric operations | `openssl enc`, `openssl rsa` |
| `gpg` | Public key infrastructure and signing | `gpg --gen-key` |
| `Python 3` | Scripting for automated ciphers | `python3` |
<br>

---
<br>
<br>
<br>

## 3. PHASE 1: DATA INTEGRITY WITH HASH FUNCTIONS

### 3.1 SHA-256 Fingerprinting and Baseline
To verify data integrity, we created a sophisticated, multi-line document named `document.txt`. This document simulates a structured project file containing metadata such as project names, versions, and access levels.

1.  **Creation**: We used the `cat` command to generate the structured file.
2.  **Initial Hash**: We executed `sha256sum document.txt` to generate the initial cryptographic digest. This 64-character hexadecimal string represents the "Known Good" state of the file.

### 3.2 Detection of "Silent" Modifications
We simulated an unauthorized modification by altering a single line within the document—specifically changing the version number from `1.0.4` to `1.0.5`. 

* **The Result**: Upon recalculating the hash, the output was entirely different from the original.
* **Technical Conclusion**: This demonstrates the **Avalanche Effect**, where even a minor, 1-bit change results in a drastically different hash. This confirms that SHA-256 is highly effective at detecting tampering in structured data.

### 3.3 Collision Resistance Analysis (MD5)
To explore legacy hash functions, we generated two files that were "almost identical" to the human eye, differing only by a single trailing space in the string "Access Granted".

* **Observation**: Executing `md5sum` on both files revealed two completely different 128-bit digests.
* **Security Note**: While MD5 successfully detected this specific change, it is considered cryptographically insecure today because it is susceptible to "collision attacks," where different inputs can be engineered to produce the same hash.

<br>
<br>
<br>
<br>
<br>

### Evidence Annex: Phase 1 (Integrity)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Creation & Initial Hash** | ![[creation-sha256-initial.png]] | Generation of the 256-bit fingerprint for the original structured file. |
| **Integrity Violation** | ![[modify-sha256-final.png]] | Hash mismatch confirmed after modifying a single line (Version update). |
| **MD5 Comparison** | ![[md5sum-comparation.png]] | Successful differentiation of two nearly identical files using MD5. |

---

## 4. PHASE 2: SYMMETRIC ENCRYPTION (AES)

### 4.1 Implementation of AES-256-CBC
To ensure **Confidentiality**, we utilized the Advanced Encryption Standard (AES) with a 256-bit key in Cipher Block Chaining (CBC) mode. 

1.  **Encryption**: We created `secret.txt` with fictitious sensitive data. Using `openssl`, we encrypted it into `secret.enc`. 
2.  **Key Derivation Note**: During execution, OpenSSL issued a warning regarding deprecated key derivation. To align with modern standards, we utilized the `-pbkdf2` and `-iter` flags, ensuring the password was processed through a robust key-stretching algorithm.
3.  **Obfuscation Check**: Running `cat secret.enc` confirmed that the content was no longer human-readable, appearing as encrypted binary data.

### 4.2 Decryption and Resilience Testing
* **Successful Recovery**: By applying the correct password with the `-d` (decrypt) flag, we successfully reconstructed the original sensitive content in `secret_decrypted.txt`.
* **Security Failure Case**: We attempted to bypass the encryption using incorrect passwords. OpenSSL consistently rejected these attempts with a `bad decrypt` error, proving that without the exact cryptographic key, the data remains secure and inaccessible.

### 4.3 Behavioral Analysis: CBC vs. ECB Mode
We analyzed the behavioral differences between **CBC** (Cipher Block Chaining) and **ECB** (Electronic Codebook).

* **Observations**: In ECB mode, identical blocks of plaintext are encrypted into identical blocks of ciphertext, which can reveal data patterns. CBC, by utilizing an Initialization Vector (IV), ensures that even identical data blocks produce unique ciphertext, providing superior protection against pattern analysis.

### Evidence Annex: Phase 2 (Confidentiality)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **AES-256 Encryption** | ![[creation-secret-encrypt-enc.png]] | Secure encryption of sensitive data and visualization of binary ciphertext. |
| **Successful Decryption** | ![[decrypt-correct-passwd.png]] | Verification of the decryption process using the authorized password. |
| **Unauthorized Access** | ![[aes-wrong-passwd.png]] | Demonstration of the system's resilience against incorrect key attempts. |
| **ECB vs. CBC Mode** | ![[aes-ecb-comparison.png]] | Behavioral analysis of pattern preservation in insecure encryption modes. |

---

## 5. PHASE 3: ASYMMETRIC ENCRYPTION (GPG)

### 5.1 Public/Private Key Generation
We implemented a secure communication channel using **GPG (GNU Privacy Guard)**. Each analyst generated an RSA key pair (Public and Private). 

* **Public Key**: Exported and shared with the partner to allow message encryption.
* **Private Key**: Kept secret and protected by a passphrase to allow decryption of received messages.

<br>
<br>

### 5.2 Key Exchange and Trust
We exchanged public keys in ASCII-armored format. Importing the partner's key into the local keyring is a critical step that establishes the infrastructure for asymmetric communication.

### 5.3 Secure Communication Workflow
1.  **Encryption**: Andersson encrypted a message using Cristian's public key.
2.  **Decryption**: Cristian received the `.gpg` file and used his private key (and passphrase) to reveal the original message. This process was then mirrored for bi-directional communication.



### 5.4 Vulnerability Analysis
**Q: What would happen if someone intercepted the encrypted message but did not have the recipient’s private key?**
> If an attacker intercepts the message, they would only see a block of ciphered text (the PGP message). Without the recipient's private key, the message is mathematically impossible to decrypt within a reasonable timeframe using current technology. 

**Q: What property ensures the message remains confidential?**
> The property is **Asymmetric Trapdoor Functions**. In RSA, while it is computationally easy to encrypt a message using a public key, it is computationally "hard" (practically impossible) to reverse the process without the private key, which serves as the "trapdoor" information. This ensures **Confidentiality**.

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

### Evidence Annex: Phase 3 (Asymmetric Exchange)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Andersson: Key Gen** | ![[gpg-key-creation.png]] | Selection of RSA/RSA 4096-bit algorithm for Andersson. |
| **Andersson: Passphrase**| ![[gpg-key-passwd.png]] | Implementation of a secure passphrase for private key protection. |
| **Cristian: Key Gen** | ![[pub-generation.png]] | Generation of the public/private key pair on Cristian's VM. |
| **Andersson: Import** | ![[importing-andersson-pub.png]] | Importing the partner's public key into the local keyring. |
| **Andersson: Listing** | ![[listing-keys.png]] | Verification of the keyring status showing both identities. |
| **Cristian: Import/List**| ![[gpg-import-cristianpub-listkeys.png]] | Cristian's environment showing the successful import of Andersson's key. |
| **Andersson: Encrypt** | ![[encrypting-message_andersson.png]] | Ciphers a message intended exclusively for Cristian's private key. |
| **Cristian: Encrypt** | ![[encrypting-message_cistian.png]] | Ciphers a message intended exclusively for Andersson's private key. |
| **Andersson: Decrypt** | ![[decrypt-message-andersson.png]] | Successful retrieval of the secret message using the private key. |
| **Cristian: Decrypt** | ![[decrypt-message-cristian.png]] | Final verification of the secure channel on Cristian's side. |

---

## 6. PHASE 4: CLASSICAL CRYPTOGRAPHY & CRYPTOANALYSIS

### 6.1 Implementation of Caesar Cipher
We developed a custom Python-based tool to simulate classical substitution ciphers. Unlike the modern algorithms analyzed in previous phases, the Caesar cipher relies on a fixed shift across the alphabet ($n + \text{shift} \pmod{26}$), representing a significant evolutionary step in cryptographic history.

1.  **Script Logic**: Using the `nano` editor, we implemented functions for encryption and decryption. The script handles ASCII character manipulation using `ord()` and `chr()` to ensure precise mathematical rotations.
2.  **Maintainability**: The implementation preserves non-alphabetic symbols (spaces and punctuation) while maintaining the case of the original plaintext.



### 6.2 Vulnerability Assessment: Frequency Analysis
To demonstrate the inherent weakness of monoalphabetic substitution, we implemented a frequency detection algorithm within our script.
* **Theory**: In English, the letter **'E'** is statistically the most frequent character. Our script identifies the most common character in the ciphertext and calculates its distance from 'E'.
* **Result**: During testing, the script successfully identified the probable key (Shift 7) without human intervention, proving that preserving character frequency makes encryption trivial to break.



### 6.3 Brute Force Attack
Due to the extremely small key space (only 26 possible shifts), Caesar ciphers are entirely susceptible to exhaustive search attacks.
* **Mechanism**: Our script iterates through all 25 possible rotations of the ciphertext.
* **Observation**: As seen in the evidence, a computational "Brute Force" attack yields the original message almost instantaneously. This highlights why modern security requires exponentially larger key spaces, such as those found in AES-256 or RSA-4096.

<br>
<br>
<br>
### Evidence Annex: Phase 4 (Classical Crypto)

| Activity | Command / Evidence | Technical Observation |
| :--- | :--- | :--- |
| **Source Code Development** | ![[creation_script.png]] | Implementation of the shift logic and statistical analysis using Python 3. |
| **Functional Testing** | ![[test-execution.png]] | Successful encryption of a complex string using a shift key of 7. |
| **Cryptoanalysis Results** | ![[breaking-attempts.png]] | Exhaustive search output showing the recovered plaintext at Key 07. |

---

## 7. CONCLUSION
Through this laboratory, we successfully verified the three pillars of information security:
* **Integrity**: Confirmed via SHA-256 and the observation of the Avalanche Effect, where a 1-bit change invalidates the entire hash.
* **Confidentiality**: Demonstrated through the implementation of symmetric (AES) and asymmetric (GPG) encryption, where the latter provides a superior "Trapdoor" mechanism for secure key exchange.
* **Vulnerability**: Analyzed through classical cryptography, proving that algorithms with small key spaces or those that preserve plaintext patterns are obsolete against modern statistical and brute-force attacks.

<br>
<br>
<br>
<br>

## 8. BIBLIOGRAPHY
1. Stallings, W. (2020). *Cryptography and Network Security: Principles and Practice*. Pearson.
2. GnuPG Documentation. (2026). *The GNU Privacy Handbook*. 
3. OpenSSL Project. (2026). *Cryptography and SSL/TLS Toolkit Manual*.

---