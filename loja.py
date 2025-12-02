from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "segredo"

def gen(tipo, qtd, genero, img_base):
    return [
        {
            "id": f"{tipo.lower().replace(' ','_')}_{genero.lower()}_{i}",
            "nome": f"{tipo.title()} {genero} {i+1}",
            "desc": f"{tipo.title()} para {genero.lower()} de alta performance.",
            "imagem": img_base,
            "preco": 59 + (i % 90),
            "genero": genero,
            "tipo": tipo.lower()  # para identificar categoria do produto
        } for i in range(qtd)
    ]

artigos_femininos = gen("Meia Cano Curto", 50, "Feminino", "https://cdn.awsli.com.br/600x600/645/645246/produto/144867983/meia-cano-curto-nike-dry-cushion-3-par-black-nikemcc153---06801280031-black-7349ad53.jpg") \
    + gen("Segunda Pele", 50, "Feminino", "https://static.centauro.com.br/900x900/82826601.jpg") \
    + gen("Bermuda Esportiva", 50, "Feminino", "https://images.tcdn.com.br/img/img_prod/1081983/bermuda_nike_feminina_sportswear_14521_1_20210520161036.jpg")

artigos_masculinos = gen("Meia Cano Longo", 50, "Masculino", "https://cdn.awsli.com.br/600x600/1016/1016959/produto/67618071/meia-nike-cano-alto-classic-3-pack-nike-3394-550f6416.jpg") \
    + gen("Bermuda Esportiva", 50, "Masculino", "https://images.tcdn.com.br/img/img_prod/1081983/bermuda_nike_feminina_sportswear_14521_1_20210520161036.jpg") \
    + gen("Joelheira", 50, "Masculino", "https://images.tcdn.com.br/img/img_prod/600054/joelheira_elastica_fisioterapia_664_1_20200819151207.jpg")

todos_artigos = artigos_femininos + artigos_masculinos

def buscar_produto_por_id(produto_id):
    for art in todos_artigos:
        if art["id"] == produto_id:
            return art
    return None

