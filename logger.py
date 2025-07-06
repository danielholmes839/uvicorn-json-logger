import logging
import json
import structlog
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


def format_uvicorn_events(_logger, _name, event_dict):
    record = event_dict["_record"]

    return {
        "system": "uvicorn",
        "timestamp": format_timestamp(record.created),
        "level": record.levelname,
        "event": event_dict["event"],
    }


def format_uvicorn_access_events(_logger, _name, event_dict):
    (client, method, path, http_version, status_code) = event_dict["positional_args"]

    record = event_dict["_record"]

    return {
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

STDLIB_FORMATTERS = {
    "default": {
        "()": UvicornJSONLogFormatter,
    },
    "access": {
        "()": UvicornJSONAccessLogFormatter,
    },
}

STRUCTLOG_FORMATTERS = {
    "default": {
        "()": structlog.stdlib.ProcessorFormatter,
        "processors": [format_uvicorn_events, structlog.processors.JSONRenderer()],
    },
    "access": {
        "()": structlog.stdlib.ProcessorFormatter,
        "processors": [
            format_uvicorn_access_events,
            structlog.processors.JSONRenderer(),
        ],
        "pass_foreign_args": True,
    },
}

UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": STDLIB_FORMATTERS,
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