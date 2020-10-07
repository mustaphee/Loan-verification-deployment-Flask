import uvicorn
uvicorn.run("app.app:app", host="127.0.0.1", port=6671, log_level="info")
