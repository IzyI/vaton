INSERT INTO public.vaton_user_role (id, role)
VALUES (333, 'admin');
INSERT INTO public.vaton_user_role (id, role)
VALUES (222, 'manager');
INSERT INTO public.vaton_user_role (id, role)
VALUES (111, 'user');
INSERT INTO public.vaton_user_role (id, role)
VALUES (444, 'bot');

-- SALT = "9j086fdsf__sdff7g9g8^^$Dyc67"
-- hash password: $2b$12$6vFY5LwMAOXxWjotGFRR3O.e72Qb9fCMvB0JVri7uGTiTNxawmYe2  - admin
INSERT INTO public.vaton_user (email, password, registration_time)
VALUES ('admin@vaton.com', '$2b$12$6vFY5LwMAOXxWjotGFRR3O.e72Qb9fCMvB0JVri7uGTiTNxawmYe2', CURRENT_TIMESTAMP);

INSERT INTO public.vaton_user_info (id, bio, username, id_user)
VALUES ('07d26b56-31ac-46b2-9480-946bb043f60d', 'admin',
        (SELECT id from public.vaton_user where email = 'admin@vaton.com'));


INSERT INTO public.association_user_role (vaton_user_id, vaton_user_role_id)
VALUES ((SELECT id from public.vaton_user where email = 'admin@vaton.com'),
        (SELECT id from public.vaton_user_role where role = 'admin'));



