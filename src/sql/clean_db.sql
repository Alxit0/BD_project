DROP TABLE equipamentos CASCADE;
DROP TABLE computadores CASCADE;
DROP TABLE televisoes CASCADE;
DROP TABLE smartphones CASCADE;
DROP TABLE utilizador CASCADE;
DROP TABLE admnistrador CASCADE;
DROP TABLE comprador CASCADE;
DROP TABLE vendedor CASCADE;
DROP TABLE rating CASCADE;
DROP TABLE perguntas CASCADE;
DROP TABLE notificacoes CASCADE;
DROP TABLE campanhas CASCADE;
DROP TABLE cupao CASCADE;
DROP TABLE compra CASCADE;
DROP TABLE mini_compra CASCADE;


CREATE TABLE equipamentos (
	id			 SERIAL,
	preco			 FLOAT(8) NOT NULL,
	descricao		 VARCHAR(512) NOT NULL,
	stock			 INTEGER NOT NULL,
	nome			 VARCHAR(512),
	vendedor_utilizador_id BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE computadores (
	processador	 VARCHAR(50) NOT NULL,
	placa_vidio	 VARCHAR(25),
	ram		 VARCHAR(10) NOT NULL,
	storage	 VARCHAR(10) NOT NULL,
	equipamentos_id INTEGER,
	PRIMARY KEY(equipamentos_id)
);

CREATE TABLE televisoes (
	tamanho	 INTEGER NOT NULL,
	resolucao	 VARCHAR(15) NOT NULL,
	refresh_rt	 INTEGER NOT NULL,
	equipamentos_id INTEGER,
	PRIMARY KEY(equipamentos_id)
);

CREATE TABLE smartphones (
	tamanho	 INTEGER NOT NULL,
	ram		 VARCHAR(10) NOT NULL,
	storage	 VARCHAR(10) NOT NULL,
	camera		 VARCHAR(25) NOT NULL,
	processador	 VARCHAR(25) NOT NULL,
	equipamentos_id INTEGER,
	PRIMARY KEY(equipamentos_id)
);

CREATE TABLE utilizador (
	id	 SERIAL,
	email	 VARCHAR(50) NOT NULL,
	username VARCHAR(25) NOT NULL,
	password VARCHAR(25) NOT NULL,
	PRIMARY KEY(username)
);

CREATE TABLE admnistrador (
	utilizador_id BIGINT,
	PRIMARY KEY(utilizador_id)
);

CREATE TABLE vendedor (
	nif		 BIGINT NOT NULL,
	morada	 VARCHAR(100) NOT NULL,
	utilizador_id BIGINT,
	PRIMARY KEY(utilizador_id)
);

CREATE TABLE comprador (
	morada	 VARCHAR(100) NOT NULL,
	utilizador_id BIGINT,
	PRIMARY KEY(utilizador_id)
);

CREATE TABLE rating (
	classificacao		 INTEGER DEFAULT 0,
	comentario		 VARCHAR(512),
	comprador_utilizador_id BIGINT NOT NULL,
	equipamentos_id	 INTEGER NOT NULL
);

CREATE TABLE perguntas (
	pergunta		 VARCHAR(512) NOT NULL,
	resposta		 VARCHAR(512),
	equipamentos_id	 INTEGER NOT NULL,
	comprador_utilizador_id BIGINT NOT NULL
);

CREATE TABLE notificacoes (
	descricao		 VARCHAR(512),
	data			 DATE,
	comprador_utilizador_id BIGINT NOT NULL,
	vendedor_utilizador_id	 BIGINT NOT NULL,
	PRIMARY KEY(descricao)
);

CREATE TABLE campanhas (
	id			 BIGINT,
	inicio			 DATE,
	fim			 DATE,
	n_cupoes			 INTEGER,
	deconto_perc		 INTEGER,
	validade_de_cupao		 BOOL,
	admnistrador_utilizador_id BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE cupao (
	data_aquizicao		 DATE NOT NULL,
	comprador_utilizador_id BIGINT NOT NULL,
	campanhas_id		 BIGINT NOT NULL
);

CREATE TABLE compra (
	id			 BIGINT,
	data			 DATE,
	comprador_utilizador_id BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE mini_compra (
	quantidade	 INTEGER,
	equipamentos_id INTEGER NOT NULL,
	compra_id	 BIGINT NOT NULL
);

ALTER TABLE equipamentos ADD CONSTRAINT equipamentos_fk1 FOREIGN KEY (vendedor_utilizador_id) REFERENCES vendedor(utilizador_id);
ALTER TABLE computadores ADD CONSTRAINT computadores_fk1 FOREIGN KEY (equipamentos_id) REFERENCES equipamentos(id);
ALTER TABLE televisoes ADD CONSTRAINT televisoes_fk1 FOREIGN KEY (equipamentos_id) REFERENCES equipamentos(id);
ALTER TABLE smartphones ADD CONSTRAINT smartphones_fk1 FOREIGN KEY (equipamentos_id) REFERENCES equipamentos(id);
ALTER TABLE admnistrador ADD CONSTRAINT admnistrador_fk1 FOREIGN KEY (utilizador_id) REFERENCES utilizador(id);
ALTER TABLE vendedor ADD CONSTRAINT vendedor_fk1 FOREIGN KEY (utilizador_id) REFERENCES utilizador(id);
ALTER TABLE comprador ADD CONSTRAINT comprador_fk1 FOREIGN KEY (utilizador_id) REFERENCES utilizador(id);
ALTER TABLE rating ADD CONSTRAINT rating_fk1 FOREIGN KEY (comprador_utilizador_id) REFERENCES comprador(utilizador_id);
ALTER TABLE rating ADD CONSTRAINT rating_fk2 FOREIGN KEY (equipamentos_id) REFERENCES equipamentos(id);
ALTER TABLE perguntas ADD CONSTRAINT perguntas_fk1 FOREIGN KEY (equipamentos_id) REFERENCES equipamentos(id);
ALTER TABLE perguntas ADD CONSTRAINT perguntas_fk2 FOREIGN KEY (comprador_utilizador_id) REFERENCES comprador(utilizador_id);
ALTER TABLE notificacoes ADD CONSTRAINT notificacoes_fk1 FOREIGN KEY (comprador_utilizador_id) REFERENCES comprador(utilizador_id);
ALTER TABLE notificacoes ADD CONSTRAINT notificacoes_fk2 FOREIGN KEY (vendedor_utilizador_id) REFERENCES vendedor(utilizador_id);
ALTER TABLE campanhas ADD CONSTRAINT campanhas_fk1 FOREIGN KEY (admnistrador_utilizador_id) REFERENCES admnistrador(utilizador_id);
ALTER TABLE cupao ADD CONSTRAINT cupao_fk1 FOREIGN KEY (comprador_utilizador_id) REFERENCES comprador(utilizador_id);
ALTER TABLE cupao ADD CONSTRAINT cupao_fk2 FOREIGN KEY (campanhas_id) REFERENCES campanhas(id);
ALTER TABLE compra ADD CONSTRAINT compra_fk1 FOREIGN KEY (comprador_utilizador_id) REFERENCES comprador(utilizador_id);
ALTER TABLE mini_compra ADD CONSTRAINT mini_compra_fk1 FOREIGN KEY (equipamentos_id) REFERENCES equipamentos(id);
ALTER TABLE mini_compra ADD CONSTRAINT mini_compra_fk2 FOREIGN KEY (compra_id) REFERENCES compra(id);