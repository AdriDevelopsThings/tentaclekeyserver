from flask import request

from resources.config import X_FORWARDED_HEADER_FIELD, CLOUDFLARE


def get_remote_address() -> str:
    addr = request.remote_addr
    if X_FORWARDED_HEADER_FIELD:
        addr = request.headers[X_FORWARDED_HEADER_FIELD] or addr
    elif CLOUDFLARE:
        addr = request.headers["CF-Connecting-IP"] or addr
    return addr
