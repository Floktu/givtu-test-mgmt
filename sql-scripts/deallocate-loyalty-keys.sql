SELECT DISTINCT u.*
FROM user u
LEFT JOIN fortune_keys fk ON fk.user_id = u.id
LEFT JOIN fortune_draws fd ON fk.fortune_draw_id = fd.id
WHERE fk.status = 1
  AND fk.category = 3
  AND fk.active_date < fd.draw_date
  AND fd.draw_date < '2025-05-18 18:00:01'
  AND NOT EXISTS (
      SELECT 1
      FROM subscription s
      WHERE s.user_id = u.id AND s.status >= 0
  )
LIMIT 10;