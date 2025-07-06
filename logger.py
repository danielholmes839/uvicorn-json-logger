import logging
import json
from datetime import datetime, timezone


class UvicornJSONLogFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(
            {
                "system": "uvicorn",
                "timestamp": format_timestamp(record.created),
                "level": record.levelname,
                "event": record.msg % record.args,
            }
        )


class UvicornJSONAccessLogFormatter(logging.Formatter):
    def format(self, record):
        (client, method, path, http_version, status_code) = record.args

        return json.dumps(
            {
                "system": "uvicorn.access",
                "timestamp": format_timestamp(record.created),
                "level": record.levelname,
                "http": {
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "client": client,
                    "version": "HTTP/" + http_version,
                },
            }
        )


def format_timestamp(created: float) -> str:
    dt = datetime.fromtimestamp(created, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": UvicornJSONLogFormatter,
        },
        "access": {
            "()": UvicornJSONAccessLogFormatter,
        },
    },
    "filters": {},
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},  # propagates to the "uvicorn" logger above
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
