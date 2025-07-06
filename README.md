# FastAPI/Uvicorn JSON Logger Config

Example for overriding the uvicorn logger to output logs in JSON:

```json
{"system": "uvicorn", "timestamp": "2025-07-06T20:50:47.793969Z", "level": "INFO", "event": "Started server process [135051]"}
{"system": "uvicorn", "timestamp": "2025-07-06T20:50:47.794057Z", "level": "INFO", "event": "Waiting for application startup."}
{"system": "uvicorn", "timestamp": "2025-07-06T20:50:47.794169Z", "level": "INFO", "event": "Application startup complete."}
{"system": "uvicorn", "timestamp": "2025-07-06T20:50:47.796156Z", "level": "INFO", "event": "Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"}
{"system": "uvicorn.access", "timestamp": "2025-07-06T20:52:05.747763Z", "level": "INFO", "http": {"method": "GET", "path": "/", "status_code": 200, "client": "127.0.0.1:33546", "version": "HTTP/1.1"}}
{"system": "uvicorn.access", "timestamp": "2025-07-06T20:52:05.759917Z", "level": "INFO", "http": {"method": "GET", "path": "/favicon.ico", "status_code": 404, "client": "127.0.0.1:33548", "version": "HTTP/1.1"}}
```

Compared to the original uvicorn logs:

```text
INFO:     Started server process [136549]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:50980 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:50986 - "GET /favicon.ico HTTP/1.1" 404 Not Found
```