### HTML: página inicial estilo Netshoes ampliada e responsiva, com banner, buscas e destaque de categorias ###
HTML_HOME = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GRMN STORE - Loja Esportiva</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css?family=Montserrat:700|Rubik:400,600&display=swap" rel="stylesheet">
<style>
body {
    font-family: 'Rubik', Arial, sans-serif;
    background: linear-gradient(-45deg,#ecf0f3,#c3d5fe,#fff,#e3e7fa);
    animation: bgmove 16s ease-in-out infinite;
    margin:0; padding:0;
}
@keyframes bgmove {
  0% {background-position:0% 50%;}
  50% {background-position:100% 50%;}
  100% {background-position:0% 50%;}
}
.menu-blur {backdrop-filter: blur(4px);}
.navbar {
    box-shadow: 0 4px 20px #aaccf933;
    background: rgba(255,255,255,.98)!important;
}
.logo-netshoes { height:62px; margin-right:22px; }
.nav-link {color:#5840ba!important;font-weight:600;}
.nav-link.active, .nav-link:focus, .nav-link:hover {color:#fff;background:#5840ba!important;}
.search-input {
    border-radius:2rem; border:none; padding:.7rem 1.3rem; min-width:280px;
}
.banner {
    min-height:380px;
    color:#fff;
    background: linear-gradient(120deg,#4529e4 60%,#37b8ff 97%);
    border-radius:28px;
    margin:32px 0 40px;
    box-shadow:0 8px 80px #843bd233;
    display:flex;flex-direction:column;align-items:center;
    justify-content:center;text-align:center;position:relative;
    padding:48px 10vw 56px 10vw;
}
.banner h1{
    font-family: 'Montserrat',sans-serif;
    font-size:3.4rem;
    font-weight:900;
    letter-spacing:-2px;
    user-select:none;
}
.banner .cta {
    margin-top:30px;
    font-weight:700;
    font-size:1.45rem;
    padding:12px 36px;
}
.banner .desc {
    font-size:1.8rem;
    margin-top:18px;
    opacity:0.88;
    user-select:none;
}
.prod-categ {
    font-size:2.6rem;
    font-family:'Montserrat';
    color:#4739b3;
    font-weight:900;
    margin-top:35px;
    margin-bottom:15px;
    user-select:none;
}
.card{
    border-radius:28px;
    box-shadow:0 8px 38px 0 #6d57cf10;
    transition:box-shadow 0.3s, transform 0.3s;
    cursor:pointer;
}
.card:hover{
    box-shadow:0 14px 52px 0 #ab9bfc22;
    transform:scale(1.05);
}
.card-img-top {
    border-radius:24px 24px 0 0;
    height:190px;
    object-fit:contain;
    background:#f5f7fd;
}
.btn-success {
    background:linear-gradient(90deg,#6e36f9 80%,#69f5f7);
    color:#fff;
    font-weight:800;
    border:0;
    transition: background 0.3s;
}
.btn-success:hover {
    background:linear-gradient(90deg,#5c2ecc 80%,#40c4f8);
}
footer {
    background:#4329bd;
    color:#fff;
    padding:40px 0;
    margin-top:60px;
    text-align:center;
    font-weight:600;
}
@media (max-width: 768px){
    .prod-categ{font-size:1.6rem;}
    .banner h1{font-size:2rem; padding:0 10px;}
    .banner .desc{font-size:1rem;}
    .banner{padding:28px 15px 40px 15px;}
    .card-img-top{height:130px;}
}
</style>
</head>
<body>
<nav class="navbar navbar-expand-lg menu-blur sticky-top">
    <div class="container-fluid">
        <a href="/" class="navbar-brand d-flex align-items-center">
            <img src="/logo_grmnstore" class="logo-netshoes" alt="GRMN Store"> 
            <span style="font-family:Montserrat;font-size:2.3rem;font-weight:700;color:#4739b3;">GRMN STORE</span>
        </a>
        <form class="d-flex" action="{{ url_for('buscar') }}" method="get" role="search">
            <input class="form-control search-input me-2" type="search" placeholder="Buscar produtos, marcas..." name="q" aria-label="Buscar produtos">
            <button class="btn btn-outline-primary" type="submit" aria-label="Buscar">Buscar</button>
        </form>
        <a href="{{ url_for('cadastro') }}" class="btn btn-primary ms-3">Cadastro / Login</a>
    </div>
</nav>

<div class="container px-3 px-md-5">

    <div class="banner" role="banner" aria-label="Bem-vindo à GRMN Store">
        <h1>Bem-vindo(a) à GRMN STORE!</h1>
        <div class="desc">A experiência Netshoes repaginada: estilo, tecnologia e esporte num só lugar.</div>
        <a href="#produtos" class="btn btn-success cta" role="button">Ver Ofertas!</a>
    </div>

    <section aria-labelledby="destaques-femininos">
        <h2 class="prod-categ" id="destaques-femininos">DESTAQUES FEMININOS</h2>
        <div class="row">
            {% for produto in artigos_femininos[:12] %}
            <div class="col-12 col-sm-6 col-lg-4 col-xl-3 mb-4">
              <div class="card h-100" onclick="location.href='{{ url_for('comprar', produto_id=produto.id) }}';" tabindex="0" role="link" aria-label="{{ produto.nome }} - R$ {{ produto.preco }},00">
                <img src="{{ produto.imagem }}" class="card-img-top" alt="{{ produto.nome }}">
                <div class="card-body text-center">
                  <div class="fw-bold mb-1">{{ produto.nome }}</div>
                  <div class="mb-2 text-secondary">{{ produto.desc }}</div>
                  <div class="text-success fs-4 mb-2">R$ {{ produto.preco }},00</div>
                  <a href="{{ url_for('comprar', produto_id=produto.id) }}" class="btn btn-success w-100" tabindex="-1">Comprar</a>
                </div>
              </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <section aria-labelledby="mais-vendidos-masculinos">
        <h2 class="prod-categ" id="mais-vendidos-masculinos">MAIS VENDIDOS MASCULINOS</h2>
        <div class="row">
            {% for produto in artigos_masculinos[:12] %}
            <div class="col-12 col-sm-6 col-lg-4 col-xl-3 mb-4">
              <div class="card h-100" onclick="location.href='{{ url_for('comprar', produto_id=produto.id) }}';" tabindex="0" role="link" aria-label="{{ produto.nome }} - R$ {{ produto.preco }},00">
                <img src="{{ produto.imagem }}" class="card-img-top" alt="{{ produto.nome }}">
                <div class="card-body text-center">
                  <div class="fw-bold mb-1">{{ produto.nome }}</div>
                  <div class="mb-2 text-secondary">{{ produto.desc }}</div>
                  <div class="text-primary fs-4 mb-2">R$ {{ produto.preco }},00</div>
                  <a href="{{ url_for('comprar', produto_id=produto.id) }}" class="btn btn-success w-100" tabindex="-1">Comprar</a>
                </div>
              </div>
            </div>
            {% endfor %}
        </div>
    </section>

</div>

<footer>
    © 2025 GRMN STORE — Para quem vive esporte.
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

### HTML: Página de compra com cálculo de frete e seleção dinâmica de tamanhos ###
HTML_COMPRAR = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Comprar {{ produto.nome }}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"/>
<style>
body {font-family: 'Rubik', Arial, sans-serif; margin:0; padding:0; background:#f7f9fc;}
.container {margin-top:40px;}
.card-img-top {
    border-radius:12px;
    height:280px;
    object-fit:contain;
    background:#eef3fa;
}
h2, h4 {font-family: 'Montserrat', sans-serif;}
.mb-3 label {font-weight:600;}
</style>
</head>
<body>
<div class="container">
    <a href="{{ url_for('home') }}" class="btn btn-outline-secondary mb-3">&larr; Voltar</a>
    <div class="row g-4">
        <div class="col-md-5">
            <img src="{{ produto.imagem }}" alt="{{ produto.nome }}" class="img-fluid rounded shadow card-img-top">
        </div>
        <div class="col-md-7">
            <h2>{{ produto.nome }}</h2>
            <p>{{ produto.desc }}</p>
            <h4>Preço: R$ {{ produto.preco }},00</h4>

            <form method="post" id="compraForm" novalidate>
                <div class="mb-3">
                    <label for="cep" class="form-label">Digite seu CEP para calcular o frete <span aria-hidden="true" title="CEP deve conter 8 dígitos">ℹ️</span>:</label>
                    <input type="text" class="form-control" id="cep" name="cep" maxlength="8" pattern="\\d{8}" required placeholder="Ex: 01001000" aria-describedby="cepHelp" value="{{ cep or '' }}">
                    <div class="form-text" id="cepHelp">Apenas números, 8 dígitos.</div>
                </div>

                <div id="tamanhoSection" class="mb-3" style="display:none;">
                    <label for="tamanho" class="form-label">Escolha o tamanho:</label>
                    <select name="tamanho" id="tamanho" class="form-select" required aria-required="true" aria-describedby="tamanhoHelp">
                        <!-- Opções preenchidas via JS -->
                    </select>
                    <div class="form-text" id="tamanhoHelp">Selecione seu tamanho adequado.</div>
                </div>

                <div class="mb-3">
                    <label>Frete estimado:</label>
                    <p id="freteDisplay" aria-live="polite" aria-atomic="true" style="font-weight:600;">-</p>
                </div>

                <div class="mb-3">
                    <label>Total com frete:</label>
                    <p id="totalDisplay" aria-live="polite" aria-atomic="true" style="font-weight:700;">R$ {{ produto.preco }},00</p>
                </div>

                <button type="submit" class="btn btn-primary">Finalizar Compra</button>
            </form>
        </div>
    </div>
</div>

<script>
    const produtoTipo = "{{ produto.tipo }}".toLowerCase();
    const tamanhoSection = document.getElementById('tamanhoSection');
    const tamanhoSelect = document.getElementById('tamanho');
    const freteDisplay = document.getElementById('freteDisplay');
    const totalDisplay = document.getElementById('totalDisplay');
    const precoProduto = {{ produto.preco }};

    // Define opções de tamanho conforme o tipo do produto
    function definirOpcoesTamanho() {
        tamanhoSelect.innerHTML = '';
        if (produtoTipo.includes('meia') || produtoTipo.includes('tenis')) {
            // Tamanhos pé para meia/tênis
            ['34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45'].forEach(t => {
                let option = document.createElement('option');
                option.value = t; option.text = t;
                tamanhoSelect.appendChild(option);
            });
            tamanhoSection.style.display = 'block';
        } else if (produtoTipo.includes('bermuda') || produtoTipo.includes('segunda pele') || produtoTipo.includes('joelheira')) {
            // Tamanhos P, M, G, GG para roupas/apoios
            ['P', 'M', 'G', 'GG'].forEach(t => {
                let option = document.createElement('option');
                option.value = t; option.text = t;
                tamanhoSelect.appendChild(option);
            });
            tamanhoSection.style.display = 'block';
        } else {
            tamanhoSection.style.display = 'none';
        }
    }
    definirOpcoesTamanho();

    // Validação e cálculo simples do frete baseado no CEP
    document.getElementById('compraForm').addEventListener('submit', function(evt) {
        evt.preventDefault();
        const cep = document.getElementById('cep').value.trim();
        if (!cep.match(/^\\d{8}$/)) {
            alert('Informe um CEP válido com 8 dígitos numéricos.');
            return;
        }
        // Cálculo fictício do valor do frete
        const frete = 15 + ((+cep.slice(-1)) % 10) * 2;
        freteDisplay.textContent = 'R$ ' + frete.toFixed(2).replace('.', ',');
        totalDisplay.textContent = 'R$ ' + (precoProduto + frete).toFixed(2).replace('.', ',');
        alert('Compra finalizada com sucesso! (Simulação)');
    });
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

### HTML: Página de busca por termo, mostrando resultados ###
HTML_BUSCAR = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Buscar produtos</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"/>
<style>
body {font-family: 'Rubik', Arial, sans-serif; background:#f7f9fc; margin:0; padding-bottom:40px;}
.container {padding-top:30px;}
h2 {font-family: 'Montserrat', sans-serif; margin-bottom:30px;}
.card-img-top {
    border-radius:12px;
    height:180px;
    object-fit:contain;
    background:#eef3fa;
}
.card {
    border-radius:20px;
    cursor:pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 40px rgba(0,0,0,0.12);
}
</style>
</head>
<body>
<div class="container">
    <a href="{{ url_for('home') }}" class="btn btn-outline-secondary mb-3">&larr; Voltar</a>
    <h2>Resultados para "{{ termo }}" ({{ resultados|length }})</h2>
    {% if resultados %}
    <div class="row g-3">
        {% for produto in resultados %}
        <div class="col-12 col-sm-6 col-lg-4 col-xl-3">
          <div class="card h-100" onclick="location.href='{{ url_for('comprar', produto_id=produto.id) }}'" role="link" tabindex="0" aria-label="{{ produto.nome }} - R$ {{ produto.preco }},00">
            <img src="{{ produto.imagem }}" class="card-img-top" alt="{{ produto.nome }}">
            <div class="card-body text-center">
              <div class="fw-bold mb-1">{{ produto.nome }}</div>
              <div class="text-secondary mb-2" style="font-size:0.9rem;">{{ produto.desc }}</div>
              <div class="text-success fs-5 mb-1">R$ {{ produto.preco }},00</div>
              <a href="{{ url_for('comprar', produto_id=produto.id) }}" class="btn btn-success w-100" tabindex="-1">Comprar</a>
            </div>
          </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p>Nenhum produto encontrado.</p>
    {% endif %}
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

### HTML: Página cadastro/login com abas usando Bootstrap ###
HTML_CADASTRO = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Cadastro e Login</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"/>
<style>
body {font-family: 'Rubik', Arial, sans-serif; background:#f7f9fc;}
.container {padding-top:40px; max-width: 480px;}
.nav-tabs .nav-link.active {
    background-color: #673ab7;
    color: white;
    font-weight: 700;
}
</style>
</head>
<body>
<div class="container">
    <a href="{{ url_for('home') }}" class="btn btn-outline-secondary mb-4">&larr; Voltar</a>
    <h2>Cadastro e Login</h2>
    <ul class="nav nav-tabs" id="authTab" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="login-tab" data-bs-toggle="tab" data-bs-target="#login" type="button" role="tab" aria-controls="login" aria-selected="true">Login</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="registro-tab" data-bs-toggle="tab" data-bs-target="#registro" type="button" role="tab" aria-controls="registro" aria-selected="false">Cadastro</button>
        </li>
    </ul>
    <div class="tab-content mt-4" id="authTabContent">
        <div class="tab-pane fade show active" id="login" role="tabpanel" aria-labelledby="login-tab">
            <form method="post" action="{{ url_for('login') }}">
                <div class="mb-3">
                    <label for="loginEmail" class="form-label">Email</label>
                    <input type="email" class="form-control" id="loginEmail" name="email" required autocomplete="username">
                </div>
                <div class="mb-3">
                    <label for="loginSenha" class="form-label">Senha</label>
                    <input type="password" class="form-control" id="loginSenha" name="senha" required autocomplete="current-password">
                </div>
                <button type="submit" class="btn btn-primary w-100">Entrar</button>
            </form>
        </div>
        <div class="tab-pane fade" id="registro" role="tabpanel" aria-labelledby="registro-tab">
            <form method="post" action="{{ url_for('registro') }}">
                <div class="mb-3">
                    <label for="regNome" class="form-label">Nome</label>
                    <input type="text" class="form-control" id="regNome" name="nome" required autocomplete="name">
                </div>
                <div class="mb-3">
                    <label for="regEmail" class="form-label">Email</label>
                    <input type="email" class="form-control" id="regEmail" name="email" required autocomplete="email">
                </div>
                <div class="mb-3">
                    <label for="regSenha" class="form-label">Senha</label>
                    <input type="password" class="form-control" id="regSenha" name="senha" required autocomplete="new-password">
                </div>
                <button type="submit" class="btn btn-success w-100">Registrar</button>
            </form>
        </div>
    </div>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div class="alert alert-info mt-4" role="alert">
                {% for msg in messages %}
                    <div>{{ msg }}</div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

### Flask routes ###

@app.route('/')
def home():
    return render_template_string(HTML_HOME, artigos_femininos=artigos_femininos, artigos_masculinos=artigos_masculinos)

@app.route('/comprar/<produto_id>', methods=['GET','POST'])
def comprar(produto_id):
    produto = buscar_produto_por_id(produto_id)
    if not produto:
        return "Produto não encontrado", 404
    cep = None
    if request.method == 'POST':
        cep = request.form.get('cep','').strip()
        tamanho = request.form.get('tamanho')
        # Simulação de processamento; aqui poderia salvar o pedido
    return render_template_string(HTML_COMPRAR, produto=produto, cep=cep)

@app.route('/buscar')
def buscar():
    termo = request.args.get('q','').strip()
    resultados = []
    if termo:
        termo_lower = termo.lower()
        resultados = [p for p in todos_artigos if termo_lower in p['nome'].lower()]
    return render_template_string(HTML_BUSCAR, resultados=resultados, termo=termo)

@app.route('/cadastro')
def cadastro():
    return render_template_string(HTML_CADASTRO)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    # Simulação simples de login
    flash(f'Login simulado para o usuário: {email}')
    return redirect(url_for('cadastro'))

@app.route('/registro', methods=['POST'])
def registro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    # Simulação simples de registro
    flash(f'Cadastro simulado para {nome} ({email})')
    return redirect(url_for('cadastro'))

@app.route('/logo_grmnstore')
def logo_img():
    # Retorna um placeholder - substitua por seu arquivo real de logo
    return "Imagem logo placeholder"

if __name__ == '__main__':
    app.run(debug=True)
 