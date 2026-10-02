"""
Mini Project 1.3: 0G-6G Generation Validation and Recommender
CE80762 Mobile Communications - Unit 1
"""

# ---------------------------------------------------------------
# Keyword -> generation mapping
# ---------------------------------------------------------------
GENERATION_KEYWORDS = {
    "1G": [
        "analog", "analogue", "amps", "nmt", "tacs",
        "first generation", "1g", "basic voice", "analog voice"
    ],
    "2G": [
        "digital voice", "sms", "gsm", "is-95", "cdmaone",
        "second generation", "2g", "sim", "encryption",
        "digital cellular"
    ],
    "2.5G": [
        "gprs", "edge", "packet data", "always on",
        "2.5g", "2.75g", "early mobile internet", "wap"
    ],
    "3G": [
        "mobile broadband", "video calling", "umts", "wcdma",
        "cdma2000", "hspa", "imt-2000", "3g",
        "third generation", "mobile internet"
    ],
    "4G": [
        "lte", "volte", "all-ip", "ofdma", "mimo",
        "4g", "fourth generation", "mobile broadband",
        "high speed data"
    ],
    "5G": [
        "low latency", "urllc", "embb", "mmtc", "iot",
        "massive mimo", "network slicing", "5g",
        "fifth generation", "robotic arm", "autonomous",
        "industrial automation", "remote surgery"
    ],
    "6G": [
        "terahertz", "ai-native", "integrated sensing",
        "reconfigurable intelligent surface", "ris",
        "6g", "sixth generation", "holographic",
        "immersive communication", "ubiquitous connectivity"
    ],
}

GENERATION_EXPLANATIONS = {
    "1G": "1G introduced analog cellular voice (AMPS, NMT, TACS).",
    "2G": "2G brought digital voice, SMS, and SIM-based security (GSM, IS-95).",
    "2.5G": "2.5G added packet-switched data to 2G (GPRS, EDGE).",
    "3G": "3G enabled mobile broadband and video calling (UMTS, CDMA2000).",
    "4G": "4G delivered all-IP mobile broadband with VoLTE and OFDMA.",
    "5G": "5G supports eMBB, URLLC, and mMTC use cases (5G NR).",
    "6G": "6G research targets AI-native networks, sensing, and terahertz.",
}


def recommend_generation(requirement: str):
    """Return (generation, matched_keywords, explanation) or no-match."""
    text = requirement.lower()
    scores = {}
    matches = {}

    for gen, keywords in GENERATION_KEYWORDS.items():
        hits = [kw for kw in keywords if kw in text]
        if hits:
            scores[gen] = len(hits)
            matches[gen] = hits

    if not scores:
        return None, [], "No clear match to a single generation."

    best = max(scores, key=scores.get)
    return best, matches[best], GENERATION_EXPLANATIONS[best]


# ---------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------
TEST_CASES = [
    "Basic analog mobile voice service",
    "Digital cellular voice and SMS",
    "Packet data and early mobile Internet using GPRS",
    "Mobile broadband and video calling",
    "Low-latency control for a robotic arm",
    "Integrated sensing and extremely high data rates",
    "General mobile connectivity without generation-specific terms",
]

print("=" * 78)
print(f"{'Test requirement':<50}{'Result'}")
print("=" * 78)

for req in TEST_CASES:
    gen, hits, expl = recommend_generation(req)
    label = gen if gen else "No clear match"
    print(f"{req:<50}{label}")
    if hits:
        print(f"   matched: {', '.join(hits)}")
    print(f"   -> {expl}\n")