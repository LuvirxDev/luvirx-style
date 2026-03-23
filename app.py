from flask import Flask, render_template_string, request, jsonify, url_for

app = Flask(__name__)

# --- CONFIGURACIÓN ESTRATÉGICA LUVIRX STYLE ---
WSP_OFFICIAL = "573115221592"
ADMIN_PIN_ACCESS = "2102"

# DATABASE VOLÁTIL DE ALTA DISPONIBILIDAD
storage = {
    "pedidos": [],
    "disenos_personalizados": [],
    "quejas_reclamos": [],
    "analytics": {"vistas": 0, "interacciones_wsp": 0}
}

# ESTRUCTURA DE PRODUCTOS (ARREGLO MASIVO PARA ROBUSTEZ)
CATALOGO_LUVIRX = {
    "conjuntos": [
        {"id": "C1", "nombre": "Conjunto Onyx Urban", "precio": 185000, "desc": "Seda y Algodón"},
        {"id": "C2", "nombre": "Conjunto Marble White", "precio": 210000, "desc": "Edición Limitada"}
    ],
    "jeans": [
        {"id": "J1", "nombre": "Jean Heritage Slim", "precio": 145000, "desc": "Denim Japonés"},
        {"id": "J2", "nombre": "Jean Street Baggy", "precio": 130000, "desc": "Corte Oversize"}
    ],
    "camisas": [
        {"id": "CM1", "nombre": "Camisa Oxford Luvirx", "precio": 95000, "desc": "100% Algodón Pima"},
        {"id": "CM2", "nombre": "Camisa Versailles Print", "precio": 115000, "desc": "Estampado Digital"}
    ],
    "blusas": [
        {"id": "B1", "nombre": "Blusa Silk Radiance", "precio": 85000, "desc": "Seda Natural"},
        {"id": "B2", "nombre": "Blusa Velvet Night", "precio": 90000, "desc": "Terciopelo Premium"}
    ],
    "faldas": [
        {"id": "F1", "nombre": "Falda Midi Plisada", "precio": 75000, "desc": "Efecto Satinado"},
        {"id": "F2", "nombre": "Minifalda Leather Luxe", "precio": 95000, "desc": "Cuero Vegano"}
    ],
    "deportiva": [
        {"id": "D1", "nombre": "Leggings Pro-Performance", "precio": 110000, "desc": "Tecnología Dry-Fit"},
        {"id": "D2", "nombre": "Top Impact Studio", "precio": 65000, "desc": "Soporte Alta Intensidad"}
    ]
}

