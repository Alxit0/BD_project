-- SELECT DISTINCT ra.id, ra.valor, ra.comment, ra.comprador_id
-- FROM ratings as ra, equipamentos_versions as eqver
-- WHERE eqver.equipamentos_main = ra.equipamento_id AND eqver.equipamentos_main = 1;

-- SELECT DISTINCT eqver.equipamentos_main, eqver.preco
-- FROM equipamentos_versions as eqver
-- WHERE eqver.equipamentos_main = 1;

-- SELECT descricao FROM equipamentos_versions ORDER BY descricao ASC LIMIT 1;

-- create type int_str as (f1 int, f2 text);
-- SELECT (SELECT ARRAY_AGG(preco) FROM equipamentos_versions WHERE equipamentos_main = prod.id),
-- (SELECT ARRAY_AGG((valor, comment)::int_str) FROM ratings WHERE equipamento_id = prod.id) FROM equipamentos as prod WHERE
-- prod.id = 1;

-- SELECT _date, SUM(total), SUM(num_orders) FROM orders GROUP BY _date;

CREATE OR REPLACE FUNCTION sell_allert_helper() RETURNS TRIGGER AS
$BODY$
BEGIN
    INSERT INTO notificacoes(utilizador_id, title, descricao) VALUES (NEW.vendedor_utilizador_id, 'Valor vendido', OLD.stock - NEW.stock);
    RETURN NEW;
END;
$BODY$
language plpgsql;

CREATE or replace TRIGGER sell_allert
     AFTER UPDATE ON equipamentos
     FOR EACH ROW
     EXECUTE PROCEDURE sell_allert_helper();