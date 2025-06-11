import httpx, logging
from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

async def send_slack(msg: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(settings.slack_webhook, json={"text": msg})
    if resp.status_code != 200:
        logger.error("Slack failed (%s): %s", resp.status_code, resp.text)