import json

with open('/Users/ltang/Downloads/www.lazada.sg.har', 'r') as f:
    har = json.load(f)

for entry in har['log']['entries']:
    url = entry['request']['url']
    if 'mtop.global.detail.web.getdetailinfo' in url:
        print("✅ FOUND THE PRODUCT API!")
        print("\n" + "="*80)
        print("URL:", url[:150])
        print("\nMethod:", entry['request']['method'])
        print("\nPost Data:")
        post_data = entry['request'].get('postData', {}).get('text', '')
        print(post_data[:500])
        print("\n\nHeaders:")
        for h in entry['request']['headers']:
            if h['name'].lower() in ['cookie', 'x-', 'referer', 'user-agent']:
                print(f"  {h['name']}: {h['value'][:80]}...")
        print("\n\nResponse Preview:")
        try:
            content = entry['response']['content'].get('text', '')
            if content:
                resp = json.loads(content)
                print(json.dumps(resp, indent=2)[:1000])
        except:
            print("  (binary or large response)")
        break
