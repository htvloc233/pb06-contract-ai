# Staging phương án B — native trên macOS 10.15 (DECISION-D8 v1.1)

Thay `docker compose up` bằng: **Python 3.12 (venv) + Postgres.app + ./staging-up.sh**.
File compose vẫn nằm trong repo — đó là định nghĩa staging chuẩn cho CI và máy đủ điều kiện.

## 1. Cài Python 3.12 (một lần)
python.org → Downloads → macOS → bản **Python 3.12.x — macOS 64-bit universal2 installer**
(installer chính chủ hỗ trợ các đời macOS cũ; chạy tốt trên 10.15). Cài mặc định, rồi kiểm:

    python3.12 --version

## 2. Cài Postgres.app (một lần)
Trang Releases: `github.com/PostgresApp/PostgresApp/releases` — kéo xuống các bản 2020–2022,
**đọc dòng "requires macOS …" trong release notes** và chọn bản MỚI NHẤT còn nhận 10.15.
Bản chắc chắn chạy (fallback): release **May 2020**, file `Postgres-2.3.5-12.dmg` — ghi rõ
*requires macOS 10.12 or later*, kèm PostgreSQL 12.3.

Cài: mở .dmg → kéo vào Applications → mở app → bấm **Initialize** → thấy server *Running*.
Tạo database của dự án (một lần):

    /Applications/Postgres.app/Contents/Versions/latest/bin/createdb pb06

## 3. Chạy staging
    cd ~/pb06-contract-ai
    cp .env.example .env        # sửa mật khẩu trong .env; file này KHÔNG commit
    ./staging-up.sh             # tab Terminal thứ 1 — giữ chạy

## 4. Bằng chứng lật D8 (tab Terminal thứ 2 — dán cả hai output)
    curl http://localhost:8000/health
    /Applications/Postgres.app/Contents/Versions/latest/bin/psql -d pb06 -c "select version();"

Kỳ vọng: JSON `"status":"ok"` và một dòng `PostgreSQL 12.x/13.x ...`.

## Ghi chú lệch phiên bản (đã ghi nhận trong DECISION-D8 v1.1)
Staging-B chạy PG 12/13; compose/CI định nghĩa PG 16 → migration Wave 1 chỉ dùng
tính năng cổ điển (bảng, CHECK, UNIQUE, trigger — đều có từ trước PG 12), skew tự hết
khi chuyển máy/OS mới.
