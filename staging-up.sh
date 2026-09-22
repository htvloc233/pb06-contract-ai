#!/bin/bash
# staging-up.sh — Staging phương án B (native, DECISION-D8 v1.1)
# Chạy AI service trong venv Python; Postgres do Postgres.app đảm nhiệm (mở app trước).
set -e

PY=python3.12
if ! command -v $PY >/dev/null 2>&1; then
  echo "❌ Chưa có python3.12 — cài installer chính chủ từ python.org (xem README-STAGING-B.md, bước 1)"
  exit 1
fi

if [ ! -f .env ]; then
  echo "❌ Thiếu .env — chạy: cp .env.example .env  (rồi sửa mật khẩu; .env không bao giờ commit)"
  exit 1
fi
set -a; source .env; set +a

if [ ! -d .venv ]; then
  echo "== Tạo venv lần đầu (python3.12) =="
  $PY -m venv .venv
fi
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "== Staging B đang chạy: http://localhost:8000/health  (Ctrl+C để dừng) =="
echo "== Nhớ: Postgres.app phải đang mở (server Running) để có DB =="
echo ""
exec uvicorn src.main:app --host 127.0.0.1 --port 8000
