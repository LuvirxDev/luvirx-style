from flask import Flask, render_template_string, request, jsonify, url_for

app = Flask(__name__)

# --- BASE DE DATOS TEMPORAL ---
WSP = "573115221592"
PIN_ADMIN = "2102"
pedidos = []
disenos_personalizados = []

HTML_MASTER = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style | Luxury Studio</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --oro: #d4af37; --negro: #000; --gris: #0a0a0a; --blanco: #fff; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background: var(--negro); color: var(--blanco); scroll-behavior: smooth; }
        
        /* HEADER Y LOGO */
        nav { background: #000; padding: 1.5rem 8%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--oro); position: sticky; top: 0; z-index: 1000; }
        .logo-container { display: flex; align-items: center; text-decoration: none; }
        .logo-img { height: 60px; margin-right: 15px; border-radius: 5px; }
        .logo-txt { font-family: 'Playfair Display'; color: var(--oro); font-size: 2rem; letter-spacing: 5px; }

        /* SECCIONES DE NAVEGACIÓN */
        .categorias-bar { background: var(--gris); padding: 15px; text-align: center; border-bottom: 1px solid #222; overflow-x: auto; white-space: nowrap; }
        .categorias-bar a { color: #888; text-decoration: none; margin: 0 20px; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; transition: 0.3s; }
        .categorias-bar a:hover { color: var(--oro); }

        /* HAZ TU PROPIO DISEÑO - IMPACTO */
        .diseno-seccion { 
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1558769132-cb1aea458c5e?q=80&w=1600');
            background-size: cover; padding: 100px 8%; text-align: center; border-bottom: 1px solid var(--oro);
        }
        .diseno-seccion h2 { font-family: 'Playfair Display'; font-size: 3.5rem; color: var(--oro); margin-bottom: 20px; }
        .diseno-box { max-width: 800px; margin: 0 auto; background: rgba(10,10,10,0.9); padding: 40px; border-radius: 20px; border: 1px solid #333; }
        textarea { width: 100%; padding: 20px; background: #000; border: 1px solid var(--oro); color: #fff; border-radius: 10px; min-height: 150px; margin-bottom: 20px; font-size: 1rem; }

        /* APARTADOS DE MODA */
        .contenedor { padding: 60px 8%; }
        .titulo-apartado { font-family: 'Playfair Display'; font-size: 2.5rem; color: var(--oro); margin-bottom: 40px; border-left: 5px solid var(--oro); padding-left: 20px; text-transform: uppercase; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; margin-bottom: 100px; }
        .producto-card { background: var(--gris); border-radius: 20px; overflow: hidden; border: 1px solid #222; transition: 0.4s; }
        .producto-card:hover { border-color: var(--oro); transform: scale(1.02); }
        .foto-vacia { height: 400px; background: #050505; display: flex; align-items: center; justify-content: center; color: #1a1a1a; font-size: 2rem; font-weight: 700; letter-spacing: 10px; }
        
        .btn-lujo { background: var(--oro); color: #000; border: none; padding: 18px; width: 100%; font-weight: 700; border-radius: 10px; cursor: pointer; text-transform: uppercase; letter-spacing: 2px; font-size: 1rem; }

        /* PANEL ADMIN */
        #admin-panel { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #fff; color: #000; z-index: 2000; padding: 50px; overflow-y: auto; }
        .btn-cerrar { background: red; color: white; padding: 10px; cursor: pointer; border: none; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 15px; text-align: left; }
    </style>
</head>
<body>

    <nav>
        <a href="/" class="logo-container">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Luvirx Logo" class="logo-img">
            <span class="logo-txt">LUVIRX</span>
        </a>
        <button onclick="abrirBolsa()" style="background:none; border:1px solid var(--oro); color:var(--oro); padding:10px 25px; border-radius:10px; cursor:pointer; font-weight:600;">MI BOLSA (<span id="cart-count">0</span>)</button>
    </nav>

    <div class="categorias-bar">
        <a href="#estudio">Haz tu diseño</a>
        <a href="#conjuntos">Conjuntos</a>
        <a href="#jeans">Jeans</a>
        <a href="#camisas">Camisas</a>
        <a href="#blusas">Blusas</a>
        <a href="#faldas">Faldas</a>
        <a href="#deportiva">Deportiva</a>
    </div>

    <section id="estudio" class="diseno-seccion">
        <h2>Haz tu propio diseño</h2>
        <div class="diseno-box">
            <p style="color:#ccc; margin-bottom:20px;">Describe tu prenda soñada. Formas, colores y materiales. Nosotros la fabricamos.</p>
            <textarea id="idea-text" placeholder="Escribe aquí tu diseño personalizado..."></textarea>
            <button class="btn-lujo" onclick="enviarDiseno()">Enviar a Cotización</button>
        </div>
    </section>

    <div class="contenedor">
        <h2 id="conjuntos" class="titulo-apartado">Conjuntos Premium</h2>
        <div class="grid">
            <div class="producto-card">
                <div class="foto-vacia">LUVIRX</div>
                <div class="p-4" style="padding:25px; text-align:center;">
                    <h3>Conjunto Urban Gold</h3>
                    <span style="color:var(--oro); font-size:1.8rem; font-weight:700; display:block; margin:15px 0;">$180.000</span>
                    <button class="btn-lujo" onclick="add('Conjunto Urban Gold', 180000)">Añadir</button>
                </div>
            </div>
        </div>

        <h2 id="jeans" class="titulo-apartado">Jeans & Faldas</h2>
        <div class="grid">
            <div class="producto-card">
                <div class="foto-vacia">LUVIRX</div>
                <div class="p-4" style="padding:25px; text-align:center;">
                    <h3>Jean Heritage Slim</h3>
                    <span style="color:var(--oro); font-size:1.8rem; font-weight:700; display:block; margin:15px 0;">$125.000</span>
                    <button class="btn-lujo" onclick="add('Jean Heritage', 125000)">Añadir</button>
                </div>
            </div>
        </div>

        <h2 id="deportiva" class="titulo-apartado">Ropa Deportiva</h2>
        <div class="grid">
            <div class="producto-card">
                <div class="foto-vacia">LUVIRX</div>
                <div class="p-4" style="padding:25px; text-align:center;">
                    <h3>Conjunto Gym Pro</h3>
                    <span style="color:var(--oro); font-size:1.8rem; font-weight:700; display:block; margin:15px 0;">$95.000</span>
                    <button class="btn-lujo" onclick="add('Conjunto Gym', 95000)">Añadir</button>
                </div>
            </div>
        </div>
    </div>

    <div id="admin-panel">
        <button class="btn-cerrar" onclick="document.getElementById('admin-panel').style.display='none'">CERRAR PANEL</button>
        <h1>Panel de Control Luvirx Style</h1>
        <div id="data-content"></div>
    </div>

    <footer style="padding:60px; text-align:center; border-top:1px solid #111;" onclick="checkAdmin()">
        <p style="opacity:0.2;">Luvirx Style &copy; 2026 | Sistema de Gestión</p>
    </footer>

    <script>
        let bolsa = []; let total = 0;
        function add(n, p) { bolsa.push(n); total += p; document.getElementById('cart-count').innerText = bolsa.length; alert("✓ Producto añadido."); }
        
        async function enviarDiseno() {
            const idea = document.getElementById('idea-text').value;
            if(!idea) return alert("Describe tu idea primero.");
            await fetch('/api/diseno', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ idea: idea }) });
            window.open(`https://wa.me/{{ wsp }}?text=Hola Luvirx! Quiero cotizar este diseño: ${idea}`);
            location.reload();
        }

        async function abrirBolsa() {
            if(bolsa.length == 0) return alert("Tu bolsa está vacía.");
            const n = prompt("Tu Nombre:"); const d = prompt("Dirección:");
            if(!n || !d) return alert("Datos necesarios para el pedido.");
            const p = { nombre: n, dir: d, items: bolsa.join(", "), total: total };
            await fetch('/api/pedido', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(p) });
            window.open(`https://wa.me/{{ wsp }}?text=Nuevo Pedido: ${p.items}. Total: $${total}. Cliente: ${n}`);
            location.reload();
        }

        function checkAdmin() {
            if(prompt("PIN ADMIN:") === "{{ pin }}") {
                document.getElementById('admin-panel').style.display = 'block';
                fetchData();
            }
        }

        async function fetchData() {
            const res = await fetch('/api/lista'); const data = await res.json();
            let html = '<h3>Pedidos Recientes</h3><table><tr><th>Cliente</th><th>Productos</th><th>Total</th></tr>';
            data.pedidos.forEach(p => html += `<tr><td>${p.nombre}</td><td>${p.items}</td><td>$${p.total}</td></tr>`);
            html += '</table><h3 style="margin-top:30px;">Diseños Personalizados</h3><table><tr><th>Idea de Diseño</th></tr>';
            data.disenos.forEach(d => html += `<tr><td>${d.idea}</td></tr>`);
            document.getElementById('data-content').innerHTML = html + '</table>';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_MASTER, wsp=WSP, pin=PIN_ADMIN)

@app.route('/api/pedido', methods=['POST'])
def pedido(): pedidos.append(request.json); return jsonify({"ok": True})

@app.route('/api/diseno', methods=['POST'])
def diseno(): disenos_personalizados.append(request.json); return jsonify({"ok": True})

@app.route('/api/lista')
def lista(): return jsonify({"pedidos": pedidos, "disenos": disenos_personalizados})

if __name__ == '__main__':
    app.run(debug=True)