QUERY_FOR_INSERTING_ADMIN = """INSERT INTO admin VALUES (nextval('admin_id_seq'), :first_name,:last_name,:gender,
                            :email,:password,:phone_number,:is_active,:role,now() at time zone 'UTC',:created_by,now() at time zone 'UTC',:updated_by) RETURNING id; """



QUERY_FOR_SAVING_FACILITY = """INSERT INTO facilities VALUES (nextval('facilities_id_seq'),:name,:is_active,now() at time zone 'UTC') """


QUERY_FOR_SAVING_AMENITIES = """INSERT INTO amenties VALUES (nextval('amenties_id_seq'),:name,:is_active,now() at time zone 'UTC') """
