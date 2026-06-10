import re

# =====================================================
# PSEUDONYMIZER
# =====================================================

class Pseudonymizer:
    def __init__(self):
        self.people  = {}
        self.counter = 1

    def get_user(self, name):
        name = str(name).strip().lower()

        if name not in self.people:
            self.people[name] = f"USER_{self.counter:05d}"
            self.counter += 1

        return self.people[name]

# =====================================================
# ANONYMIZER
# =====================================================

def anonymize_text(text):
    if text is None:
        return ""

    text = str(text)

    # email
    text = re.sub(r'(?i)[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}', 'EMAIL_MASKED', text)

    # url
    text = re.sub(r'https?://\S+|www\.\S+', 'URL_MASKED', text, flags=re.IGNORECASE)

    # ip address
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', 'IP_MASKED', text)

    # nomor hp indonesia
    text = re.sub(r'(?<!\d)(?:\+62|62|0)8\d{8,13}(?!\d)', 'PHONE_MASKED', text)

    # NIP 18 digit
    text = re.sub(r'(?<!\d)\d{18}(?!\d)', 'NIP_MASKED', text)

    # NPWP 15-16 digit
    text = re.sub(r'(?<!\d)\d{15,16}(?!\d)', 'NPWP_MASKED', text)

    # rekening 10-20 digit
    text = re.sub(r'(?<!\d)\d{10,20}(?!\d)', 'ACCOUNT_MASKED', text)

    # username
    text = re.sub(r'(?i)\b(username|userid|user\s*id|user)\s*[:=]?\s*[a-z0-9._\-]+\b', 'USERNAME_MASKED', text)

    # sapaan formal
    sapaan_patterns = [
        r'(?i)(yth\.?\s+bapak\s+)([A-Za-z][A-Za-z\s]{1,40})',
        r'(?i)(yth\.?\s+ibu\s+)([A-Za-z][A-Za-z\s]{1,40})',
        r'(?i)(yth\.?\s+saudara\s+)([A-Za-z][A-Za-z\s]{1,40})',
        r'(?i)(kepada\s+bapak\s+)([A-Za-z][A-Za-z\s]{1,40})',
        r'(?i)(kepada\s+ibu\s+)([A-Za-z][A-Za-z\s]{1,40})',
        r'(?i)(dear\s+pak\s+)([A-Za-z][A-Za-z\s]{1,40})',
        r'(?i)(dear\s+bu\s+)([A-Za-z][A-Za-z\s]{1,40})',
    ]
    for pattern in sapaan_patterns:
        text = re.sub(pattern, lambda m: f"{m.group(1)}PERSON_MASKED", text)

    # user code
    text = re.sub(r'(?i)\b(?:opr|operator|usr|user)_[a-z0-9_]+\b', 'USERCODE_MASKED', text)

    # normalisasi spasi
    text = re.sub(r'\s+', ' ', text).strip()

    return text