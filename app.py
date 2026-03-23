from flask import Flask, render_template_string, request, jsonify, url_for

app = Flask(__name__)

# --- CONFIGURACIÓN DE ALTO NIVEL ---
WSP = "573115221592"
PIN_ADMIN = "2102"
pedidos_db = []
diseños_db = []
quejas_db = []

HTML_PROFESIONAL = """
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
        body { background: var(--negro); color: var(--blanco); scroll-behavior: smooth; overflow-x: hidden; }
        
        /* HEADER Y LOGO RESTAURADO */
        nav { 
            background: #000; padding: 1.5rem 8%; 
            display: flex; justify-content: space-between; align-items: center; 
            border-bottom: 1px solid var(--oro); position: sticky; top: 0; z-index: 1000; 
        }
        .logo-box { display: flex; align-items: center; text-decoration: none; justify-content: center; width: 100%; }
        .logo-img { height: 60px; width: auto; object-fit: contain; margin-right: 20px; border-radius: 8px; }
        .logo-txt { font-family: 'Playfair Display'; color: var(--oro); font-size: 2.2rem; letter-spacing: 5px; text-transform: uppercase; }

        /* BOTÓN WHATSAPP INTACTO */
        .btn-wsp { position: fixed; bottom: 25px; right: 25px; background: #25d366; color: #fff; padding: 15px 25px; border-radius: 50px; text-decoration: none; font-weight: 600; z-index: 1000; box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: flex; align-items: center; gap: 10px; transition: 0.3s; }
        .btn-wsp:hover { transform: scale(1.1); background: #128c7e; }

        /* MENÚ DE CATEGORÍAS */
        .menu-cat { background: var(--gris); padding: 15px; text-align: center; border-bottom: 1px solid #111; overflow-x: auto; white-space: nowrap; position: sticky; top: 90px; z-index: 999; }
        .cat-link { color: #666; text-decoration: none; margin: 0 15px; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; transition: 0.3s; }
        .cat-link:hover { color: var(--oro); }

        /* HERO SECCIÓN */
        .hero { height: 50vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1558769132-cb1aea458c5e?q=80&w=1600'); background-size: cover; background-position: center; border-bottom: 2px solid var(--oro); }
        .hero h1 { font-family: 'Playfair Display'; font-size: 4rem; color: var(--oro); margin-bottom: 10px; }
        
        /* CONTENEDOR GENERAL */
        .contenedor { padding: 60px 8%; }
        .titulo-seccion { font-family: 'Playfair Display'; font-size: 2.5rem; color: var(--oro); text-align: center; margin: 80px 0 50px; text-transform: uppercase; letter-spacing: 3px; position: relative; }
        .titulo-seccion::after { content: ''; display: block; width: 60px; height: 2px; background: var(--oro); margin: 15px auto 0; }
        
        /* GRID DE PRODUCTOS (IMÁGENES VACÍAS) */
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 35px; }
        .card { background: var(--gris); border-radius: 20px; overflow: hidden; border: 1px solid #111; transition: 0.4s; text-align: center; }
        .card:hover { border-color: var(--oro); transform: translateY(-10px); }
        .img-vacia { height: 380px; background: #050505; display: flex; align-items: center; justify-content: center; color: #1a1a1a; font-size: 2rem; font-weight: 700; letter-spacing: 10px; border-bottom: 1px solid #111; }
        .info { padding: 25px; }
        .precio { color: var(--oro); font-size: 1.6rem; font-weight: 700; margin: 15px 0; display: block; }
        .btn-lujo { background: var(--oro); color: #000; border: none; padding: 15px; width: 100%; font-weight: 700; border-radius: 10px; cursor: pointer; text-transform: uppercase; letter-spacing: 2px; transition: 0.3s; }
        .btn-lujo:hover { background: #fff; transform: scale(1.02); }

        /* STUDIO: HAZ TU PROPIO DISEÑO */
        .studio-box { background: #0a0a0a; padding: 80px 10%; border: 1px solid var(--oro); border-radius: 25px; margin: 60px 0; text-align: center; }
        .studio-box textarea { width: 100%; padding: 20px; background: #000; border: 1px solid #222; color: #fff; border-radius: 12px; min-height: 150px; margin: 25px 0; }

        /* GALERÍA DISEÑOS 3D */
        .grid-3d { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
        .card-3d { background: var(--gris); border-radius: 15px; overflow: hidden; border: 1px solid #111; transition: 0.3s; text-align: center; padding: 30px; }
        .card-3d:hover { border-color: var(--oro); }
        .icon-3d { font-size: 3rem; color: var(--oro); margin-bottom: 20px; display: block; }

        /* QUEJAS Y RECLAMOS */
        .quejas-box { background: #111; padding: 60px 10%; border-radius: 20px; margin-top: 100px; text-align: center; border: 1px solid #222; }
        .form-queja { max-width: 600px; margin: 0 auto; text-align: left; }
        input, textarea { width: 100%; padding: 16px; margin-bottom: 20px; background: #0d0d0d; border: 1px solid #1a1a1a; color: #fff; border-radius: 8px; outline: none; }
        input:focus, textarea:focus { border-color: var(--oro); }

        /* PANEL ADMIN */
        #admin-panel { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #fff; color: #000; z-index: 2000; padding: 50px; overflow-y: auto; }
        .table-admin { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .table-admin th, .table-admin td { border: 1px solid #ddd; padding: 15px; text-align: left; }
    </style>
</head>
<body>

    <a href="https://wa.me/{{ wsp }}" class="btn-wsp" target="_blank">Soporte VIP 💬</a>

    <nav>
        <a href="/" class="logo-box">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Luvirx Logo" class="logo-img">
            <span class="logo-txt">LUVIRX</span>
        </a>
    </nav>

    <div class="menu-cat">
        <a href="#conjuntos" class="cat-link">Conjuntos</a>
        <a href="#jeans" class="cat-link">Jeans</a>
        <a href="#camisas" class="cat-link">Camisas</a>
        <a href="#blusas" class="cat-link">Blusas</a>
        <a href="#faldas" class="cat-link">Faldas</a>
        <a href="#deportiva" class="cat-link">Deportiva</a>
        <a href="#diseno" class="cat-link" style="color:var(--oro);">Hacer mi diseño</a>
        <a href="#galeria3d" class="cat-link">Diseños 3D</a>
        <a href="#quejas" class="cat-link" style="color:red;">Quejas</a>
    </div>

    <div class="hero">
        <p style="letter-spacing:5px; color:#aaa; font-weight:300;">EXCLUSIVIDAD URBANA PREMIUM</p>
        <h1>LUVIRX STYLE</h1>
        <p>COLECCIÓN 2026</p>
    </div>

    <div class="contenedor">
        <div id="diseno" class="studio-box">
            <h2 style="font-family:'Playfair Display'; color:var(--oro); font-size:2.8rem;">HAZ TU PROPIO DISEÑO</h2>
            <p style="color:#666; margin-top:10px;">Describe tu idea, texturas y formas de diseño únicas. Nosotros la creamos para ti.</p>
            <textarea id="idea-text" placeholder="Ej: Quiero un conjunto de falda y blusa en seda negra con bordados dorados en la espalda..."></textarea>
            <button class="btn-lujo" onclick="enviarDiseno()">Cotizar mi idea</button>
        </div>

        <h2 id="conjuntos" class="titulo-seccion">Conjuntos Premium</h2>
        <div class="grid"><div class="card"><div class="img-vacia">LUVIRX</div><div class="info"><h3>Conjunto "Shadow" Edition</h3><span class="precio">$180.000</span><button class="btn-lujo" onclick="add('Conjunto Shadow', 180000)">Añadir</button></div></div></div>

        <h2 id="jeans" class="titulo-seccion">Jeans Urban</h2>
        <div class="grid"><div class="card"><div class="img-vacia">LUVIRX</div><div class="info"><h3>Jeans Heritage Slim</h3><span class="precio">$125.000</span><button class="btn-lujo" onclick="add('Jeans Urban', 125000)">Añadir</button></div></div></div>

        <h2 id="camisas" class="titulo-seccion">Camisas & Blusas</h2>
        <div class="grid"><div class="card"><div class="img-vacia">LUVIRX</div><div class="info"><h3>Blusa Silk Luxe</h3><span class="precio">$85.000</span><button class="btn-lujo" onclick="add('Blusa Silk', 85000)">Añadir</button></div></div></div>

        <h2 id="deportiva" class="titulo-seccion">Ropa Deportiva</h2>
        <div class="grid"><div class="card"><div class="img-vacia">LUVIRX</div><div class="info"><h3>Licra Pro-Fit</h3><span class="precio">$95.000</span><button class="btn-lujo" onclick="add('Licra Pro', 95000)">Añadir</button></div></div></div>

        <h2 id="galeria3d" class="titulo-seccion">Galería de Diseños 3D</h2>
        <div class="grid-3d">
            <div class="card-3d"><span class="icon-3d">立方</span><h3>Urban Armor 3D</h3><p style="color:#666; font-size:0.9rem;">Concepto de chaqueta asimétrica con texturas modulares.</p></div>
            <div class="card-3d"><span class="icon-3d">立方</span><h3>Seda Digital 3D</h3><p style="color:#666; font-size:0.9rem;">Simulación de drapeado en seda con estampados algorítmicos.</p></div>
        </div>

        <div id="quejas" class="quejas-box">
            <h2 style="font-family:'Playfair Display'; color:red; font-size:2.5rem; margin-bottom:20px;">Quejas y Reclamos</h2>
            <p style="color:#888; margin-bottom:40px;">Tu opinión es fundamental. Háznos saber cualquier inconveniente.</p>
            <div class="form-queja">
                <input type="text" id="q-nombre" placeholder="Nombre completo">
                <input type="text" id="q-contacto" placeholder="Número de contacto o Correo">
                <textarea id="q-mensaje" placeholder="Describe tu queja o reclamo detalladamente..."></textarea>
                <button class="btn-lujo" style="background:red; color:white;" onclick="enviarQueja()">Enviar Queja</button>
            </div>
        </div>
    </div>

    <div id="admin-panel">
        <button onclick="document.getElementById('admin-panel').style.display='none'">CERRAR PANEL</button>
        <h2>PANEL DE GESTIÓN LUVI-STYLE</h2>
        <div id="tabla-admin-content"></div>
    </div>

    <footer style="text-align:center; padding:60px; opacity:0.1; background:#050505; border-top:1px solid #111;" onclick="checkAdmin()">Luvirx Admin Control</footer>

    <script>
        let bolsa = []; let total = 0;
        function add(n, p) { bolsa.push(n); total += p; alert("✓ Producto añadido."); }
        
        async function enviarDiseno() {
            const txt = document.getElementById('idea-text').value;
            if(!txt) return alert("Describe tu diseño exclusivo.");
            await fetch('/api/diseno', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ idea: txt }) });
            window.open(`https://wa.me/{{ wsp }}?text=Hola Luvirx! Quiero cotizar este diseño exclusivo: ${txt}`);
            location.reload();
        }

        async function enviarQueja() {
            const nom = document.getElementById('q-nombre').value;
            const con = document.getElementById('q-contacto').value;
            const msg = document.getElementById('q-mensaje').value;
            if(!nom || !msg) return alert("Por favor completa los campos.");
            await fetch('/api/queja', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ nombre: nom, contacto: con, mensaje: msg }) });
            window.open(`https://wa.me/{{ wsp }}?text=Hola Luvirx! Tengo una Queja/Reclamo: Cliente ${nom}. Mensaje: ${msg}`);
            alert("✓ Queja enviada. Nos comunicaremos contigo.");
            location.reload();
        }

        function checkAdmin() {
            if(prompt("PIN ADMIN:") === "{{ pin }}") {
                document.getElementById('admin-panel').style.display = 'block';
                cargarDatos();
            }
        }

        async function cargarDatos() {
            const res = await fetch('/api/lista'); const data = await res.json();
            let h = '<h3>Pedidos</h3><table class="table-admin"><tr><th>Pedido</th></tr>';
            data.pedidos.forEach(p => h += `<tr><td>${p.items} - $${p.total}</td></tr>`);
            h += '</table><h3>Diseños Propios</h3><table class="table-admin"><tr><th>Idea</th></tr>';
            data.disenos.forEach(d => h += `<tr><td>${d.idea}</td></tr>`);
            h += '</table><h3 style="color:red;">Quejas y Reclamos</h3><table class="table-admin"><tr><th>Cliente</th><th>Mensaje</th></tr>';
            data.quejas.forEach(q => h += `<tr><td>${q.nombre} (${q.contacto})</td><td>${q.mensaje}</td></tr>`);
            document.getElementById('tabla-admin-content').innerHTML = h + '</table>';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_PROFESIONAL, wsp=WSP, pin=PIN_ADMIN)

@app.route('/api/pedido', methods=['POST'])
def pedido(): pedidos_db.append(request.json); return jsonify({"ok": True})

@app.route('/api/diseno', methods=['POST'])
def diseno(): diseños_db.append(request.json); return jsonify({"ok": True})

@app.route('/api/queja', methods=['POST'])
def queja(): quejas_db.append(request.json); return jsonify({"ok": True})

@app.route('/api/lista')
def lista(): return jsonify({"pedidos": pedidos_db, "disenos": diseños_db, "quejas": quejas_db})

if __name__ == '__main__':
    app.run(debug=True)