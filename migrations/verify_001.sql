-- verify_001.sql — chạy SAU khi apply 001. Mỗi khối tự báo PASS/FAIL.
-- Cách chạy: psql -d pb06 -f migrations/verify_001.sql   (dán toàn bộ output)

-- [1] Đủ 8 bảng
DO $$
DECLARE n int;
BEGIN
  SELECT count(*) INTO n FROM information_schema.tables
   WHERE table_schema='public' AND table_name IN
   ('analysis_jobs','analysis_results','analysis_result_fields',
    'analysis_field_items','analysis_field_sources',
    'analysis_summary_sources','audit_logs','ai_model_runs');
  IF n = 8 THEN RAISE NOTICE 'PASS [1] du 8 bang';
  ELSE RAISE EXCEPTION 'FAIL [1] chi thay % bang', n; END IF;
END $$;

-- [2] DoD-5: audit_logs chặn UPDATE
DO $$
BEGIN
  INSERT INTO audit_logs(actor_type, action) VALUES ('system','verify_probe');
  BEGIN
    UPDATE audit_logs SET action='hacked' WHERE action='verify_probe';
    RAISE EXCEPTION 'FAIL [2] UPDATE audit_logs KHONG bi chan';
  EXCEPTION WHEN raise_exception THEN
    IF SQLERRM LIKE '%append-only%' THEN RAISE NOTICE 'PASS [2] UPDATE audit bi chan';
    ELSE RAISE; END IF;
  END;
END $$;

-- [3] DoD-5: audit_logs chặn DELETE
DO $$
BEGIN
  BEGIN
    DELETE FROM audit_logs WHERE action='verify_probe';
    RAISE EXCEPTION 'FAIL [3] DELETE audit_logs KHONG bi chan';
  EXCEPTION WHEN raise_exception THEN
    IF SQLERRM LIKE '%append-only%' THEN RAISE NOTICE 'PASS [3] DELETE audit bi chan';
    ELSE RAISE; END IF;
  END;
END $$;

-- [4] Quyết định ARCH v1.4: results KHÔNG có status failed
DO $$
DECLARE jid uuid;
BEGIN
  INSERT INTO analysis_jobs(contract_id, status, created_by)
  VALUES (gen_random_uuid(),'completed',gen_random_uuid()) RETURNING job_id INTO jid;
  BEGIN
    INSERT INTO analysis_results(job_id,contract_id,version_no,status,summary_status,created_by)
    VALUES (jid, gen_random_uuid(), 1, 'failed', 'grounded', gen_random_uuid());
    RAISE EXCEPTION 'FAIL [4] status=failed lot qua CHECK';
  EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'PASS [4] results tu choi status=failed';
  END;
END $$;

-- [5] D7: UNIQUE (contract_id, version_no)
DO $$
DECLARE cid uuid := gen_random_uuid(); j1 uuid; j2 uuid;
BEGIN
  INSERT INTO analysis_jobs(contract_id,status,created_by)
  VALUES (cid,'completed',gen_random_uuid()) RETURNING job_id INTO j1;
  INSERT INTO analysis_jobs(contract_id,status,created_by)
  VALUES (cid,'completed',gen_random_uuid()) RETURNING job_id INTO j2;
  INSERT INTO analysis_results(job_id,contract_id,version_no,status,summary_status,created_by)
  VALUES (j1,cid,1,'draft_ai','grounded',gen_random_uuid());
  BEGIN
    INSERT INTO analysis_results(job_id,contract_id,version_no,status,summary_status,created_by)
    VALUES (j2,cid,1,'draft_ai','grounded',gen_random_uuid());
    RAISE EXCEPTION 'FAIL [5] trung (contract_id,version_no) lot qua UNIQUE';
  EXCEPTION WHEN unique_violation THEN
    RAISE NOTICE 'PASS [5] UNIQUE version theo hop dong hoat dong';
  END;
END $$;

-- [6] Dọn dữ liệu probe (results/jobs xoá được — chỉ audit_logs là append-only)
DELETE FROM analysis_results WHERE version_no = 1 AND status='draft_ai'
  AND contract_id NOT IN (SELECT DISTINCT contract_id FROM analysis_result_fields JOIN analysis_results USING(result_id));
DELETE FROM analysis_jobs WHERE status='completed' AND job_id NOT IN (SELECT job_id FROM analysis_results);
DO $$ BEGIN RAISE NOTICE 'PASS [6] don probe xong — dong audit verify_probe GIU LAI lam bang chung append-only'; END $$;
