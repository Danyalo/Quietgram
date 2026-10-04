#!/usr/bin/env python3
"""Create an encrypted release keystore outside the source checkout."""
import argparse
import base64
import hashlib
import os
from pathlib import Path
import secrets
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('directory', type=Path, help='New private output directory outside this checkout')
args = parser.parse_args()
directory = args.directory.resolve()
checkout = Path(__file__).resolve().parents[1]
if directory == checkout or checkout in directory.parents:
    parser.error('Keep release keys outside the source checkout')
os.umask(0o077)
directory.mkdir(mode=0o700, parents=True, exist_ok=False)
password = directory / 'signing-password.txt'
password.write_text(secrets.token_hex(32) + '\n')
keystore = directory / 'quietgram-release.p12'
result = subprocess.run([
    'keytool', '-genkeypair', '-noprompt', '-storetype', 'PKCS12',
    '-keystore', str(keystore), '-alias', 'quietgram', '-keyalg', 'RSA',
    '-keysize', '4096', '-validity', '36500', '-dname', 'CN=Quietgram',
    '-storepass:file', str(password), '-keypass:file', str(password),
])
if result.returncode:
    raise SystemExit(result.returncode)
certificate = directory / 'quietgram-certificate.der'
subprocess.run([
    'keytool', '-exportcert', '-keystore', str(keystore), '-alias', 'quietgram',
    '-storepass:file', str(password), '-file', str(certificate),
], check=True)
fingerprint = hashlib.sha256(certificate.read_bytes()).hexdigest()
(directory / 'certificate-sha256.txt').write_text(fingerprint + '\n')
(directory / 'keystore-base64.txt').write_text(base64.b64encode(keystore.read_bytes()).decode() + '\n')
(directory / 'README.txt').write_text(
    'Quietgram private signing backup\n\n'
    'Keep quietgram-release.p12 and signing-password.txt in a private password vault or encrypted backup. '
    'The PKCS12 keystore is encrypted; the password file is plain text. '
    'The base64 file contains the same encrypted keystore for optional GitHub Actions secret setup. '
    'Do not commit or upload these files publicly.\n\n'
    'Key alias: quietgram\n'
    'Store and key password: contents of signing-password.txt\n'
    f'Public certificate SHA-256: {fingerprint}\n'
)
print('Encrypted signing key created. No passwords or private key material printed.')
print('Public certificate SHA-256:', fingerprint)
