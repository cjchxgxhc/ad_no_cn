import urllib.request

def fetch_and_filter():
    # Fetch ad blocklist
    ad_url = 'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro.mini-onlydomains.txt'
    try:
        with urllib.request.urlopen(ad_url) as response:
            ad_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching ad blocklist: {e}")
        return

    # Fetch CN direct list
    cn_url = 'https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/direct-list.txt'
    try:
        with urllib.request.urlopen(cn_url) as response:
            cn_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching CN list: {e}")
        return

    # Process ad domains into a set for fast lookup and removal
    ad_domains = set()
    for line in ad_data.splitlines():
        line = line.strip().lower()
        if line and not line.startswith(('#', '!')):
            ad_domains.add(line)

    # Process CN domains into a set
    cn_domains = set()
    for line in cn_data.splitlines():
        line = line.strip().lower()
        if line and not line.startswith(('#', '!')):
            cn_domains.add(line)

    # Filter: remove ad domains that are equal to or subdomains of CN domains
    to_remove = set()
    for ad in ad_domains:
        for cn in cn_domains:
            if ad == cn or ad.endswith('.' + cn):
                to_remove.add(ad)
                break

    filtered_ad = ad_domains - to_remove

    # Sort the filtered list for consistent output
    filtered_list = sorted(filtered_ad)

    # Output to file
    output_file = 'filtered_ad_domains.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(filtered_list) + '\n')

    print(f"Filtered domains saved to {output_file}")
    print(f"Original ad domains: {len(ad_domains)}")
    print(f"CN domains: {len(cn_domains)}")
    print(f"Filtered ad domains: {len(filtered_list)}")

if __name__ == "__main__":
    fetch_and_filter()
