-- Script SQL separado para criação do schema 

CREATE TABLE alunos(
    alunoID SERIAL PRIMARY KEY,
    nome_aluno VARCHAR(35) NOT NULL,
    sobrenome_aluno VARCHAR(50) NOT NULL,
    email VARCHAR(80) UNIQUE NOT NULL,
    telefone VARCHAR(13),
    data_nascimento DATE,
    data_cadastro DATE
);

CREATE TABLE especialidades(
    especialidadeID SERIAL PRIMARY KEY,
    nome_especialidade VARCHAR(50) NOT NULL
);

CREATE TABLE instrutores(
    instrutorID SERIAL PRIMARY KEY,
    especialidadeID INT NOT NULL,
    nome_instrutor VARCHAR(30)NOT NULL,
    sobrenome_instrutor VARCHAR(50) NOT NULL,
    email_instrutor VARCHAR(80) UNIQUE NOT NULL,
    data_cadastro DATE NOT NULL,
    biografia VARCHAR(500),
    FOREIGN KEY(especialidadeID) REFERENCES especialidades(especialidadesID)
);

CREATE TABLE instrutor_especialidades(
    especialidadeID INT NOT NULL,
    instrutorID INT NOT NULL,
    FOREIGN KEY (especialidadeID) REFERENCES especialidades(especialidadeID),
    FOREIGN KEY (instrutorID) REFERENCES instrutores(instrutorID),
    PRIMARY KEY(especialidadeID, instrutorID)
);

CREATE TABLE categoria_cursos(
    categoriaID SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(50) NOT NULL UNIQUE
);

CREATE TYPE dificuldade_enum AS ENUM('iniciante','intermediario','avancado');

CREATE TABLE cursos(
    cursoID SERIAL PRIMARY KEY,
    categoriaID INT NOT NULL,
    instrutorID INT NOT NULL,
    titulo_curso VARCHAR(150) NOT NULL,
    carga_horaria INT NOT NULL,
    nivel_dificuldade dificuldade_enum NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    data_criacao DATE NOT NULL,
    descricao TEXT NOT NULL,
    FOREIGN KEY(categoriaID) REFERENCES categoria_cursos(categoriaID),
    FOREIGN KEY(instrutorID) REFERENCES instrutores(instrutorID)
);

CREATE TYPE status_enum AS ENUM ('ativa','concluida', 'cancelada');

CREATE TABLE matriculas(
    matriculaID SERIAL PRIMARY KEY,
    alunoID INT NOT NULL,
    cursoID INT NOT NULL,
    data_matricula DATE NOT NULL,
    data_conclusao DATE,
    status_matricula status_enum NOT NULL DEFAULT 'ativa',
    valor_pago DECIMAL(10,2) NOT NULL,
    certificado_emitido BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY(alunoID) REFERENCES alunos(alunoID),
    FOREIGN KEY(cursoID) REFERENCES cursos(cursoID),
    CONSTRAINT unica_matricula_por_aluno UNIQUE (alunoID, cursoID)
);

CREATE TABLE modulos(
    moduloID SERIAL PRIMARY KEY,
    cursoID INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    ordem INT NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    FOREIGN KEY(cursoID) REFERENCES cursos(cursoID),
    CONSTRAINT ordem_unica_por_curso UNIQUE (cursoID, ordem)
);

CREATE TYPE tipo_conteudo_enum AS ENUM ('video', 'texto', 'quiz');

CREATE TABLE aulas(
    aulaID SERIAL PRIMARY KEY,
    moduloID INT NOT NULL,
    titulo VARCHAR(50) NOT NULL,
    ordem INT NOT NULL,
    duracao_minutos INT NOT NULL,
    tipo tipo_conteudo_enum NOT NULL,
    conteudo BYTEA,
    FOREIGN KEY(moduloID) REFERENCES modulos(moduloID),
    CONSTRAINT ordem_unica_por_modulo UNIQUE (moduloID, ordem)
);

CREATE TYPE avaliacao_enum AS ENUM('extra','comum','final');

CREATE TABLE avaliacoes(
    avaliacaoID SERIAL PRIMARY KEY,
    matriculaID INT NOT NULL,
    cursoID INT NOT NULL,
    nome_prova VARCHAR(30) NOT NULL,
    nota_prova INT NOT NULL,
    tipo_avaliacao avaliacao_enum NOT NULL,
    comentario VARCHAR(300),
    data_avaliacao DATE,
    FOREIGN KEY(matriculaID) REFERENCES matriculas(matriculaID),
    FOREIGN KEY(cursoID) REFERENCES cursos(cursoID)
);

CREATE TABLE progresso_aulas(
    progresso_aulaID SERIAL PRIMARY KEY,
    aulaID INT NOT NULL,
    matriculaID INT NOT NULL,
    concluida BOOLEAN DEFAULT FALSE NOT NULL,
    data_conclusao DATE,
    tempo_assistido_minutos INT,
    FOREIGN KEY(aulaID) REFERENCES aulas(aulaID),
    FOREIGN KEY(matriculaID) REFERENCES matriculas(matriculaID),
    CONSTRAINT unica_aula_por_matricula UNIQUE (aulaID, matriculaID)

);

-- CRIAÇAO DA FUNÇÃO E DO TRIGGER
CREATE OR REPLACE FUNCTION verificar_notafinal()
RETURNS TRIGGER AS
$$
BEGIN
-- aqui é veificado se foi inserida uma nota final e uma nota igual ou acima de 7.
    IF NEW.tipo_avaliacao = 'final' AND NEW.nota_prova >= 7 THEN
        UPDATE matriculas
        SET certificado_emitido = TRUE
        WHERE matriculaID = NEW.matriculaID;
	ELSE
	   RAISE NOTICE 'Nota menor que 7. Certificado não emitido para a matrícula %', NEW.matriculaID;
       
    END IF;
    RETURN NEW;
END;
$$ language plpgsql;


CREATE TRIGGER trigger_verificar_notafinal
AFTER INSERT ON avaliacoes
FOR EACH ROW
EXECUTE FUNCTION verificar_notafinal();
