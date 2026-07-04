from fastapi import FastAPI

app = FastAPI(title="VisionSearch")


@app.get("/health")
def health_check():
    return {"status": "ok"}
