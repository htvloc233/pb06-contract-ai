"""Cổng egress (DoD-4): request NGOÀI whitelist PHẢI bị chặn — bị chặn là PASS."""
import pytest

import src.egress_guard as eg
from src.egress_guard import EgressBlockedError, check, guarded_urlopen

ALLOWED = "api.allowed-example.com"


def _whitelist(monkeypatch, value):
    if value is None:
        monkeypatch.delenv("EGRESS_ALLOWED_HOSTS", raising=False)
    else:
        monkeypatch.setenv("EGRESS_ALLOWED_HOSTS", value)


def test_mac_dinh_dong_khi_khong_co_whitelist(monkeypatch):
    """Không cấu hình gì → chặn TẤT CẢ, kể cả host 'tốt'. Đây là luật lõi."""
    _whitelist(monkeypatch, None)
    with pytest.raises(EgressBlockedError):
        check(f"https://{ALLOWED}/v1")


def test_host_ngoai_whitelist_bi_chan(monkeypatch):
    _whitelist(monkeypatch, ALLOWED)
    with pytest.raises(EgressBlockedError):
        check("https://evil-collector.example.net/upload")


def test_subdomain_khong_duoc_suy_ra(monkeypatch):
    """Whitelist 'allowed-example.com' KHÔNG mở cửa cho 'api.allowed-example.com'."""
    _whitelist(monkeypatch, "allowed-example.com")
    with pytest.raises(EgressBlockedError):
        check(f"https://{ALLOWED}/v1")


def test_http_bi_chan_ke_ca_host_trong_whitelist(monkeypatch):
    _whitelist(monkeypatch, ALLOWED)
    with pytest.raises(EgressBlockedError):
        check(f"http://{ALLOWED}/v1")


def test_host_trong_whitelist_qua_cong(monkeypatch):
    _whitelist(monkeypatch, ALLOWED)
    check(f"https://{ALLOWED}/v1")  # không ném exception = qua cổng


def test_guarded_urlopen_chi_cham_transport_khi_qua_cong(monkeypatch):
    """Bị chặn thì KHÔNG được chạm tới tầng mạng — chặn trước, không chặn sau."""
    _whitelist(monkeypatch, ALLOWED)
    called = {}

    def fake_urlopen(url, timeout=None, **kw):
        called["url"] = url
        return "OK-STUB"

    monkeypatch.setattr(eg.urllib.request, "urlopen", fake_urlopen)
    assert guarded_urlopen(f"https://{ALLOWED}/v1") == "OK-STUB"
    assert called["url"] == f"https://{ALLOWED}/v1"

    called.clear()
    with pytest.raises(EgressBlockedError):
        guarded_urlopen("https://evil.example.net/x")
    assert called == {}, "Bị chặn mà vẫn chạm transport = cổng giả"
