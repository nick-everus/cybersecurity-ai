import yara

# Compile YARA rules
rules = yara.compile(filepath="malware_rules.yara")

# Scan a file for malware patterns
matches = rules.match("/path/to/suspicious/file")

# Check if any rule matches
if matches:
    print(f"Malware detected: {matches}")
else:
    print("No malware detected.")