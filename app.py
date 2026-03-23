from flask import Flask, render_template_string, request, jsonify, url_for

app = Flask(__name__)

# --- CONFIGURACIÓN DE ALTO NIVEL ---
WSP = "573115221592"
PIN_ACCESO = "2102"
pedidos_db = []
diseños_db = []

HTML_FINAL = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style | Luxury Urban Studio</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --oro: #d4af37; --negro: #000; --gris: #0a0a0a; --blanco: #fff; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background: var(--negro); color: var(--blanco); scroll-behavior: smooth; }
        
        /* NAVEGACIÓN Y LOGO */
        nav { background: #000; padding: 1rem 8%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--oro); position: sticky; top: 0; z-index: 1000; }
        .logo-box { display: flex; align-items: center; text-decoration: none; }
        .logo-img { height: 50px; margin-right: 15px; }
        .logo-txt { font-family: 'Playfair Display'; color: var(--oro); font-size: 1.8rem; letter-spacing: 4px; }

        .btn-wsp { position: fixed; bottom: 25px; right: 25px; background: #25d366; color: #fff; padding: 15px 25px; border-radius: 50px; text-decoration: none; font-weight: 600; z-index: 1000; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }

        /* SECCIONES DE MODA */
        .menu-cat { background: var(--gris); padding: 15px; text-align: center; border-bottom: 1px solid #111; overflow-x: auto; white-space: nowrap; }
        .menu-cat a { color: #666; text-decoration: none; margin: 0 15px; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; }
        .menu-cat a:hover { color: var(--oro); }

        .contenedor { padding: 40px 8%; }
        .seccion-titulo { font-family: 'Playfair Display'; font-size: 2.2rem; color: var(--oro); text-align: center; margin: 60px 0 40px; text-transform: uppercase; }
        
        /* GRID DE PRODUCTOS VACÍOS */
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
        .card { background: var(--gris); border-radius: 15px; overflow: hidden; border: 1px solid #111; transition: 0.3s; text-align: center; }
        .card:hover { border-color: var(--oro); transform: translateY(-5px); }
        .img-vacia { height: 350px; background: #050505; display: flex; align-items: center; justify-content: center; color: #222; font-size: 0.8rem; letter-spacing: 5px; }
        .info { padding: 20px; }
        .precio { color: var(--oro); font-size: 1.5rem; font-weight: 700; margin: 10px 0; display: block; }
        .btn-lujo { background: var(--oro); color: #000; border: none; padding: 12px; width: 100%; font-weight: 700; border-radius: 8px; cursor: pointer; text-transform: uppercase; }

        /* STUDIO: HAZ TU PROPIO DISEÑO */
        .studio { background: #0a0a0a; padding: 60px; border: 1px solid var(--oro); border-radius: 25px; margin: 40px 0; text-align: center; }
        textarea { width: 100%; padding: 20px; background: #000; border: 1px solid #222; color: #fff; border-radius: 10px; margin: 20px 0; min-height: 120px; }

        /* PANEL ADMIN */
        #panel-admin { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #fff; color: #000; z-index: 2000; padding: 40px; overflow-y: auto; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
    </style>
</head>
<body>

    <a href="https://wa.me/{{ wsp }}" class="btn-wsp" target="_blank">Soporte VIP 💬</a>

    <nav>
        <a href="/" class="logo-box">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" class="logo-img">
            <span class="logo-txt">LUVIRX</span>
        </a>
        <button onclick="verCarrito()" style="background:none; border:1px solid var(--oro); color:var(--oro); padding:8px 15px; border-radius:5px; cursor:pointer;">BOLSA (<span id="c">0</span>)</button>
    </nav>

    <div class="menu-cat">
        <a href="#conjuntos">Conjuntos</a>
        <a href="#jeans">Jeans</a>
        <a href="#camisas">Camisas</a>
        <a href="#blusas">Blusas</a>
        <a href="#faldas">Faldas</a>
        <a href="#deportiva">Deportiva</a>
        <a href="#diseno" style="color:var(--oro);">Haz tu diseño</a>
    </div>

    <div class="contenedor">
        <div id="diseno" class="studio">
            <h2 style="font-family:'Playfair Display'; color:var(--oro); font-size:2.5rem;">HAZ TU PROPIO DISEÑO</h2>
            <p style="color:#666;">Describe tu idea, texturas y formas. Nosotros la creamos para ti.</p>
            <textarea id="idea" placeholder="Ej: Quiero un conjunto de falda y blusa en seda negra con bordados dorados..."></textarea>
            <button class="btn-lujo" onclick="enviarDiseno()">Cotizar mi idea</button>
        </div>

        <h2 id="conjuntos" class="seccion-titulo">Conjuntos</h2>
        <div class="grid"><div class="card"><div class="img-vacia">LUVI-SPACE</div><div class="info"><h3>Conjunto Premium</h3><span class="precio">$180.000</span><button class="btn-lujo" onclick="add('Conjunto', 180000)">Añadir</button></div></div></div>

        <h2 id="jeans" class="seccion-titulo">Jeans</h2>
        <div class="grid"><div class="card"><div class="img-vacia">LUVI-SPACE</div><div class="info"><h3>Jeans Urban</h3><span class="precio">$125.000</span><button class="btn-lujo" onclick="add('Jeans', 125000)">Añadir</button></div></div></div>

        <h2 id="blusas" class="seccion-titulo">Blusas & Camisas</h2>
        <div class="grid"><div class="card"><div class="img-vacia">LUVI-SPACE</div><div class="info"><h3>Top Luxury</h3><span class="precio">$85.000</span><button class="btn-lujo" onclick="add('Top', 85000)">Añadir</button></div></div></div>

        <h2 id="deportiva" class="seccion-titulo">Ropa Deportiva</h2>
        <div class="grid"><div class="card"><div class="img-vacia">LUVI-SPACE</div><div class="info"><h3>Licra Pro</h3><span class="precio">$95.000</span><button class="btn-lujo" onclick="add('Licra', 95000)">Añadir</button></div></div></div>
    </div>

    <div id="panel-admin">
        <button onclick="document.getElementById('panel-admin').style.display='none'">CERRAR PANEL</button>
        <h2>HISTORIAL DE VENTAS Y DISEÑOS</h2>
        <div id="tabla-pedidos"></div>
    </div>

    <footer style="text-align:center; padding:40px; opacity:0.3;" onclick="loginAdmin()">Luvirx Style Admin</footer>

    <script>
        let bolsa = []; let total = 0;
        function add(n, p) { bolsa.push(n); total += p; document.getElementById('c').innerText = bolsa.length; alert("Añadido."); }
        
        async function enviarDiseno() {
            const txt = document.getElementById('idea').value;
            if(!txt) return alert("Describe tu diseño");
            await fetch('/api/diseno', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ idea: txt }) });
            window.open(`https://wa.me/{{ wsp }}?text=Quiero cotizar mi propio diseño: ${txt}`);
            location.reload();
        }

        async function verCarrito() {
            if(bolsa.length == 0) return;
            const nom = prompt("Nombre:"); const dir = prompt("Dirección:");
            if(!nom || !dir) return;
            const ped = { nombre: nom, dir: dir, items: bolsa.join(", "), total: total };
            await fetch('/api/pedido', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(ped) });
            window.open(`https://wa.me/{{ wsp }}?text=Nuevo Pedido: ${ped.items}. Total: $${total}`);
            location.reload();
        }

        function loginAdmin() {
            if(prompt("PIN:") == "{{ pin }}") {
                document.getElementById('panel-admin').style.display = 'block';
                cargarDatos();
            }
        }

        async function cargarDatos() {
            const res = await fetch('/api/lista'); const data = await res.json();
            let h = '<table><tr><th>Cliente</th><th>Productos / Ideas</th><th>Total</th></tr>';
            data.pedidos.forEach(p => h += `<tr><td>${p.nombre}</td><td>${p.items}</td><td>$${p.total}</td></tr>`);
            data.disenos.forEach(d => h += `<tr><td>DISEÑO PROPIO</td><td>${d.idea}</td><td>COTIZAR</td></tr>`);
            document.getElementById('tabla-pedidos').innerHTML = h + '</table>';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_FINAL, wsp=WSP, pin=PIN_ACCESO)

@app.route('/api/pedido', methods=['POST'])
def pedido(): pedidos_db.append(request.json); return jsonify({"ok": True})

@app.route('/api/diseno', methods=['POST'])
def diseno(): diseños_db.append(request.json); return jsonify({"ok": True})

@app.route('/api/lista')
def lista(): return jsonify({"pedidos": pedidos_db, "disenos": diseños_db})

if __name__ == '__main__':
    app.run(debug=True)