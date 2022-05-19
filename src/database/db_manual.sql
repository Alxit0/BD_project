DROP TABLE comprador CASCADE;
DROP TABLE admnistrador CASCADE;
DROP TABLE vendedor CASCADE;
DROP TABLE utilizador CASCADE;
DROP TABLE equipamentos CASCADE;
DROP TABLE equipamentos_versions CASCADE;
DROP TABLE computadores CASCADE;
DROP TABLE televisoes CASCADE;
DROP TABLE smartphones CASCADE;
DROP TABLE orders CASCADE;
DROP TABLE ratings CASCADE;
DROP TABLE questions CASCADE;

CREATE TABLE utilizador (
	id			SERIAL UNIQUE,
	email		VARCHAR(50) NOT NULL,
	username	VARCHAR(25) NOT NULL,
	privileges	INTEGER NOT NULL,
	password	VARCHAR(25) NOT NULL,
	PRIMARY KEY(username)
);

CREATE TABLE admnistrador (
	utilizador_id	BIGINT NOT NULL,
	PRIMARY KEY(utilizador_id)
);

CREATE TABLE vendedor (
	nif				BIGINT NOT NULL,
	morada			VARCHAR(100) NOT NULL,
	utilizador_id	BIGINT,
	PRIMARY KEY(utilizador_id)
);

CREATE TABLE comprador (
	morada	 VARCHAR(100) NOT NULL,
	utilizador_id BIGINT,
	PRIMARY KEY(utilizador_id)
);

CREATE TABLE equipamentos (
	id						SERIAL,
	stock					INT NOT NULL CHECK (stock > -1),
	vendedor_utilizador_id	BIGINT NOT NULL,
	tipo					INT NOT NULL,
	cur_version				INT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE equipamentos_versions (
	id						SERIAL UNIQUE,
	preco					FLOAT(8) NOT NULL,
	descricao				VARCHAR(512) NOT NULL,
	nome					VARCHAR(512),
	equipamentos_main		INT,
	PRIMARY KEY(id)
);

CREATE TABLE computadores (
	processador	 VARCHAR(50) NOT NULL,
	placa_vidio	 VARCHAR(25),
	ram		 VARCHAR(10) NOT NULL,
	storage	 VARCHAR(10) NOT NULL,
	equipamentos_versions_id INTEGER,
	PRIMARY KEY(equipamentos_versions_id)
);

CREATE TABLE televisoes (
	tamanho	 INTEGER NOT NULL,
	resolucao	 VARCHAR(15) NOT NULL,
	refresh_rt	 INTEGER NOT NULL,
	equipamentos_versions_id INTEGER,
	PRIMARY KEY(equipamentos_versions_id)
);

CREATE TABLE smartphones (
	tamanho	 INTEGER NOT NULL,
	ram		 VARCHAR(10) NOT NULL,
	storage	 VARCHAR(10) NOT NULL,
	camera		 VARCHAR(25) NOT NULL,
	processador	 VARCHAR(25) NOT NULL,
	equipamentos_versions_id INTEGER,
	PRIMARY KEY(equipamentos_versions_id)
);


ALTER TABLE admnistrador ADD CONSTRAINT admnistrador_fk1 FOREIGN KEY (utilizador_id) REFERENCES utilizador(id);
ALTER TABLE vendedor ADD CONSTRAINT vendedor_fk1 FOREIGN KEY (utilizador_id) REFERENCES utilizador(id);
ALTER TABLE comprador ADD CONSTRAINT comprador_fk1 FOREIGN KEY (utilizador_id) REFERENCES utilizador(id);

ALTER TABLE equipamentos ADD CONSTRAINT equipamentos_fk1 FOREIGN KEY (vendedor_utilizador_id) REFERENCES vendedor(utilizador_id);
ALTER TABLE equipamentos ADD CONSTRAINT equipamentos_fk2 FOREIGN KEY (cur_version) REFERENCES equipamentos_versions(id);
ALTER TABLE equipamentos_versions ADD CONSTRAINT equipamentos_versions_fk1 FOREIGN KEY (equipamentos_main) REFERENCES equipamentos(id); 

ALTER TABLE computadores ADD CONSTRAINT computadores_fk1 FOREIGN KEY (equipamentos_versions_id) REFERENCES equipamentos_versions(id);
ALTER TABLE televisoes ADD CONSTRAINT televisoes_fk1 FOREIGN KEY (equipamentos_versions_id) REFERENCES equipamentos_versions(id);
ALTER TABLE smartphones ADD CONSTRAINT smartphones_fk1 FOREIGN KEY (equipamentos_versions_id) REFERENCES equipamentos_versions(id);


CREATE TABLE orders (
	id			SERIAL UNIQUE,
	total		FLOAT(8),
	num_orders	INT
);


CREATE TABLE ratings (
	id				SERIAL UNIQUE,
	equipamento_id	INT NOT NULL,
	comprador_id	INT NOT NULL,
	valor			INT NOT NULL,
	comment			VARCHAR(150),
	PRIMARY KEY(equipamento_id, comprador_id)
);

ALTER TABLE ratings ADD CONSTRAINT ratings_fk1 FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id);
ALTER TABLE ratings ADD CONSTRAINT ratings_fk2 FOREIGN KEY (comprador_id) REFERENCES comprador(utilizador_id);

CREATE TABLE questions (
	id				SERIAL UNIQUE,
	equipamento_id	INT NOT NULL,
	utilizador_id	INT NOT NULL,
	question		VARCHAR(150),
	parent_question	INT
);

ALTER TABLE questions ADD CONSTRAINT questions_fk1 FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id);
ALTER TABLE questions ADD CONSTRAINT questions_fk2 FOREIGN KEY (utilizador_id) REFERENCES utilizador(id);
ALTER TABLE questions ADD CONSTRAINT questions_fk3 FOREIGN KEY (parent_question) REFERENCES questions(id);

\i data.sql