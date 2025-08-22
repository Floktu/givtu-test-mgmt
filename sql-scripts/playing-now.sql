SELECT
                ot.id as order_ticket_id,
                win_n.name as winning_charity_name,
                MAX(CASE WHEN dwc.ticket_type = 1 THEN 1 ELSE 0 END) AS has_grand_prize, /*to check the tile has grand winning ticket*/
                MAX(tw.id) as ticket_owner_id,
                MAX(tw.draw_id) as draw_id,
                MAX(d.id) as drawId,
                MAX(d.name) as name,
                MAX(d.end_date) as draw_end_date,
                MAX(p.id) as prize_id,
                MAX(p.cube_image) as prizeHeroImage,
                MAX(p.video_url) AS prizeVideo,
                MAX(p.subtitle) as prize,
                MAX(n.id) as nfps_id,
                MAX(n.name) as charity,
                MAX(n.video_url) AS nfpsVideo,
                MAX(ot.subs_order_no) as subs_order_no,
                MAX(ot.quantity) as quantity,
                MAX(s.id) as subscription_id,
                MAX(s.status) as sub_status,
                MAX(s.next_due_date) as sub_next_due_date,
                MAX(tw.verify_date) as verify_date,
                MAX(dw.reveal_date) as reveal_date,
                MAX(dw.draw_date_time) as drawDate,
                MAX(nfpC.name) as nfp_category_name,
                MAX(dw.draw_schedule_id) as draw_schedule_id,
                MAX(dw.claim_date) as claim_date,
                MAX(nfpC.win_text) as winTileSuffix,
                MAX(nfpC.lose_text) as loseTileSuffix,
                COUNT(DISTINCT(dw.id)) as win_count,
                MAX(s.max_try_sub_end_date) as max_try_sub_end_date,
                CASE
                    WHEN MAX(d.end_date) <  CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') THEN 'Past'
                    ELSE 'Future'
                END AS tile_status,
                CASE WHEN
                (SELECT COUNT(id) FROM draw_winners WHERE draw_winners.draw_id= MAX(tw.draw_id)) = 0 THEN false ELSE true END AS has_drawn,
                -- CASE
                --     WHEN MAX(dw.reveal_date) IS NOT NULL THEN
                --         CASE
                --             WHEN COUNT(DISTINCT CONCAT(dw.draw_id, '-', dw.ticket_owner_id)) > 0
                --                 AND MAX(dw.reveal_date) >= (CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') - INTERVAL 2 DAY) THEN 'display'
                --             WHEN COUNT(DISTINCT CONCAT(dw.draw_id, '-', dw.ticket_owner_id)) = 0
                --                 AND MAX(dw.reveal_date) >= (CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') - INTERVAL 1 DAY) THEN 'display'
                --             ELSE 'hide'
                --         END
                --     ELSE 'display'
                -- END AS tile_show,
                CASE
                    WHEN MAX(dw.reveal_date) IS NOT NULL THEN
                        CASE
                            WHEN COUNT(DISTINCT CONCAT(dw.draw_id, '-', dw.ticket_owner_id)) > 0
                                AND MAX(dw.reveal_date) >= (CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') - INTERVAL 2 DAY) THEN 'display'
                            WHEN COUNT(DISTINCT CONCAT(dw.draw_id, '-', dw.ticket_owner_id)) = 0
                                AND MAX(dw.reveal_date) >= (CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') - INTERVAL 1 DAY) THEN 'display'
                            ELSE 'hide'
                        END
					WHEN MAX(tw.verify_date) IS NOT NULL AND MAX(dw.reveal_date) IS NULL THEN
						CASE
                            WHEN COUNT(DISTINCT CONCAT(dw.draw_id, '-', dw.ticket_owner_id)) > 0 THEN 'display'
                            WHEN COUNT(DISTINCT CONCAT(dw.draw_id, '-', dw.ticket_owner_id)) = 0
                                AND MAX(tw.verify_date) >= (CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') - INTERVAL 1 DAY) THEN 'display'
                            ELSE 'hide'
                        END
					ELSE 'display'
                END AS tile_show,
                CASE
                WHEN MAX(s.next_due_date) <  CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') and CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') < MAX(s.max_try_sub_end_date) and MAX(s.status) = 1 THEN true
                ELSE false
                END AS is_multi_renewing
                from order_ticket ot
                left join ticket_owners tw on ot.id = tw.order_ticket_id
                left join draws d on d.id = tw.draw_id
                left join prizes p on p.id = ot.prize_id
                left join nfps n on n.id = ot.nfps_id
                left join categories nfpC on nfpC.id = ot.nfps_cat_id
                left join subscription s on s.id = ot.subscription_id
                left join draw_winners dw on dw.ticket_owner_id = tw.id
                /*to check the tile has grand winning ticket*/
                left join drawing_winner_conf dwc on dwc.id = dw.winner_conf_id
                left join nfps win_n on win_n.id = tw.grand_winner_charity
                where tw.draw_id is not null
                and end_date <= (SELECT max(end_date) FROM draws where active = 1 and CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') > launched_date AND CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') < end_date order by end_date asc limit 2)
                AND tw.profile_id = 7  AND  tw.type != 3 GROUP BY ot.id
				HAVING NOT (
					MAX(s.status) = 0 AND
					CASE
						WHEN MAX(s.next_due_date) < CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney')
 							 AND CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') < MAX(s.max_try_sub_end_date)
						THEN true
						ELSE false
					END
				)

			  ORDER BY
                CASE
                    WHEN MAX(tw.verify_date) IS NOT NULL AND MAX(dw.reveal_date) IS NULL AND count(DISTINCT(dw.id)) != 0 THEN 1
                    WHEN MAX(d.end_date) < CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') AND MAX(tw.verify_date) IS NULL THEN 2
                    WHEN MAX(d.end_date) >  CONVERT_TZ(NOW(), 'SYSTEM', 'Australia/Sydney') THEN 3
                    WHEN MAX(dw.reveal_date) IS NOT NULL THEN 4
                    ELSE 5
                END,
                MAX(d.end_date) ASC
                ;

