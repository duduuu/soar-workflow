import logging, asyncio
from fastapi import FastAPI, Request, BackgroundTasks
from .models import Event
from .cti import score_ip
from .notifier import send_slack

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
app = FastAPI(title="Mini SOAR Demo")

@app.post("/webhook")
async def webhook(event: Event, bg: BackgroundTasks):
    logging.info("Event received: %s", event.model_dump())

    async def triage():
        score = await score_ip(str(event.src_ip))
        logging.info("IP Score: %s", score)
        if score >= 50:
            await send_slack(f":rotating_light: 악성 IP 탐지 ➡ {event.src_ip} (score={score})")

    bg.add_task(triage)
    return {"status": "queued"}
