import re
from urllib.parse import urlparse

# List of common phishing keywords
PHISHING_KEYWORDS = ["urgent", "important", "verify", "password", "account", "login", "click", "immediately",
                     "security"]

# List of common trusted domains (can be extended)
TRUSTED_DOMAINS = ["gmail.com", "yahoo.com", "microsoft.com", "apple.com"]


# Function to check if the email contains suspicious URLs
def detect_suspicious_urls(email_text):
    # Regex pattern to find URLs
    url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    urls = re.findall(url_pattern, email_text)
    suspicious_urls = []

    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Check if the domain is in the list of trusted domains
        if not any(trusted_domain in domain for trusted_domain in TRUSTED_DOMAINS):
            suspicious_urls.append(url)

    return suspicious_urls


# Function to check for phishing keywords
def detect_phishing_keywords(email_text):
    email_text_lower = email_text.lower()
    detected_keywords = [word for word in PHISHING_KEYWORDS if word in email_text_lower]
    return detected_keywords


# Function to check the email sender address for phishing (e.g., mismatched domains)
def check_sender_address(sender_email):
    # Simple check for common free email services vs. corporate emails
    sender_domain = sender_email.split('@')[-1]

    if sender_domain not in TRUSTED_DOMAINS:
        return f"Suspicious sender domain: {sender_domain}"
    return None


# Function to check for requests for sensitive information
def detect_sensitive_info_requests(email_text):
    sensitive_phrases = ["social security", "credit card", "password", "PIN", "security number"]
    detected_phrases = [phrase for phrase in sensitive_phrases if phrase in email_text.lower()]
    return detected_phrases


# Main function to analyze email for phishing
def analyze_email(sender_email, email_text):
    phishing_indicators = {
        "suspicious_urls": detect_suspicious_urls(email_text),
        "phishing_keywords": detect_phishing_keywords(email_text),
        "sender_check": check_sender_address(sender_email),
        "sensitive_info_requests": detect_sensitive_info_requests(email_text)
    }

    # Determine if the email is potentially phishing
    phishing_flags = [indicator for key, indicator in phishing_indicators.items() if indicator]

    if phishing_flags:
        print("Potential phishing email detected!")
        for key, indicator in phishing_indicators.items():
            if indicator:
                print(f"{key.capitalize()}: {indicator}")
    else:
        print("No phishing indicators found.")


# Test the script with an email sample
email_sample_text = """
Hello,

We noticed some unusual activity on your account. To protect your account, we need you to verify your login information immediately by clicking the link below:

http://example-phishing-site.com/login

Failure to do so will result in the suspension of your account.

Thank you,
Security Team
"""

sender_email_sample = "support@example-phishing-site.com"

# Run the phishing detection on the sample email
analyze_email(sender_email_sample, email_sample_text)