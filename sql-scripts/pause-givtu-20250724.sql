-- Script to extend games out for two months
-- We need to back up these tables then update the dates
CREATE TABLE backup_fortune_draws_20250724 AS SELECT * FROM fortune_draws;
CREATE TABLE backup_draw_schedule_20250724 AS SELECT * FROM draw_schedule;
CREATE TABLE backup_draws_20250724 AS SELECT * FROM draws;
CREATE TABLE backup_subscription_20250724 AS SELECT * FROM subscription;

UPDATE fortune_draws
SET draw_date = DATE_ADD(draw_date, INTERVAL 56 DAY) where id >= 12;

UPDATE draw_schedule
SET start_date = DATE_ADD(start_date, INTERVAL 56 DAY),
	end_date = DATE_ADD(end_date, INTERVAL 56 DAY),
    clone_end_date = DATE_ADD(clone_end_date, INTERVAL 56 DAY),
    updated = CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney')
where id >= 9;

update draw_schedule set start_date = '2025-05-29 17:00:00' where id = 9;

UPDATE draws
SET launched_date = DATE_ADD(launched_date, INTERVAL 56 DAY),
	end_date = DATE_ADD(end_date, INTERVAL 56 DAY),
    clone_end_date = DATE_ADD(clone_end_date, INTERVAL 56 DAY)
where draw_schedule_id >= 9;

update draws set launched_date = '2025-05-29 17:00:00' where id = 9;

update subscription
SET next_due_date = DATE_ADD(next_due_date, INTERVAL 56 DAY),
	max_try_sub_end_date = DATE_ADD(max_try_sub_end_date, INTERVAL 56 DAY)
where status = 1;

-- We will turn off subscription renewals to prevent them from being updated




