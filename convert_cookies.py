#!/usr/bin/env python3
"""Convert Netscape cookies to JSON format"""

import json

def convert_netscape_to_json(netscape_file, json_file):
    """Convert Netscape cookie format to JSON"""
    cookies = []

    with open(netscape_file, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse cookie line
            parts = line.split('\t')
            if len(parts) < 7:
                continue

            domain, _, path, secure, expiry, name, value = parts

            cookie = {
                'name': name,
                'value': value,
                'domain': domain,
                'path': path,
                'secure': secure == 'TRUE',
                'httpOnly': False,
                'sameSite': 'None' if secure == 'TRUE' else 'Lax'
            }

            cookies.append(cookie)

    # Save as JSON
    with open(json_file, 'w') as f:
        json.dump(cookies, f, indent=2)

    print(f"✅ Converted {len(cookies)} cookies")
    print(f"   From: {netscape_file}")
    print(f"   To: {json_file}")

    return cookies

if __name__ == '__main__':
    convert_netscape_to_json(
        '/Users/ltang/Downloads/www.lazada.sg_cookies.txt',
        'lazada_cookies.json'
    )
