import httpx, logging
from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

async def send_slack(msg: str):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(settings.slack_webhook, json={"text": msg})
            resp.raise_for_status
    except httpx.RequestError as e:
        logger.error("Slack request failed: %s", e)
        return
    except httpx.HTTPStatusError as e:
        logger.error("Slack HTTP error: %s", e)
        return
    except Exception as e:
        logger.error("Unexpected error sending to Slack: %s", e)
        return