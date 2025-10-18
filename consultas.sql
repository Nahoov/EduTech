-- Arquivos com todas as consultas SQL

-- 1ra consulta Listar todos os cursos com nome da categoria e do instrutor

SELECT
    c.titulo_curso,
    ct.nome_categoria,
    it.nome_instrutor
FROM cursos c

JOIN categoria_cursos ct ON c.categoriaid = ct.categoriaid
JOIN instrutores it ON c.instrutorid = it.instrutorid;


--2da consulta Listar todos os alunos matriculados em um curso específico

SELECT 
    m.matriculaid,
    c.titulo_curso,
	a.nome_aluno
FROM matriculas m

JOIN cursos c ON m.cursoid = c.cursoid
JOIN alunos a ON m.alunoid = a.alunoid
WHERE titulo_curso = 'Controle de Versão com Git e GitHub';





--Exibir todas as aulas de um curso ordenadas por módulo e ordem
SELECT 
    c.titulo_curso,
    m.titulo,
    m.ordem,
    a.titulo,
    a.ordem
FROM cursos c
JOIN modulos m ON m.cursoid = c.cursoid
JOIN aulas a ON a.moduloid = m.moduloid
WHERE c.titulo_curso = 'Controle de Versão com Git e GitHub';



-- Calcular media de avaliacoes de cada curso

SELECT
    c.titulo_curso,
    ROUND(AVG(a.nota_prova), 2)AS media_avaliacao
FROM avaliacoes a
JOIN cursos c ON a.cursoid = c.cursoid
GROUP BY
    c.cursoid, c.titulo_curso;



-- Contar quantos alunos estao matriculados por curso



SELECT
    c.titulo_curso,
    COUNT(m.alunoID) AS total_alunos_matriculados
FROM matriculas m

JOIN cursos c ON m.cursoID = c.cursoID
GROUP BY
    c.cursoID, c.titulo_curso
ORDER BY
    total_alunos_matriculados DESC;


-- Calcular faturamento total por categoria

SELECT
    ct.nome_categoria,
    SUM(m.valor_pago) AS faturamento_total
FROM matriculas m

JOIN cursos c ON m.cursoID = c.cursoID
JOIN categoria_cursos ct ON c.categoriaID = ct.categoriaID
GROUP BY
    ct.nome_categoria
ORDER BY
    faturamento_total DESC;

--Identificar o curso com maior número de matriculas ativas

SELECT
    c.titulo_curso,
    COUNT(m.matriculaID) AS total_ativas
FROM matriculas m

JOIN cursos c ON m.cursoID = c.cursoID
WHERE
    m.status_matricula = 'ativa'
GROUP BY
    c.cursoID, c.titulo_curso
ORDER BY
    total_ativas DESC;


-- Listar alunos, cursos matriculados e porcentagem de conclusão

SELECT 
    a.alunoID,
    a.nome_aluno || ' ' || a.sobrenome_aluno AS nome_completo,
    c.cursoID,
    c.titulo_curso,
    COUNT(pa.aulaID) FILTER (WHERE pa.concluida = TRUE) * 100.0 / COUNT(au.aulaID) AS porcentagem_conclusao
FROM 
    matriculas m
JOIN 
    alunos a ON m.alunoID = a.alunoID
JOIN 
    cursos c ON m.cursoID = c.cursoID
JOIN 
    modulos mo ON c.cursoID = mo.cursoID
JOIN 
    aulas au ON mo.moduloID = au.moduloID
LEFT JOIN 
    progresso_aulas pa ON pa.aulaID = au.aulaID AND pa.matriculaID = m.matriculaID
GROUP BY 
    a.alunoID, a.nome_aluno, a.sobrenome_aluno, c.cursoID, c.titulo_curso
ORDER BY 
    nome_completo, c.titulo_curso;

  


-- Relatório completo de um curso: instrutor, número de alunos, média de avaliações, faturamento 

SELECT 
    c.cursoID,
    c.titulo_curso,
    i.nome_instrutor || ' ' || i.sobrenome_instrutor AS instrutor,
    COUNT(DISTINCT m.alunoID) AS num_alunos,
    ROUND(AVG(av.nota_prova), 2) AS media_avaliacoes,
    SUM(m.valor_pago) AS faturamento_total
FROM 
    cursos c
JOIN 
    instrutores i ON c.instrutorID = i.instrutorID
LEFT JOIN 
    matriculas m ON c.cursoID = m.cursoID
LEFT JOIN 
    avaliacoes av ON c.cursoID = av.cursoID
GROUP BY 
    c.cursoID, c.titulo_curso, instrutor
ORDER BY 
    faturamento_total DESC;




-- instrutores com quantidade de cursos, total de alunos e média geral de avaliações

SELECT
    i.instrutorID,
    i.nome_instrutor || ' ' || i.sobrenome_instrutor AS instrutor,
    COUNT(DISTINCT c.cursoID) AS qtd_cursos,
    COUNT(DISTINCT m.alunoID) AS total_alunos,
    ROUND(AVG(av.nota_prova), 2) AS media_geral_avaliacoes
FROM instrutores i
LEFT JOIN 
    cursos c ON i.instrutorID = c.instrutorID
LEFT JOIN 
    matriculas m ON c.cursoID = m.cursoID
LEFT JOIN 
    avaliacoes av ON c.cursoID = av.cursoID
GROUP BY 
    i.instrutorID, instrutor
ORDER BY 
    media_geral_avaliacoes DESC;





-- Top 5 cursos mais rentáveis (considerar valor_pago das matrículas) 

SELECT 
    c.cursoID,
    c.titulo_curso,
    SUM(m.valor_pago) AS faturamento_total,
    COUNT(m.matriculaID) AS num_matriculas
FROM cursos c
JOIN 
    matriculas m ON c.cursoID = m.cursoID
GROUP BY 
    c.cursoID, c.titulo_curso
ORDER BY 
    faturamento_total DESC
LIMIT 5;





-- Alunos que não concluíram nenhum curso nos últimos 6 meses
SELECT 
    a.alunoID,
    a.nome_aluno || ' ' || a.sobrenome_aluno AS nome_completo,
    a.email
FROM alunos a
WHERE 
    a.alunoID NOT IN (
        SELECT 
            m.alunoID
        FROM 
            matriculas m
        WHERE 
            m.data_conclusao IS NOT NULL
            AND m.data_conclusao >= CURRENT_DATE - INTERVAL '6 months'
    )
ORDER BY 
    nome_completo;
