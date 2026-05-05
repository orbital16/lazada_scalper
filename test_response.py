import json

# Load the HAR file and extract the actual response
with open('/Users/ltang/Downloads/www.lazada.sg.har', 'r') as f:
    har = json.load(f)

for entry in har['log']['entries']:
    if 'mtop.global.detail.web.getdetailinfo' in entry['request']['url']:
        content = entry['response']['content'].get('text', '')
        if content:
            response = json.loads(content)
            
            print("ACTUAL RESPONSE STRUCTURE:")
            print("=" * 80)
            print(json.dumps(response, indent=2)[:3000])
            
            # Save full response
            with open('response_sample.json', 'w') as out:
                json.dump(response, out, indent=2)
            
            print("\n\n✅ Saved full response to response_sample.json")
            break
