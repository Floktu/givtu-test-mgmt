TRUNCATE TABLE new_subscription;
TRUNCATE TABLE new_fortune_draws;
TRUNCATE TABLE new_draw_schedule;
TRUNCATE TABLE new_draws;
TRUNCATE TABLE new_fortune_keys;
TRUNCATE TABLE new_fortune_key_audit;


CREATE TABLE new_subscription AS SELECT * FROM subscription;
CREATE TABLE new_fortune_draws AS SELECT * FROM fortune_draws;
CREATE TABLE new_draw_schedule AS SELECT * FROM draw_schedule;
CREATE TABLE new_draws AS SELECT * FROM draws;
--CREATE TABLE new_fortune_keys AS (SELECT * FROM fortune_keys where status = 1);
--CREATE TABLE new_fortune_key_audit AS (SELECT * FROM fortune_key_audit);

-- Fortune draws
SELECT * FROM givtuprod.new_fortune_draws;

UPDATE new_fortune_draws
SET draw_date = DATE_ADD(draw_date, INTERVAL 56 DAY) where id >= 12;

-- Draw Schedule
SELECT * FROM givtuprod.new_draw_schedule;

UPDATE new_draw_schedule
SET start_date = DATE_ADD(start_date, INTERVAL 56 DAY),
	end_date = DATE_ADD(end_date, INTERVAL 56 DAY),
    clone_end_date = DATE_ADD(clone_end_date, INTERVAL 56 DAY),
    updated = CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney')
where id >= 9;

-- Draws
SELECT * FROM givtuprod.new_draws;

UPDATE new_draws
SET launched_date = DATE_ADD(launched_date, INTERVAL 56 DAY),
	end_date = DATE_ADD(end_date, INTERVAL 56 DAY),
    clone_end_date = DATE_ADD(clone_end_date, INTERVAL 56 DAY)
where draw_schedule_id >= 9;

-- Subscriptions
SELECT s.*, d.end_date FROM givtuprod.new_subscription s
left join new_draws d on d.id = s.last_order_draw
 where status = 1;

update new_subscription
SET next_due_date = DATE_ADD(next_due_date, INTERVAL 56 DAY),
	max_try_sub_end_date = DATE_ADD(max_try_sub_end_date, INTERVAL 56 DAY)
where status = 1;

-- Fortune Keys
SELECT * FROM givtuprod.new_fortune_keys where fortune_draw_id >= 12;

SELECT nfk.*, fd.draw_date FROM new_fortune_keys nfk left join new_fortune_draws fd on fd.id = nfk.fortune_draw_id where fortune_draw_id >= 12;

UPDATE new_fortune_keys
SET active_date = DATE_ADD(active_date, INTERVAL 56 DAY) where fortune_draw_id >= 12;

-- Fortune Key Audit
SELECT * FROM givtuprod.new_fortune_key_audit where fortune_draw_id >= 12;

SELECT nfk.*, fd.draw_date FROM new_fortune_key_audit nfk left join new_fortune_draws fd on fd.id = nfk.fortune_draw_id where fortune_draw_id >= 12;

UPDATE new_fortune_key_audit
SET active_date = DATE_ADD(active_date, INTERVAL 56 DAY) where fortune_draw_id >= 12;

-- DANGEROUS THIS IS THE SCRIPT TO SWAP THE TABLES
RENAME TABLE
    fortune_draws TO fortune_draws_backup_20250531,
    new_fortune_draws TO fortune_draws,
    draw_schedule TO draw_schedule_backup_20250531,
    new_draw_schedule TO draw_schedule,
    draws TO draws_20250531,
    new_draws TO draws,
    subscription TO subscription_backup_20250531,
    new_subscription to subscription,
    fortune_key_audit to fortune_key_audit_backup_20250531,
    new_fortune_key_audit to fortune_key_audit;

-- The Fortune Keys Table is too big to backup and swap
-- We have backed up the fortune_key_audit table

-- For fortune_keys table we will run:
-- UPDATE new_fortune_keys
-- SET active_date = DATE_ADD(active_date, INTERVAL 56 DAY) where fortune_draw_id >= 12;


