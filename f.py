from flask import Flask, render_template_string, render_template, request, redirect, url_for, flash, session
import datetime

app = Flask(__name__)
app.secret_key = "inovajornal"
app.config['SESSION_COOKIE_NAME'] = "revolucao_jn"

# Simulador de banco de dados (expanda para usar SQL/ORM)
artigos = [
    {
        "id": 1,
        "titulo": "Tecnologia Revoluciona o Jornalismo",
        "categoria": "Tecnologia",
        "autor": "Equipe JN",
        "data": "2025-11-03",
        "imagem": "https://www.gazetadopovo.com.br/static_content/public/images/2021/10/jornal-nacional-1.png",
        "texto": "O avanço tecnológico transformou o modo como as notícias são produzidas, distribuídas e consumidas. Plataformas digitais tornam o jornalismo mais ágil, interativo e democrático.",
        "video": "https://www.youtube.com/embed/I5syfw5zgnc",
        "comentarios": [],
        "destaque": True
    },
    # Adicione vários artigos, matérias, vídeos e colunas simuladas para expandir...
]

usuarios = [
    {"email": "admin@jn.com", "senha": "admin", "nome": "Equipe JN"},
    # Cadastre mais usuários
]

CATEGORIAS = ['Tecnologia', 'Política', 'Economia', 'Mundo', 'Saúde', 'Cultura', 'Esporte']

