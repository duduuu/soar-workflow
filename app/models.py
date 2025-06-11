from pydantic import BaseModel, IPvAnyAddress

class Event(BaseModel):
    src_ip: IPvAnyAddress
    dest_ip: IPvAnyAddress | None = None
    signature: str | None = None