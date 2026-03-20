"""
license.py — License validation for ReachFlow Pro (reachflow-pro)

This file is a functional stub intended to be replaced with a PyArmor-obfuscated
version before distribution. The check_license() function currently returns True
unconditionally, allowing the app to run without a real license check.

HOW TO ENABLE REAL LICENSING WITH PYARMOR
------------------------------------------
1. Install PyArmor:
       pip install pyarmor

2. Obtain or generate a license key file (e.g. via pyarmor's license command):
       pyarmor gen key --expired 365

3. Replace the body of check_license() below with your real validation logic
   (e.g. verifying a signed license file, calling a license server, or comparing
   a user-supplied key against get_machine_id()).

4. Obfuscate this file with PyArmor so the validation logic cannot be read:
       pyarmor gen license.py

5. Replace this file in your distribution with the obfuscated output from
   the dist/ folder that PyArmor produces. The obfuscated file exposes the same
   public API (check_license, get_machine_id), so no other code needs to change.

6. Never ship the un-obfuscated source of the real check_license() to customers.
"""

import hashlib
import socket
import uuid


def get_machine_id() -> str:
    """
    Return a stable, hex-encoded fingerprint of this machine derived from its
    hostname and primary network interface MAC address.

    The fingerprint is a SHA-256 digest, so it is one-way and does not expose
    raw hardware identifiers to a license server log.  The same machine will
    always produce the same fingerprint (assuming hostname and MAC do not change).
    """
    hostname = socket.gethostname()

    # uuid.getnode() returns the MAC address as a 48-bit integer.
    # On machines where the hardware MAC cannot be determined the stdlib falls
    # back to a random 48-bit value seeded with the current time; that value is
    # not stable across reboots, but it is the best available cross-platform
    # option without requiring elevated privileges or third-party packages.
    mac_int = uuid.getnode()
    mac_str = ":".join(
        f"{(mac_int >> (8 * i)) & 0xFF:02x}" for i in range(5, -1, -1)
    )

    raw = f"{hostname}|{mac_str}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def check_license() -> bool:
    """
    Validate the current machine's license.

    STUB IMPLEMENTATION — always returns True.

    Replace this function body (ideally after obfuscating the file with PyArmor)
    with real validation logic before distributing a paid build.  A typical
    implementation would:
      - Read a license file bundled with the distribution or stored in the user's
        home directory.
      - Verify a cryptographic signature on that file using a public key embedded
        in the obfuscated source.
      - Optionally compare the license's locked machine-id field against
        get_machine_id() to enforce single-machine activation.
      - Return True only when all checks pass, False (or raise LicenseError)
        otherwise.
    """
    return True
