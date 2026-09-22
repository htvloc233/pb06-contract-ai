-- ============================================================================
-- 001_init_schema.sql — W1-04: 8 bảng lõi PB-06 (ARCH v1.5 §3)
-- Leash A+: file này CHỜ PM DUYỆT trước khi apply. Target: PostgreSQL >= 12
-- (design rule 5, DECISION-D8 v1.1 — chỉ tính năng cổ điển).
-- Apply:  psql -d pb06 -f migrations/001_init_schema.sql
-- ============================================================================

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- gen_random_uuid() trên PG 12

-- ── 1. analysis_jobs ── job được phép failed; result thì không (ARCH v1.4) ──
CREATE TABLE analysis_jobs (
    job_id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id      uuid        NOT NULL,
    status           varchar(20) NOT NULL
                     CHECK (status IN ('queued','processing','completed','failed')),
    pdf_type         varchar(20) CHECK (pdf_type IN ('text_layer','scan')),
    error_code       varchar(50),
    error_detail_ref varchar(100),  -- Confidential (DB-20): ID mờ, KHÔNG trả ra client
    created_by       uuid        NOT NULL,
    created_at       timestamptz NOT NULL DEFAULT now(),
    started_at       timestamptz,
    completed_at     timestamptz
);
COMMENT ON COLUMN analysis_jobs.error_detail_ref IS
  'Confidential — nhan con tro theo cai no mo duoc (ARCH v1.5, DB-20)';

-- ── 2. analysis_results ── 1 job : 0..1 result; khong co status failed ──────
CREATE TABLE analysis_results (
    result_id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id             uuid        NOT NULL UNIQUE REFERENCES analysis_jobs(job_id),
    contract_id        uuid        NOT NULL,
    version_no         integer     NOT NULL CHECK (version_no >= 1),
    status             varchar(20) NOT NULL CHECK (status IN ('draft_ai','approved')),
    summary_text       text,           -- Restricted; NULL khi insufficient_grounding
    summary_status     varchar(30) NOT NULL
                       CHECK (summary_status IN ('grounded','insufficient_grounding')),
    summary_confidence varchar(10) CHECK (summary_confidence IN ('high','medium','low')),
    user_summary_text  text,           -- Restricted; nguoi sua khong can source (4.8b)
    summary_edited_by  uuid,
    summary_edited_at  timestamptz,
    created_by         uuid        NOT NULL,
    created_at         timestamptz NOT NULL DEFAULT now(),
    approved_by        uuid,
    approved_at        timestamptz,
    UNIQUE (contract_id, version_no)   -- D7: version tuyen tinh theo hop dong
);

-- ── 3. analysis_result_fields ── dung 5 rows/result; grounding thuan ────────
CREATE TABLE analysis_result_fields (
    field_id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id        uuid        NOT NULL REFERENCES analysis_results(result_id),
    field_key        varchar(30) NOT NULL CHECK (field_key IN
                     ('parties','effective_date','expiry_date',
                      'contract_value','penalty_clause')),
    status           varchar(20) NOT NULL
                     CHECK (status IN ('grounded','not_found','uncertain')),
    confidence_label varchar(10) CHECK (confidence_label IN ('high','medium','low')),
    ai_value         text,   -- Restricted
    user_value       text,   -- Restricted; ghi de cap truong, khong can source
    display_value    text,   -- Restricted; render tong hop tu items
    is_edited        boolean     NOT NULL DEFAULT false,
    edited_by        uuid,
    edited_at        timestamptz,
    UNIQUE (result_id, field_key)
);

-- ── 4. analysis_field_items ── da gia tri ①/da doan ⑤ (AC-15-1a) ────────────
CREATE TABLE analysis_field_items (
    item_id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    field_id   uuid        NOT NULL REFERENCES analysis_result_fields(field_id),
    item_value text        NOT NULL,  -- Restricted
    ord        integer     NOT NULL CHECK (ord >= 1),
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (field_id, ord)
);

-- ── 5. analysis_field_sources ── span verbatim per ITEM (D6-a) ──────────────
CREATE TABLE analysis_field_sources (
    source_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id        uuid        NOT NULL REFERENCES analysis_field_items(item_id),
    page_number    integer     NOT NULL CHECK (page_number >= 1),
    char_start     integer,
    char_end       integer,
    source_excerpt text        NOT NULL,  -- Restricted
    created_at     timestamptz NOT NULL DEFAULT now(),
    CHECK (char_start IS NULL OR char_end IS NULL OR char_end >= char_start)
);

-- ── 6. analysis_summary_sources ── con tro nguon theo CAU (D6-b) ────────────
CREATE TABLE analysis_summary_sources (
    source_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id      uuid        NOT NULL REFERENCES analysis_results(result_id),
    sentence_index integer     NOT NULL CHECK (sentence_index >= 0),
    sentence_hash  varchar(64) NOT NULL,  -- Confidential: phat hien tom tat lech nguon
    page_number    integer     NOT NULL CHECK (page_number >= 1),
    char_start     integer,
    char_end       integer,
    source_excerpt text        NOT NULL,  -- Restricted
    created_at     timestamptz NOT NULL DEFAULT now()
);

-- ── 7. audit_logs ── APPEND-ONLY bang trigger (DoD-5) ───────────────────────
CREATE TABLE audit_logs (
    log_id       bigserial PRIMARY KEY,
    occurred_at  timestamptz NOT NULL DEFAULT now(),
    actor_id     uuid,
    actor_type   varchar(10) NOT NULL CHECK (actor_type IN ('user','system')),
    action       varchar(50) NOT NULL,
    contract_id  uuid,
    result_id    uuid,
    job_id       uuid,
    field_key    varchar(30),
    before_value varchar(500),  -- truncate 500 (NFR-S6) — enforce o audit writer
    after_value  varchar(500),
    request_id   varchar(64)
);

CREATE OR REPLACE FUNCTION audit_logs_append_only() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'audit_logs la append-only (DoD-5): % bi cam', TG_OP;
END $$;

CREATE TRIGGER trg_audit_no_update_delete
    BEFORE UPDATE OR DELETE ON audit_logs
    FOR EACH ROW EXECUTE FUNCTION audit_logs_append_only();

CREATE TRIGGER trg_audit_no_truncate
    BEFORE TRUNCATE ON audit_logs
    FOR EACH STATEMENT EXECUTE FUNCTION audit_logs_append_only();

-- ── 8. ai_model_runs ── metadata, KHONG luu prompt text (D4) ────────────────
CREATE TABLE ai_model_runs (
    run_id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id         uuid        NOT NULL REFERENCES analysis_jobs(job_id),
    provider       varchar(50) NOT NULL,
    model_name     varchar(100) NOT NULL,
    prompt_version varchar(30),
    latency_ms     integer     CHECK (latency_ms >= 0),
    created_at     timestamptz NOT NULL DEFAULT now()
);

-- ── Indexes ─────────────────────────────────────────────────────────────────
CREATE INDEX idx_jobs_contract    ON analysis_jobs (contract_id, status);
CREATE INDEX idx_results_contract ON analysis_results (contract_id);
CREATE INDEX idx_fields_result    ON analysis_result_fields (result_id);
CREATE INDEX idx_items_field      ON analysis_field_items (field_id);
CREATE INDEX idx_fsrc_item        ON analysis_field_sources (item_id);
CREATE INDEX idx_ssrc_result      ON analysis_summary_sources (result_id);
CREATE INDEX idx_audit_contract   ON audit_logs (contract_id, occurred_at);

COMMIT;
