INSERT INTO utilizador (email, username, privileges, password) VALUES ('alex@ola.com', 'Alex', 3, 'ola123');
INSERT INTO admnistrador (utilizador_id) VALUES (1);

INSERT INTO utilizador (email, username, privileges, password) VALUES ('marga@ola.com', 'Marga', 2, 'ola123');
INSERT INTO vendedor (utilizador_id, nif, morada) VALUES (2, '123123', 'Carmo');