# Templates gigantes, separando partes em variáveis (no projeto real, usar os arquivos da pasta templates)
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>JN Digital - Revolução Jornalística</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"/>
<style>
body {
    font-family: 'Segoe UI', 'Montserrat', Arial, sans-serif;
    background: linear-gradient(140deg,#273c75 60%,#487eb0 99%);
    color:#fff;
    margin:0;
    min-height:100vh;
}
a.navbar-brand, .nav-link, h1, h2, h3, .btn {
    font-family:'Montserrat',sans-serif;
}
.navbar {background: #162447;}
.navbar-brand{font-size:2.1rem; font-weight:800; color:#40a3ff;}
.nav-link{color:#fff!important;}
.jn-banner{
    width:100%;max-width:1680px;margin:auto;
    background:linear-gradient(120deg,#2980b9 70%,#6dd5fa 100%);
    box-shadow:0 6px 45px rgba(46,60,120,0.22);
    border-radius:34px;
    padding:62px 4vw 54px 4vw;
    margin:42px 0 34px 0;
    color:#fff;text-shadow:0 2px 8px #35579077;
}
.jn-banner h1{font-size:3.2rem;font-weight:900;letter-spacing:-2px;}
.jn-banner .lead{font-size:1.5rem;}
.jn-banner .destaques{margin-top:38px;}
.section-title{font-family:'Montserrat';font-size:2.2rem;margin:35px 0 18px 0; font-weight:800;color:#1e90ff;}
.card{border-radius:20px;box-shadow:0 8px 40px #1325ab11;}
.card-img-top{border-radius:18px 18px 0 0;object-fit:cover;height:170px;background:#e5e9f2;}
.card:hover{transform:scale(1.025);box-shadow:0 14px 58px #4989c926;}
footer{
    background:#182952;color:#cfd2dc;padding:42px 0;margin-top:46px;font-family:'Montserrat',sans-serif;
    text-align:center;font-size:1.2rem;font-weight:600;letter-spacing:-1px;
}
@media(max-width:900px){.jn-banner h1{font-size:2.05rem;}.jn-banner{padding:36px 12px 32px 12px;}}
</style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark sticky-top shadow-lg">
 <div class="container-fluid">
   <a class="navbar-brand" href="/">JN Digital</a>
   <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#jnnav"><span class="navbar-toggler-icon"></span></button>
   <div class="collapse navbar-collapse" id="jnnav">
     <ul class="navbar-nav me-auto mb-2 mb-lg-0">
      {% for cat in categorias %}
      <li class="nav-item"><a class="nav-link" href="{{ url_for('categoria', nome=cat) }}">{{ cat }}</a></li>
      {% endfor %}
      <li class="nav-item"><a class="nav-link" href="{{ url_for('sobre') }}">Sobre</a></li>
    </ul>
    <form class="d-flex" method="GET" action="{{ url_for('buscar') }}">
        <input class="form-control me-2" type="search" name="q" placeholder="Busque pelo título..." aria-label="Buscar">
        <button class="btn btn-outline-info" type="submit">Buscar</button>
    </form>
    {% if 'user' in session %}
        <span class="px-3">Olá, {{ session['user'] }}!</span>
        <a href="{{ url_for('logout') }}" class="btn btn-warning">Sair</a>
    {% else %}
        <a href="{{ url_for('login') }}" class="btn btn-primary ms-2">Entrar</a>
    {% endif %}
   </div>
 </div>
</nav>

<div class="jn-banner">
    <h1>Bem-vindo ao <span style="color:#e4ff09;text-shadow:0 0 24px #3719efbb;">JN Digital</span></h1>
    <p class="lead">A revolução digital do jornalismo, conectando você com as notícias mais relevantes, interativas e dinâmicas do Brasil e do mundo. Interaja, comente, participe!</p>
    <div class="destaques row py-4">
        {% for art in artigos if art.destaque %}
        <div class="col-12 col-md-6 col-lg-4 mb-4">
          <a href="{{ url_for('materia', id=art.id) }}" style="text-decoration:none">
            <div class="card h-100 bg-dark text-white shadow">
                {% if art.imagem %}
                <img src="{{ art.imagem }}" class="card-img-top" alt="{{ art.titulo }}">
                {% endif %}
                <div class="card-body">
                  <h3 class="card-title">{{ art.titulo }}</h3>
                  <p class="card-text">{{ art.texto[:110] }}...</p>
                  <p class="mb-1"><span class="badge bg-info">{{ art.categoria }}</span> <span style="color:#86bbef;font-size:0.95rem;"> • {{ art.data }}</span></p>
                </div>
            </div>
          </a>
        </div>
        {% endfor %}
    </div>
</div>

<div class="container">
    <div class="section-title">Últimas Notícias</div>
    <div class="row">
        {% for art in artigos %}
        <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
          <a href="{{ url_for('materia', id=art.id) }}" style="text-decoration:none">
          <div class="card h-100">
                {% if art.imagem %}
                <img src="{{ art.imagem }}" class="card-img-top" alt="{{ art.titulo }}">
                {% endif %}
                <div class="card-body text-dark">
                  <div class="fw-bold">{{ art.titulo[:70] }}{% if art.titulo|length>70 %}...{% endif %}</div>
                  <div style="font-size:.93rem;color:#234;font-weight:500;">{{ art.categoria }} • {{ art.data }}</div>
                </div>
          </div>
          </a>
        </div>
        {% endfor %}
    </div>
</div>

<footer>
JN Digital &copy; 2025 • Inspirado pelo Jornal Nacional <br>
Notícias confiáveis, interativas e acessíveis a todos.
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

MATERIA_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{{ artigo.titulo }} | JN Digital</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"/>
<style>
body{font-family:'Segoe UI','Montserrat',Arial,sans-serif;background:#21293f;color:#fff;}
.container{max-width:900px;padding:36px;}
.card-img-top{width:100%;max-width:720px;margin:auto;border-radius:18px;}
h1{font-family:'Montserrat',sans-serif;font-size:2.4rem;font-weight:900; color:#aedcff;}
.meta{color:#86bbef;font-size:1.15rem;margin-bottom:10px;}
.comentarios{margin-top: 34px;}
.comentarios textarea{width:100%;min-height:60px;border-radius:7px;}
.comentarios-list{margin:18px 0;}
.comentario-item{background:#334c80;color:#fff;border-radius:12px;padding:10px;margin-bottom:10px;}
.video-box{margin:24px 0;}
</style>
</head>
<body>
<a href="/" class="btn btn-outline-light my-4">&larr; Início</a>
<div class="container">
  <h1>{{ artigo.titulo }}</h1>
  <div class="meta">{{ artigo.categoria }} &bull; {{ artigo.data }} &bull; Por {{ artigo.autor }}</div>
  {% if artigo.imagem %}
  <img src="{{ artigo.imagem }}" class="card-img-top mb-4" alt="Imagem da matéria">
  {% endif %}
  <div class="mb-4">{{ artigo.texto }}</div>
  {% if artigo.video %}
  <div class="video-box">
    <iframe width="100%" height="300" src="{{ artigo.video }}" title="JN Vídeo" frameborder="0" allowfullscreen></iframe>
  </div>
  {% endif %}
  <div class="comentarios">
    <h3>Comentários</h3>
    <form method="POST">
      <textarea name="texto" required placeholder="Comente aqui..."></textarea>
      <button type="submit" class="btn btn-success my-2">Enviar</button>
    </form>
    <div class="comentarios-list">
      {% for com in artigo.comentarios %}
      <div class="comentario-item"><strong>{{ com['autor'] }}</strong>: {{ com['texto'] }} <span style="font-size:0.86rem;color:#bbe;">({{ com['data'] }})</span></div>
      {% endfor %}
      {% if not artigo.comentarios %}<div>(Nenhum comentário ainda.)</div>{% endif %}
    </div>
  </div>
</div>
</body>
</html>
'''

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Entrar | JN Digital</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"/>
<body style="background:#18427c;">
 <div class="container py-5" style="max-width:480px;">
  <h2 style="color:#82c4ff;">Entrar no JN Digital</h2>
  <form method="POST" class="mb-4 mt-4">
    <div class="mb-3">
      <label>Email</label>
      <input type="email" name="email" class="form-control" required>
    </div>
    <div class="mb-3">
      <label>Senha</label>
      <input type="password" name="senha" class="form-control" required>
    </div>
    <button class="btn btn-primary w-100">Entrar</button>
  </form>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <div class="alert alert-info">
        {% for msg in messages %} <div>{{ msg }}</div> {% endfor %}
      </div>
    {% endif %}
  {% endwith %}
  <a href="/" class="btn btn-secondary mt-4 w-100">Voltar</a>
 </div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
</body>
'''

# Rotas principais

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE, artigos=artigos, categorias=CATEGORIAS)

@app.route("/materia/<int:id>", methods=['GET','POST'])
def materia(id):
    artigo = next((a for a in artigos if a["id"]==id), None)
    if not artigo:
        return "Não encontrada",404
    if request.method=='POST':
        texto = request.form.get("texto","")
        autor = session.get('user','Anônimo')
        artigo["comentarios"].append({
            "texto":texto,
            "autor":autor,
            "data":datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        })
    return render_template_string(MATERIA_TEMPLATE, artigo=artigo)

@app.route("/buscar")
def buscar():
    termo = request.args.get("q","").strip().lower()
    resultados = [a for a in artigos if termo in a["titulo"].lower()]
    return render_template_string(HOME_TEMPLATE, artigos=resultados, categorias=CATEGORIAS)

@app.route("/categoria/<nome>")
def categoria(nome):
    filtrados = [a for a in artigos if a["categoria"].lower()==nome.lower()]
    return render_template_string(HOME_TEMPLATE, artigos=filtrados, categorias=CATEGORIAS)

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get("email")
        senha = request.form.get("senha")
        user = next((u for u in usuarios if u["email"]==email and u["senha"]==senha), None)
        if user:
            session['user'] = user["nome"]
            return redirect(url_for("home"))
        else:
            flash("Credenciais incorretas")
    return render_template_string(LOGIN_TEMPLATE)

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("home"))

@app.route("/sobre")
def sobre():
    return "<h3>JN Digital é uma iniciativa para revolucionar o jornalismo digital usando Python e Flask.<br>Inspirado no Jornal Nacional, trazendo dinamismo, tecnologia, comentários ao vivo e integração multimídia.</h3>"

if __name__ == "__main__":
    app.run(debug=True)
