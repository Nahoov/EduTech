from conexao_banco import conecta, encerra_conexao 
from faker import Faker
from datetime import datetime, timedelta 
import random
fake = Faker(locale='pt-BR')


data_hoje = datetime.now() 


data_inicio = data_hoje - timedelta(days=2*365)

data_curso_criado = data_hoje - timedelta(days=4*365)



# CONECTANDO AO BANCO DE DADOS
connection = conecta()
cursor = connection.cursor()



# LISTAS DE NOMES

titulo_cursos = ['Fundamentos de Programação Back-end',
  'Desenvolvimento de APIs RESTful com Node.js',
  'Banco de Dados Relacionais com PostgreSQL','Controle de Versão com Git e GitHub',
  'Colaboração e Pull Requests no GitHub','DevOps: Fundamentos e Cultura Ágil',
  'Docker para Desenvolvedores Back-end','Fundamentos de Desenvolvimento Front-end',
  'Introdução ao HTML5 e Estrutura de Páginas Web',
  'CSS3: Estilos e Layouts Modernos',
  'Design Responsivo com Flexbox e Grid',
  'JavaScript Essencial',
  'Manipulação do DOM com JavaScript',
  'Boas Práticas e Padrões de Código Front-end',
  'Lógica da programação',
  'Introdução ao TypeScript',
  'Kubernetes',
  'CI/CD: Integração e Entrega Contínua','Criptografia e Proteção de Dados',
  'Segurança na Nuvem (Cloud Security)',
  'Gestão de Identidades e Acessos (IAM)']

titulo_aulas = ['aprenderemos...', 'desenvolveremos...', 'conceitos...']

titulo_modulos = ['Módulo Inicial', 'Módulo Fundamental', 'Módulo de Prática', 'Módulo Avançado', 
                 'Módulo Especial', 'Módulo de Exploração', 'Módulo Intermediário', 'Módulo de Aplicação', 
                 'Módulo de Desafio', 'Módulo de Integração', 'Módulo de Desenvolvimento', 'Módulo Essencial', 
                 'Módulo de Experiência', 'Módulo de Conhecimento', 'Módulo de Aprimoramento', 'Módulo de Competências', 
                 'Módulo de Projetos', 'Módulo de Técnicas', 'Módulo de Estratégias', 'Módulo de Referência']



#(em inglês pois o pyfloat só reconhece esses parametros)
left_digits = 8 # digitos antes da virgula
right_digits = 2  # digitos após o ponto



