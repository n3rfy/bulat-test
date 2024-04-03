from __future__ import annotations

import enum
import json
import logging
from datetime import datetime
from typing import TextIO

import structlog


def set_message_field(_, __, event_dict: dict) -> dict:
    if 'message' in event_dict:
        return event_dict
    event_dict['message'] = event_dict['event']
    return event_dict


def set_level_field(_, method_name, event_dict: dict) -> dict:
    if 'level' in event_dict:
        return event_dict
    level = {
        'debug': 'DEBUG',
        'info': 'INFO',
        'msg': 'INFO',
        'warn': 'WARN',
        'warning': 'WARN',
        'err': 'ERROR',
        'error': 'ERROR',
        'exception': 'ERROR',
        'fatal': 'FATAL',
        'critical': 'FATAL',
    }.get(method_name, 'INFO')
    event_dict['level'] = level
    return event_dict


def set_timestamp(_, __, event: dict) -> dict:
    event['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return event


def serialize_enums(_, __, event_dict: dict) -> dict:
    for key, value in event_dict.items():
        if isinstance(value, enum.Enum):
            event_dict[key] = value.value
    return event_dict


def setup_logging(log_file: TextIO) -> None:
    processors = [
        set_timestamp,
        serialize_enums,
        structlog.processors.format_exc_info,
    ]
    processors.insert(0, set_message_field)
    processors.insert(0, set_level_field)
    structlog.configure(
        processors=[*processors, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(
                serializer=json.dumps,
                ensure_ascii=False,
            ),
        ],
    )
    steam_handler = logging.StreamHandler()
    steam_handler.setFormatter(formatter)

    file_handler = logging.StreamHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logger.addHandler(steam_handler)
    logger.addHandler(file_handler)
