SELECT DISTINCT ra.id, ra.valor, ra.comment, ra.comprador_id
FROM ratings as ra, equipamentos_versions as eqver
WHERE eqver.equipamentos_main = ra.equipamento_id AND eqver.equipamentos_main = 1;

SELECT DISTINCT eqver.equipamentos_main, eqver.preco
FROM equipamentos_versions as eqver
WHERE eqver.equipamentos_main = 1;

SELECT descricao FROM equipamentos_versions
ORDER BY descricao ASC
LIMIT 1;

SELECT (SELECT ARRAY_AGG(preco) FROM equipamentos_versions WHERE equipamentos_main = prod.id),
(SELECT ARRAY_AGG(JOIN(valor, comment)) FROM ratings WHERE equipamento_id = prod.id) FROM equipamentos as prod WHERE
prod.id = 1;

ARRAY_AGG