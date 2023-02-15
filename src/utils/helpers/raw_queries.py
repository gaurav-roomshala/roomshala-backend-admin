QUERY_FOR_INSERTING_ADMIN = """INSERT INTO admin VALUES (nextval('admin_id_seq'), :first_name,:last_name,:gender,
                            :email,:password,:phone_number,:is_active,:role,now() at time zone 'UTC',:created_by,now() at time zone 'UTC',:updated_by) RETURNING id; """
