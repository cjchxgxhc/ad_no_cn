import urllib.request

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, domain):
        node = self.root
        # Reverse domain parts for suffix matching (e.g., example.com -> com.example)
        parts = domain.split('.')[::-1]
        for part in parts:
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]
        node.is_end = True

    def is_subdomain_or_exact(self, domain):
        # Check if domain or its subdomains match any in Trie
        parts = domain.split('.')[::-1]
        node = self.root
        for part in parts:
            if part not in node.children:
                return False
            node = node.children[part]
            if node.is_end:
                return True
        return False

def fetch_and_filter():
    # Fetch CN direct list
    cn_url = 'https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/direct-list.txt'
    try:
        with urllib.request.urlopen(cn_url) as response:
            cn_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching CN list: {e}")
        return

    # Build Trie for CN domains
    trie = Trie()
    cn_domains = set()
    for line in cn_data.splitlines():
        line = line.strip().lower()
        if line and not line.startswith(('#', '!')):
            cn_domains.add(line)
            trie.insert(line)

    # Ad blocklist URLs
    ad_urls = [
        ('https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro-onlydomains.txt', 'filtered_pro_domains.txt'),
        ('https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro.mini-onlydomains.txt', 'filtered_pro_mini_domains.txt')
    ]

    for ad_url, output_file in ad_urls:
        # Fetch ad blocklist
        try:
            with urllib.request.urlopen(ad_url) as response:
                ad_data = response.read().decode('utf-8')
        except Exception as e:
            print(f"Error fetching ad blocklist {ad_url}: {e}")
            continue

        # Process ad domains into a set
        ad_domains = set()
        for line in ad_data.splitlines():
            line = line.strip().lower()
            if line and not line.startswith(('#', '!')):
                ad_domains.add(line)

        # Filter ad domains
        filtered_ad = set()
        for ad in ad_domains:
            if not trie.is_subdomain_or_exact(ad):
                filtered_ad.add(ad)

        # Sort the filtered list for consistent output
        filtered_list = sorted(filtered_ad)

        # Output to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(filtered_list) + '\n')

        print(f"Filtered domains saved to {output_file}")
        print(f"Original ad domains for {ad_url}: {len(ad_domains)}")
        print(f"CN domains: {len(cn_domains)}")
        print(f"Filtered ad domains: {len(filtered_list)}")

if __name__ == "__main__":
    fetch_and_filter()
