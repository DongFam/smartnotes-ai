from typing import Union
from fastapi import FastAPI
import sentry_sdk

sentry_sdk.init(
    dsn="https://fc691f0750584fa4a78c0c70dc7be768@o4509959101480960.ingest.us.sentry.io/4509959103512576",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}