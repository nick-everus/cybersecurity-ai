import dns.resolver

# List of known malicious domains
malicious_domains = ["example-malicious.com", "bad-domain.org"]

def monitor_dns_queries():
    # Simulate DNS query monitoring
    queries = ["google.com", "example-malicious.com", "bad-domain.org"]

    for query in queries:
        if query in malicious_domains:
            print(f"Alert! Query to malicious domain: {query}")

if __name__ == "__main__":
    monitor_dns_queries()