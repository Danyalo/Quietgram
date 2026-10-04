#!/usr/bin/env python3
"""Align and sign an unsigned Quietgram candidate using a local release key."""
import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('apk', type=Path)
parser.add_argument('key_directory', type=Path)
parser.add_argument('output', type=Path)
parser.add_argument('--sdk', type=Path, default=os.environ.get('ANDROID_HOME'))
args = parser.parse_args()
if args.sdk is None:
    parser.error('Set ANDROID_HOME or pass --sdk')
apk, output = args.apk.resolve(), args.output.resolve()
key_directory = args.key_directory.resolve()
if output.exists() or output == apk:
    parser.error('Output must be a new file')
tools = args.sdk / 'build-tools' / '36.0.0'
badging = subprocess.check_output([str(tools / 'aapt'), 'dump', 'badging', str(apk)], text=True)
if "name='io.github.danyalo.quietgram'" not in badging or "application-label:'Quietgram'" not in badging:
    parser.error('Input APK must have Quietgram identity')
if subprocess.run([str(tools / 'apksigner'), 'verify', str(apk)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
    parser.error('Input APK already has a signature')
output.parent.mkdir(parents=True, exist_ok=True)
aligned = output.with_suffix('.aligned.apk')
if aligned.exists():
    parser.error('Temporary aligned APK already exists')
try:
    subprocess.run([str(tools / 'zipalign'), '-P', '16', '-f', '4', str(apk), str(aligned)], check=True)
    subprocess.run([
        str(tools / 'apksigner'), 'sign',
        '--ks', str(key_directory / 'quietgram-release.p12'), '--ks-key-alias', 'quietgram',
        '--ks-pass', 'file:' + str(key_directory / 'signing-password.txt'),
        # PKCS12 uses the store password for the key as well.
        '--v4-signing-enabled', 'false', '--out', str(output), str(aligned),
    ], check=True)
    verification = subprocess.check_output([
        str(tools / 'apksigner'), 'verify', '--verbose', '--print-certs', str(output),
    ], text=True)
    actual = re.search(r'Signer #1 certificate SHA-256 digest: ([0-9a-fA-F]+)', verification)
    expected = (key_directory / 'certificate-sha256.txt').read_text().strip().lower()
    if not actual or actual.group(1).lower() != expected:
        raise SystemExit('Signing certificate does not match the saved release identity')
    subprocess.run([str(tools / 'zipalign'), '-c', '-P', '16', '4', str(output)], check=True)
    output.with_suffix('.verification.txt').write_text(verification)
    with output.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    output.with_suffix('.sha256').write_text(f'{digest}  {output.name}\n')
    print('Signed APK verified:', output)
    print('Public certificate SHA-256:', expected)
finally:
    aligned.unlink(missing_ok=True)
