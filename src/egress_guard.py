"""Egress guard — cổng fail-closed cho mọi request ra ngoài AI service.

Neo: DoD-4 · RISK B1 (điểm 20) · Delegation R3 · NFR-S1/S2.
Nguyên tắc: MẶC ĐỊNH ĐÓNG — whitelist rỗng nghĩa là không gì được ra.
Quyết định chặn/cho là hàm thuần (check), KHÔNG gọi mạng — test được offline.
"""
import os
import urllib.request
from urllib.parse import urlparse


class EgressBlockedError(Exception):
    """Request bị egress guard chặn."""


def _allowed_hosts() -> frozenset:
    raw = os.environ.get("EGRESS_ALLOWED_HOSTS", "")
    return frozenset(h.strip().lower() for h in raw.split(",") if h.strip())


def check(url: str) -> None:
    """Ném EgressBlockedError nếu url không được phép. Không gọi mạng.

    Luật: chỉ https · whitelist rỗng = chặn tất cả (mặc định đóng)
    · khớp ĐÚNG host, không suy ra subdomain (chặt hơn = an toàn hơn).
    """
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https":
        raise EgressBlockedError(
            f"Chỉ cho phép https, nhận {parsed.scheme!r} trong {url!r}"
        )
    allowed = _allowed_hosts()
    if not allowed:
        raise EgressBlockedError(
            "Whitelist rỗng — mặc định đóng, mọi egress bị chặn (DoD-4)"
        )
    if host not in allowed:
        raise EgressBlockedError(f"Host {host!r} không nằm trong whitelist")


def guarded_urlopen(url: str, timeout: float = 30, **kw):
    """Đường ra mạng DUY NHẤT được phép dùng trong AI service (R3)."""
    check(url)
    return urllib.request.urlopen(url, timeout=timeout, **kw)
