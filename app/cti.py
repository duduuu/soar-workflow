import httpx, asyncio, logging
import random
from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

HEADERS = {
    "abuseipdb": {"Key": settings.cti_api_key, "Accept": "application/json"},
    "virustotal": {"x-apikey": settings.cti_api_key},
}

URLS = {
    "abuseipdb": "https://api.abuseipdb.com/api/v2/check",
    "virustotal": "https://www.virustotal.com/api/v3/ip_addresses/{ip}",
}

async def score_ip(ip: str) -> int:
    provider = settings.cti_provider
    
    if provider == "mock":
        score = random.choice([random.randint(70, 100)] * 2 + [random.randint(0, 40)] * 8)
        logging.info("[MOCK] %s → score=%s", ip, score)
        return score
    
    url = URLS[provider].format(ip=ip)
    params = {"ipAddress": ip} if provider == "abuseipdb" else {}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, headers=HEADERS[provider], params=params)
    resp.raise_for_status()
    data = resp.json()

    if provider == "abuseipdb":
        return data["data"]["abuseConfidenceScore"]
    else:  # VirusTotal
        return data["data"]["attributes"]["last_analysis_stats"]["malicious"]
