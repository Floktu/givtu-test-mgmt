SELECT
                nc.id AS news_cms_id,
                 nc.value AS video_link ,
                 nc.overlay_label AS overlay_label
                FROM cms_ref cr
                    LEFT JOIN news_cms nc
                            ON nc.id = cr.cms_id
                                AND nc.category = 2
                    LEFT JOIN available_states avs
                            ON avs.id = cr.tag_value
                                AND cr.tag_type = "STATES"
                    LEFT JOIN aus_post_codes apc
                            ON apc.pcode = cr.tag_value
                                AND cr.tag_type = "POSTCODE"
                    LEFT JOIN user u
                            ON u.state = avs.state_code
                                OR u.post_code = apc.pcode
                                    AND u.id = 7
                    LEFT JOIN ticket_owners t
                            ON t.draw_id = cr.tag_value
                                AND cr.tag_type = "GAME_ID"
                                AND t.profile_id = 7
                    LEFT JOIN order_ticket ot
                            ON ot.id = t.order_ticket_id
                    LEFT JOIN user_interests ui
                            ON ui.category_id = cr.tag_value
                                AND ( cr.tag_type = "INTEREST_PRIZE" OR cr.tag_type = "INTEREST_CHARITY"  )
                                AND ui.user_id = 7
                    LEFT JOIN dreamlist d
                            ON d.cat_id = cr.tag_value
                                AND ( cr.tag_type = "SPECIFIC_CHARITY" OR cr.tag_type = "SPECIFIC_PRIZE"  )
                                -- AND d.user_id = 7
                    LEFT JOIN categories c
                            ON (
                                    c.id = ui.category_id
                                    OR c.id = d.cat_id
                                    OR c.id = ot.nfps_cat_id
                                )
                WHERE  nc.active = 1
                    AND ( nc.publish_date > Convert_tz(Now(), "SYSTEM", "Australia/Sydney") - INTERVAL 8 week )
                    AND ( u.state IS NOT NULL
                            OR u.post_code IS NOT NULL
                            OR t.profile_id IS NOT NULL
                            OR ui.user_id IS NOT NULL
                            OR d.user_id IS NOT NULL
                            OR u.post_code IS NOT NULL )
                            GROUP BY nc.id
                ORDER  BY nc.id DESC;