# COMANDOS PARA PROCURAR IDS DE CADA TABELA
cursor.execute("SELECT especialidadeID FROM especialidades")
especialidadesids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT categoriaID FROM categoria_cursos")
categoriasids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT instrutorID FROM instrutores")
instrutoresids= [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT moduloID FROM modulos")
modulosids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT cursoID FROM cursos")
cursosids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT alunoID FROM alunos")
alunosids= [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT matriculaID FROM matriculas")
matriculasids=[row[0] for row in cursor.fetchall()]

cursor.execute("SELECT aulaID FROM aulas")
aulasids=[row[0] for row in cursor.fetchall()]


# FORMATO DO NUMERO DE TELEFONE > fake.numerify()
formato_desejado = '## ########' 




#FUNÇÕES PARA GERAR DADOS FAKES PARA AS TABELAS

def gerar_alunos(quantidade):
    for i in range(quantidade):
        nome_aluno = fake.first_name()
        sobrenome_aluno = fake.last_name()
        email = fake.email()
        telefone = fake.numerify(formato_desejado)
        data_nascimento = fake.date_of_birth(minimum_age=15, maximum_age=80)
        data_cadastro = fake.date_between(start_date = data_inicio, end_date = data_hoje)
        cursor.execute("""
                       INSERT INTO alunos (nome_aluno, sobrenome_aluno, email, telefone, data_nascimento, data_cadastro)
                       VALUES (%s, %s, %s, %s, %s, %s)""",(nome_aluno, sobrenome_aluno, email, telefone, data_nascimento, data_cadastro))
        connection.commit()
        print("dados enviados com sucesso")






def gerar_instrutores(quantidade):
    for i in range(quantidade):
        nome_instrutor = fake.first_name()
        sobrenome_instrutor = fake.last_name()
        email_instrutor = fake.email()
        data_cadastro = fake.date_between(start_date = data_inicio, end_date = data_hoje)
        biografia = fake.text()
        especialidadeID = random.choice(especialidadesids)
        cursor.execute("""
                       INSERT INTO instrutores (nome_instrutor, sobrenome_instrutor, email_instrutor, data_cadastro, biografia, especialidadeID)
                       VALUES (%s, %s, %s, %s, %s, %s)""",(nome_instrutor, sobrenome_instrutor, email_instrutor, data_cadastro, biografia, especialidadeID))
        connection.commit() 
        print("enviados com sucesso")






def gerar_cursos(quantidade):
    for i in range(quantidade):
        titulo_curso = random.choice(titulo_cursos)
        carga_horaria = fake.random_int(min=2, max=50)
        nivel_dificuldade = random.choice(['iniciante','intermediario','avancado'])
        preco = fake.pyfloat(left_digits=8, right_digits=2, min_value=200, max_value=2300, positive= True)
        data_criacao = fake.date_between(start_date = data_curso_criado, end_date = data_hoje)
        descricao = fake.text()
        categoriaID = random.choice(categoriasids) 
        instrutorID = random.choice(instrutoresids) 
        cursor.execute("""INSERT INTO cursos (titulo_curso, carga_horaria, nivel_dificuldade, preco, data_criacao, descricao, categoriaID, instrutorID)
                       VALUES(%s, %s, %s, %s, %s, %s,%s,%s)""",(titulo_curso, carga_horaria, nivel_dificuldade, preco, data_criacao, descricao, categoriaID, instrutorID))
        connection.commit()
        print("Dados enviados com sucesso!")






def gerar_modulos():
    qtd_modulos_por_curso = 3

    for cursoID in cursosids:  
        for ordem in range(1, qtd_modulos_por_curso + 1):  
            titulo = random.choice(titulo_modulos)
            descricao = fake.text()

            cursor.execute("""
                INSERT INTO modulos (titulo, ordem, descricao, cursoID)
                VALUES (%s, %s, %s, %s)
            """, (titulo, ordem, descricao, cursoID))

        connection.commit()

    print("Módulos gerados: 3 por curso!")






def gerar_aulas():
    for moduloID in modulosids:  
        qtd_aulas = random.randint(2, 4)  

        for ordem in range(1, qtd_aulas + 1):  
            titulo = random.choice(titulo_aulas)
            duracao_minutos = fake.random_int(min=5, max=90)
            tipo = random.choice(['video', 'texto', 'quiz'])

            cursor.execute("""
                INSERT INTO aulas (titulo, ordem, duracao_minutos, tipo, moduloID)
                VALUES (%s, %s, %s, %s, %s)""", (titulo, ordem, duracao_minutos, tipo, moduloID))

        connection.commit()

    print("Aulas geradas com sucesso, variando entre 2 e 4 por módulo!")






def gerar_matriculas(quantidade):
    for i in range(quantidade):
        data_matricula = fake.date_between(start_date = data_inicio, end_date = data_hoje)
        #data_conclusao =
        status_matricula = random.choice(['ativa','concluida','cancelada'])
        valor_pago = fake.pyfloat(left_digits=8, right_digits=2, min_value=49.90, max_value= 499.90, positive= True)
        #certificado_emitido = 
        cursoID =random.choice(cursosids)
        alunoID = random.choice(alunosids)
        cursor.execute("""INSERT INTO matriculas(data_matricula, status_matricula, valor_pago, cursoID, alunoID) VALUES
                       (%s,%s,%s,%s,%s)""",(data_matricula, status_matricula, valor_pago, cursoID, alunoID))
        
        connection.commit()

        print("Dados enviados com sucesso!")







def gerar_avaliacoes(quantidade):
    for i in range(quantidade):
        nome_prova = random.choice(['prova','teste'])
        nota_prova = fake.random_int(min=7, max=10)
        tipo_avaliacao = random.choice(['extra','comum','final'])
        comentario = fake.text()
        data_avaliacao = fake.date_between(start_date = data_inicio, end_date = data_hoje)
        matriculaID = random.choice(matriculasids)
        cursoID = random.choice(cursosids)
        cursor.execute("""INSERT INTO avaliacoes (nome_prova, nota_prova, tipo_avaliacao, comentario, data_avaliacao, matriculaID, cursoID)
                        VALUES(%s,%s,%s,%s,%s,%s,%s)""", (nome_prova, nota_prova, tipo_avaliacao, comentario, data_avaliacao, matriculaID, cursoID))
        connection.commit()
        print("Dados enviados com sucesso!")






    
def gerar_progresso_aulas(quantidade): 
    for i in range(quantidade):
        aulaID = random.choice(aulasids)
        matriculaID = random.choice(matriculasids)
        tempo_assistido_minutos = fake.random_int(min=5, max=90)
        cursor.execute("""INSERT INTO progresso_aulas (aulaID, matriculaID, tempo_assistido_minutos)
                        VALUES (%s,%s, %s) """, (aulaID, matriculaID, tempo_assistido_minutos))
        connection.commit()
        print("enviados")   





def enviar_dados_instrutor_especialidades():
    for instrutorID in instrutoresids:
        
        qtd_especialidades = random.randint(1,3)

        especialidades_instrutor = random.sample(especialidadesids, qtd_especialidades)
        
        for especialidadeID in especialidades_instrutor:
            cursor.execute("""INSERT INTO instrutor_especialidades(instrutorID, especialidadeID)
                        VALUES (%s, %s)""", (instrutorID, especialidadeID))
            connection.commit()
            print("enviados")



encerra_conexao(connection)