HTML_TEMPLATE_ULTIMATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style | Luxury Design & 3D Fashion Platform</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Poppins:wght@100;300;400;600;800&family=Montserrat:wght@200;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --gold: #d4af37;
            --gold-bright: #ffdf00;
            --black: #000000;
            --deep-gray: #050505;
            --soft-gray: #121212;
            --white: #ffffff;
            --error: #ff3333;
            --success: #25d366;
            --accent: #1a1a1a;
        }

        /* RESET PROFESIONAL */
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; outline: none; }
        body { background-color: var(--black); color: var(--white); overflow-x: hidden; scroll-behavior: smooth; }

        /* HEADER & LOGO ENGINE */
        .top-nav {
            background: rgba(0,0,0,0.95);
            padding: 1.5rem 8%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--gold);
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 10000;
            backdrop-filter: blur(15px);
        }
        .nav-logo-area { display: flex; align-items: center; text-decoration: none; gap: 20px; }
        .nav-logo-img { height: 90px; width: auto; object-fit: contain; transition: transform 0.5s ease; filter: drop-shadow(0 0 10px rgba(212,175,55,0.2)); }
        .nav-logo-img:hover { transform: scale(1.1) rotate(-2deg); }
        .nav-brand-text { font-family: 'Playfair Display'; font-size: 3rem; color: var(--gold); letter-spacing: 12px; text-transform: uppercase; font-weight: 900; }

        /* WHATSAPP FLOAT BUTTON */
        .wsp-anchor {
            position: fixed;
            bottom: 40px;
            right: 40px;
            background: var(--success);
            color: #fff;
            padding: 20px 35px;
            border-radius: 60px;
            text-decoration: none;
            font-weight: 800;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 15px;
            z-index: 9999;
            box-shadow: 0 15px 45px rgba(0,0,0,0.7);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .wsp-anchor:hover { transform: translateY(-10px) scale(1.05); box-shadow: 0 25px 60px rgba(37,211,102,0.4); }

        /* MENU DE CATEGORIAS DINAMICO */
        .category-scroller {
            background: var(--soft-gray);
            padding: 20px 0;
            margin-top: 130px;
            border-bottom: 1px solid var(--accent);
            position: sticky;
            top: 130px;
            z-index: 9998;
            overflow-x: auto;
            white-space: nowrap;
            text-align: center;
        }
        .category-scroller a {
            color: #666;
            text-decoration: none;
            margin: 0 25px;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 4px;
            font-weight: 600;
            transition: 0.3s ease;
        }
        .category-scroller a:hover { color: var(--gold); }
        .category-scroller a.special { color: var(--gold); border: 1px solid var(--gold); padding: 5px 15px; border-radius: 5px; }

        /* HERO SECTION */
        .lux-hero {
            height: 70vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('https://images.unsplash.com/photo-1539109132304-39277013f2f0?q=80&w=2000');
            background-size: cover;
            background-attachment: fixed;
            border-bottom: 5px solid var(--gold);
        }
        .lux-hero h1 { font-family: 'Playfair Display'; font-size: 6rem; letter-spacing: 20px; color: var(--gold); margin-bottom: 20px; text-shadow: 0 10px 30px rgba(0,0,0,1); }
        .lux-hero p { letter-spacing: 8px; font-weight: 200; color: #aaa; text-transform: uppercase; }

        /* GRID SYSTEM & CARDS */
        .main-container { padding: 80px 8%; }
        .section-heading { font-family: 'Playfair Display'; font-size: 4rem; color: var(--gold); text-align: center; margin: 120px 0 80px; text-transform: uppercase; letter-spacing: 15px; }
        .section-heading span { display: block; font-family: 'Poppins'; font-size: 1rem; color: #444; letter-spacing: 6px; margin-top: 15px; }

        .fashion-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 60px; }
        .fashion-card { background: var(--deep-gray); border-radius: 40px; border: 1px solid var(--accent); overflow: hidden; transition: 0.7s cubic-bezier(0.19, 1, 0.22, 1); position: relative; }
        .fashion-card:hover { transform: translateY(-30px); border-color: var(--gold); box-shadow: 0 50px 100px rgba(0,0,0,0.8); }
        .card-image-box { height: 550px; background: #010101; display: flex; align-items: center; justify-content: center; color: #080808; font-size: 5rem; font-weight: 900; letter-spacing: 30px; position: relative; }
        .card-image-box::after { content: 'LUVIRX'; }
        
        .card-body { padding: 45px; text-align: center; }
        .card-body h3 { font-size: 1.8rem; letter-spacing: 3px; margin-bottom: 10px; font-weight: 300; color: var(--white); }
        .card-body p { color: #555; margin-bottom: 25px; font-size: 0.9rem; }
        .item-price { color: var(--gold); font-size: 2.5rem; font-weight: 800; display: block; margin-bottom: 35px; }
        
        .action-btn { background: transparent; border: 2px solid var(--gold); color: var(--gold); padding: 22px 45px; width: 100%; border-radius: 20px; cursor: pointer; text-transform: uppercase; font-weight: 800; letter-spacing: 5px; transition: 0.5s; font-size: 1.1rem; }
        .action-btn:hover { background: var(--gold); color: #000; box-shadow: 0 0 40px var(--gold); letter-spacing: 8px; }

        /* 3D DESIGN STUDIO AREA */
        .studio-3d-wrap { background: linear-gradient(145deg, #0a0a0a, #000); border: 1px solid var(--gold); border-radius: 60px; padding: 120px 10%; margin: 150px 0; position: relative; overflow: hidden; }
        .studio-3d-wrap::before { content: '3D'; position: absolute; right: -50px; top: -50px; font-size: 30rem; font-weight: 900; color: rgba(212,175,55,0.02); pointer-events: none; }
        .studio-3d-wrap h2 { font-family: 'Playfair Display'; font-size: 5rem; color: var(--gold); margin-bottom: 30px; text-transform: uppercase; }
        .studio-textarea { width: 100%; padding: 40px; background: #000; border: 2px solid #222; color: #fff; border-radius: 35px; min-height: 350px; font-size: 1.3rem; margin: 50px 0; border-left: 8px solid var(--gold); transition: 0.4s; }
        .studio-textarea:focus { border-color: var(--gold); box-shadow: 0 0 30px rgba(212,175,55,0.1); }

        /* QUEJAS Y RECLAMOS DE ALTA PRIORIDAD */
        .claim-engine { max-width: 1000px; margin: 150px auto; padding: 100px; background: #050505; border-radius: 50px; border-top: 6px solid var(--error); text-align: center; box-shadow: 0 40px 120px rgba(0,0,0,0.6); }
        .claim-engine h2 { font-family: 'Playfair Display'; color: var(--error); font-size: 3.5rem; margin-bottom: 40px; letter-spacing: 5px; }
        .claim-input-group { margin-bottom: 35px; text-align: left; }
        .claim-input-group label { color: #444; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; margin-bottom: 15px; display: block; }
        .lux-input-field { width: 100%; padding: 25px; background: #000; border: 1px solid #1a1a1a; color: #fff; border-radius: 15px; font-size: 1.1rem; transition: 0.3s; }
        .lux-input-field:focus { border-color: var(--error); }

        /* ADMIN CONTROL CENTER */
        #luv-admin-vault { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #fff; color: #000; z-index: 100000; padding: 100px; overflow-y: auto; }
        .vault-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 5px solid #000; padding-bottom: 30px; margin-bottom: 50px; }
        .vault-table { width: 100%; border-collapse: collapse; margin-top: 40px; }
        .vault-table th, .vault-table td { border: 1px solid #eee; padding: 30px; text-align: left; }
        .vault-table th { background: #fbfbfb; font-weight: 800; text-transform: uppercase; font-size: 0.8rem; color: #999; }
        .close-vault { background: #000; color: #fff; padding: 20px 50px; border: none; border-radius: 10px; cursor: pointer; font-weight: 800; }
    </style>
</head>
<body>

    <a href="https://wa.me/{{ wsp }}" class="wsp-anchor" target="_blank">
        LUVIRX STYLE VIP | SOPORTE 💬
    </a>

    <header class="top-nav">
        <a href="/" class="nav-logo-area">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo Luvirx" class="nav-logo-img" onerror="this.src='https://via.placeholder.com/200x200/000000/d4af37?text=LUVIRX';">
            <span class="nav-brand-text">LUVIRX</span>
        </a>
        <div style="display:flex; gap:30px; align-items:center;">
            <button onclick="toggleCart()" style="background:none; border:2px solid var(--gold); color:var(--gold); padding:18px 40px; border-radius:20px; font-weight:800; cursor:pointer; letter-spacing:3px;">
                MI BOLSA [<span id="cart-counter">0</span>]
            </button>
        </div>
    </header>

    <nav class="category-scroller">
        <a href="#conjuntos">Conjuntos</a>
        <a href="#jeans">Jeans</a>
        <a href="#camisas">Camisas</a>
        <a href="#blusas">Blusas</a>
        <a href="#faldas">Faldas</a>
        <a href="#deportiva">Ropa Deportiva</a>
        <a href="#design-studio" class="special">Estudio 3D & Custom</a>
        <a href="#claim-center" style="color:var(--error);">Reclamos</a>
    </nav>

    <div class="lux-hero">
        <p>Innovation in Urban Fashion</p>
        <h1>LUVIRX STYLE</h1>
        <p>COLLECTION 2026 | BOGOTÁ - NEW YORK</p>
    </div>

    <div class="main-container">
        
        <section id="design-studio" class="studio-3d-wrap">
            <h2>Estudio de Diseño Custom 3D</h2>
            <p style="color:#555; letter-spacing:4px; font-weight:200;">CREA UNA PIEZA ÚNICA. NUESTRO SISTEMA PROCESARÁ TU IDEA Y NUESTROS SASTRES LA HARÁN REALIDAD.</p>
            <textarea id="idea-box" class="studio-textarea" placeholder="Describe tu visión: Materiales, colores, texturas, formas asimétricas, detalles en 3D..."></textarea>
            <button class="action-btn" onclick="submitDesignIdea()" style="background:var(--gold); color:#000;">Iniciar Prototipo de Diseño</button>
        </section>

        {% for cat_id, items in catalogo.items() %}
        <h2 id="{{ cat_id }}" class="section-heading">{{ cat_id.capitalize() }}<span>Exclusive Luvirx Selection</span></h2>
        <div class="fashion-grid">
            {% for p in items %}
            <div class="fashion-card">
                <div class="card-image-box"></div>
                <div class="card-body">
                    <h3>{{ p.nombre }}</h3>
                    <p>{{ p.desc }}</p>
                    <span class="item-price">${{ "{:,}".format(p.precio) }}</span>
                    <button class="action-btn" onclick="addToBolsa('{{ p.nombre }}', {{ p.precio }})">Añadir a Bolsa</button>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endfor %}

        <h2 class="section-heading">Galería Conceptual 3D<span>Futurismo Textil</span></h2>
        <div class="fashion-grid">
            <div class="fashion-card" style="border-style:dashed; opacity:0.6;">
                <div class="card-body">
                    <h4 style="color:var(--gold); font-size:1.5rem; margin-bottom:20px;">PROYECTO: NEON-MANTLE</h4>
                    <p>Integración de fibra óptica en tejidos de lino para visibilidad urbana.</p>
                </div>
            </div>
            <div class="fashion-card" style="border-style:dashed; opacity:0.6;">
                <div class="card-body">
                    <h4 style="color:var(--gold); font-size:1.5rem; margin-bottom:20px;">PROYECTO: BIOMIMIC ARMOR</h4>
                    <p>Estructuras impresas en 3D que imitan la flexibilidad de la piel orgánica.</p>
                </div>
            </div>
        </div>

        <section id="claim-center" class="claim-engine">
            <h2>Atención al Cliente: Reclamos</h2>
            <p style="color:#444; margin-bottom:60px; letter-spacing:2px;">CUALQUIER INCONVENIENTE SERÁ TRATADO CON PRIORIDAD ABSOLUTA POR NUESTRO EQUIPO GERENCIAL.</p>
            <div class="claim-input-group">
                <label>Nombre Completo del Cliente</label>
                <input type="text" id="claim-user" class="lux-input-field">
            </div>
            <div class="claim-input-group">
                <label>Canal de Contacto (Celular o Correo)</label>
                <input type="text" id="claim-contact" class="lux-input-field">
            </div>
            <div class="claim-input-group">
                <label>Detalle Exhaustivo del Reclamo</label>
                <textarea id="claim-body" class="lux-input-field" style="min-height:200px;"></textarea>
            </div>
            <button class="action-btn" style="border-color:var(--error); color:var(--error);" onclick="submitClaim()">Radicar Reclamo Oficial</button>
        </section>

    </div>

    <div id="luv-admin-vault">
        <div class="vault-header">
            <h1 style="letter-spacing:15px; font-family:'Playfair Display'; font-size:3rem;">MASTER LOGISTICS CONTROL</h1>
            <button onclick="closeVault()" class="close-vault">SALIR DEL SISTEMA</button>
        </div>
        <div id="vault-content"></div>
    </div>

    <footer style="padding:150px 8%; text-align:center; border-top:1px solid var(--accent); background:#020202;" onclick="openVault()">
        <p style="opacity:0.1; letter-spacing:10px; font-weight:800; cursor:pointer;">&copy; 2026 LUVIRX STYLE | LUXURY GROUP HOLDING</p>
    </footer>

    <script>
        let bolsaItems = []; let bolsaTotal = 0;
        function addToBolsa(n, p) { bolsaItems.push(n); bolsaTotal += p; document.getElementById('cart-counter').innerText = bolsaItems.length; }

        async function toggleCart() {
            if(bolsaItems.length === 0) return alert("Tu bolsa está vacía actualmente.");
            const nom = prompt("Nombre completo para el despacho:");
            const dir = prompt("Dirección de entrega exacta:");
            if(!nom || !dir) return;
            const pedidoData = { cliente: nom, direccion: dir, articulos: bolsaItems.join(", "), total: bolsaTotal };
            await fetch('/api/internal/order', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(pedidoData) });
            window.open(`https://wa.me/{{ wsp }}?text=LUVIRX STYLE - NUEVO PEDIDO%0ACliente: ${nom}%0AItems: ${pedidoData.articulos}%0ATotal: $${bolsaTotal}`);
            location.reload();
        }

        async function submitDesignIdea() {
            const idea = document.getElementById('idea-box').value;
            if(!idea) return alert("Por favor, describe tu visión de diseño.");
            await fetch('/api/internal/design', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ idea: idea }) });
            window.open(`https://wa.me/{{ wsp }}?text=LUVIRX STYLE - DISEÑO 3D CUSTOM%0ADescripción: ${idea}`);
            alert("Propuesta enviada al equipo de diseño.");
            location.reload();
        }

        async function submitClaim() {
            const nom = document.getElementById('claim-user').value;
            const con = document.getElementById('claim-contact').value;
            const msg = document.getElementById('claim-body').value;
            if(!nom || !msg) return alert("Faltan datos críticos para radicar el reclamo.");
            const claimData = { nombre: nom, contacto: con, mensaje: msg };
            await fetch('/api/internal/claim', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(claimData) });
            window.open(`https://wa.me/{{ wsp }}?text=URGENTE - RECLAMO LUVIRX STYLE%0ACliente: ${nom}%0AMensaje: ${msg}`);
            alert("Reclamo radicado bajo supervisión gerencial.");
            location.reload();
        }

        function openVault() {
            if(prompt("CÓDIGO DE ENCRIPTACIÓN DE ACCESO:") === "{{ pin }}") {
                document.getElementById('luv-admin-vault').style.display = 'block';
                renderVaultData();
            }
        }
        function closeVault() { document.getElementById('luv-admin-vault').style.display = 'none'; }

        async function renderVaultData() {
            const res = await fetch('/api/internal/data'); const d = await res.json();
            let html = '<h2>Órdenes de Venta</h2><table class="vault-table"><tr><th>Cliente</th><th>Productos</th><th>Total</th></tr>';
            d.pedidos.forEach(p => html += `<tr><td>${p.cliente}</td><td>${p.articulos}</td><td>$${p.total}</td></tr>`);
            html += '</table><h2>Buzón de Diseños Personalizados</h2><table class="vault-table"><tr><th>Propuesta de Diseño</th></tr>';
            d.disenos_personalizados.forEach(dp => html += `<tr><td>${dp.idea}</td></tr>`);
            html += '</table><h2 style="color:red;">Reportes de Reclamación</h2><table class="vault-table"><tr><th>Cliente</th><th>Detalle del Reclamo</th></tr>';
            d.quejas_reclamos.forEach(q => html += `<tr><td>${q.nombre} (${q.contacto})</td><td>${q.mensaje}</td></tr>`);
            document.getElementById('vault-content').innerHTML = html + '</table>';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def luvirx_main():
    return render_template_string(HTML_TEMPLATE_ULTIMATE, 
                                  catalogo=CATALOGO_LUVIRX, 
                                  wsp=WSP_OFFICIAL, 
                                  pin=ADMIN_PIN_ACCESS)

@app.route('/api/internal/order', methods=['POST'])
def handle_order(): storage["pedidos"].append(request.json); return jsonify({"status": "stored"})

@app.route('/api/internal/design', methods=['POST'])
def handle_design(): storage["disenos_personalizados"].append(request.json); return jsonify({"status": "stored"})

@app.route('/api/internal/claim', methods=['POST'])
def handle_claim(): storage["quejas_reclamos"].append(request.json); return jsonify({"status": "stored"})

@app.route('/api/internal/data')
def get_vault_data(): return jsonify(storage)

if __name__ == '__main__':
    app.run(debug=True)