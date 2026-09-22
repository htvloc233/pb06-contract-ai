"""W1-02 — test resolver theo DECISION-D11 + ma trận UC SPEC §5.0.

Đọc-review kiểu PM: mỗi tên test là một dòng của ma trận quyền; test 'đắt' nhất
là các test 404-vs-403 — chúng khoá đúng nguyên tắc che-sự-tồn-tại của ARCH 6.2.
"""
from src.auth_resolver import (
    ALLOW,
    FORBIDDEN,
    NOT_FOUND,
    ROLE_EDITOR,
    ROLE_OWNER,
    ROLE_VIEWER,
    STATUS_APPROVED,
    STATUS_DRAFT,
    can_upload_contract,
    decide_audit_read,
    decide_read_result,
    decide_trigger_analyze,
    decide_write_result,
    resolve_permissions,
)


# --- Q3: approve thuộc write ---
def test_owner_va_editor_co_write_gom_ca_approve():
    for r in (ROLE_OWNER, ROLE_EDITOR):
        assert "contract:write" in resolve_permissions(r)

def test_viewer_chi_co_read():
    assert resolve_permissions(ROLE_VIEWER) == frozenset({"contract:read"})

# --- Trigger phân tích (AC-03-4) ---
def test_owner_editor_trigger_duoc():
    assert decide_trigger_analyze(ROLE_OWNER) is ALLOW
    assert decide_trigger_analyze(ROLE_EDITOR) is ALLOW

def test_viewer_trigger_bi_403_vi_biet_hd_ton_tai():
    assert decide_trigger_analyze(ROLE_VIEWER) is FORBIDDEN

def test_khong_role_trigger_bi_404_che_ca_su_ton_tai():
    assert decide_trigger_analyze(None) is NOT_FOUND

# --- Đọc kết quả: draft vô hình với người chỉ-đọc (ARCH 6.2) ---
def test_owner_thay_draft():
    assert decide_read_result(ROLE_OWNER, STATUS_DRAFT) is ALLOW

def test_viewer_doc_approved_duoc():
    assert decide_read_result(ROLE_VIEWER, STATUS_APPROVED) is ALLOW

def test_viewer_hoi_draft_nhan_404_khong_phai_403():
    assert decide_read_result(ROLE_VIEWER, STATUS_DRAFT) is NOT_FOUND

def test_khong_role_moi_thu_deu_404():
    assert decide_read_result(None, STATUS_APPROVED) is NOT_FOUND
    assert decide_read_result(None, STATUS_DRAFT) is NOT_FOUND

# --- pm_admin (UC-03): đọc approved + audit, không sửa, không thấy draft ---
def test_pm_admin_doc_approved_moi_hd():
    assert decide_read_result(None, STATUS_APPROVED, is_pm_admin=True) is ALLOW

def test_pm_admin_khong_thay_draft():
    assert decide_read_result(None, STATUS_DRAFT, is_pm_admin=True) is NOT_FOUND

def test_pm_admin_khong_duoc_sua_du_doc_duoc():
    assert decide_write_result(None, STATUS_APPROVED, is_pm_admin=True) is FORBIDDEN

def test_audit_ui_chi_pm_admin():
    assert decide_audit_read(is_pm_admin=True) is ALLOW
    assert decide_audit_read() is FORBIDDEN

# --- Sửa/approve trên kết quả (AC-08-4) ---
def test_editor_sua_va_approve_draft_duoc():
    assert decide_write_result(ROLE_EDITOR, STATUS_DRAFT) is ALLOW

def test_viewer_sua_draft_nhan_404_vi_khong_duoc_thay_no():
    assert decide_write_result(ROLE_VIEWER, STATUS_DRAFT) is NOT_FOUND

def test_viewer_sua_approved_nhan_403_vi_thay_nhung_khong_co_quyen():
    assert decide_write_result(ROLE_VIEWER, STATUS_APPROVED) is FORBIDDEN

# --- Q2: upload ---
def test_upload_chi_owner_editor():
    assert can_upload_contract(ROLE_OWNER) and can_upload_contract(ROLE_EDITOR)
    assert not can_upload_contract(ROLE_VIEWER) and not can_upload_contract(None)
