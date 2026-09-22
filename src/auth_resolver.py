"""L0-Auth permission resolver — W1-02.

Nguồn sự thật: DECISION-D11-PB06 (5 role, Q1 per-contract, Q2 upload, Q3 approve∈write)
+ ARCH v1.5 §6 (404-not-403) + SPEC v1.1 (AC-01, AC-03-4, AC-08-4, ma trận UC §5.0).

Nguyên tắc 403-vs-404 (ARCH 6.2):
- Người BIẾT hợp đồng tồn tại (có role trên nó) nhưng thiếu quyền hành động -> FORBIDDEN (403).
- Người KHÔNG được biết đối tượng tồn tại (không role, hoặc draft với người chỉ-đọc)
  -> NOT_FOUND (404) — không xác nhận cả sự tồn tại.
"""
from __future__ import annotations

# --- Role (DECISION-D11 §1) ---
ROLE_OWNER = "contract_owner"
ROLE_EDITOR = "contract_editor"
ROLE_VIEWER = "contract_viewer"
PER_CONTRACT_ROLES = frozenset({ROLE_OWNER, ROLE_EDITOR, ROLE_VIEWER})

# --- Permission (ARCH 6.2) ---
P_READ = "contract:read"
P_WRITE = "contract:write"
P_AUDIT = "audit:read"

# --- Ket qua phan quyet ---
ALLOW = "allow"
FORBIDDEN = "forbidden_403"
NOT_FOUND = "not_found_404"

# --- Trang thai ket qua phan tich ---
STATUS_DRAFT = "draft_ai"
STATUS_APPROVED = "approved"


def resolve_permissions(role: str | None, *, is_pm_admin: bool = False) -> frozenset:
    """Role trên MỘT hợp đồng cụ thể (Q1: per-contract) -> tập permission."""
    perms = set()
    if role in (ROLE_OWNER, ROLE_EDITOR):
        perms |= {P_READ, P_WRITE}          # Q3: approve thuộc write, không tách
    elif role == ROLE_VIEWER:
        perms.add(P_READ)
    if is_pm_admin:
        perms |= {P_READ, P_AUDIT}          # pm_admin: đọc approved + audit, KHÔNG write
    return frozenset(perms)


def decide_trigger_analyze(role: str | None, *, is_pm_admin: bool = False) -> str:
    """Bấm 'Phân tích bằng AI' trên hợp đồng (AC-03-4)."""
    if role in (ROLE_OWNER, ROLE_EDITOR):
        return ALLOW
    if role == ROLE_VIEWER or is_pm_admin:
        return FORBIDDEN                     # biết HĐ tồn tại, thiếu write -> 403
    return NOT_FOUND                         # không role -> che cả sự tồn tại


def decide_read_result(role: str | None, result_status: str,
                       *, is_pm_admin: bool = False) -> str:
    """Xem một kết quả phân tích theo trạng thái của nó (AC-01, ARCH 6.2)."""
    perms = resolve_permissions(role, is_pm_admin=is_pm_admin)
    if P_READ not in perms:
        return NOT_FOUND
    if result_status == STATUS_APPROVED:
        return ALLOW
    if result_status == STATUS_DRAFT:
        if P_WRITE in perms:
            return ALLOW                     # owner/editor thấy draft
        return NOT_FOUND                     # viewer/pm_admin: draft vô hình — 404, KHÔNG 403
    return NOT_FOUND


def decide_write_result(role: str | None, result_status: str,
                        *, is_pm_admin: bool = False) -> str:
    """Sửa trường / sửa tóm tắt / approve / re-analyze trên một kết quả (AC-08-4)."""
    visibility = decide_read_result(role, result_status, is_pm_admin=is_pm_admin)
    if visibility is NOT_FOUND:
        return NOT_FOUND                     # không thấy thì không có gì để bị cấm
    perms = resolve_permissions(role, is_pm_admin=is_pm_admin)
    return ALLOW if P_WRITE in perms else FORBIDDEN


def can_upload_contract(role: str | None) -> bool:
    """Q2: upload/tạo hợp đồng mới = owner hoặc editor."""
    return role in (ROLE_OWNER, ROLE_EDITOR)


def decide_audit_read(*, is_pm_admin: bool = False) -> str:
    """S6 Audit UI: chỉ pm_admin (US-11)."""
    return ALLOW if is_pm_admin else FORBIDDEN
