from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

import sentry_sdk

sentry_sdk.init(
    dsn="https://fc691f0750584fa4a78c0c70dc7be768@o4509959101480960.ingest.us.sentry.io/4509959103512576",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

app = FastAPI(
    title="SmartNotes AI API",
    description="Realtime Note Editor with AI",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)