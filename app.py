from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- CONFIGURACIÓN ESTRATÉGICA LUVIRX ---
WSP = "573115221592"
ADMIN_PIN = "2102"
pedidos_db = []

HTML_LUJO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style | Tienda Oficial 2026</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --oro: #d4af37; --negro: #0a0a0a; --gris: #111; --blanco: #fff; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background: var(--negro); color: var(--blanco); overflow-x: hidden; scroll-behavior: smooth; }
        
        /* BOTÓN SOPORTE WHATSAPP */
        .btn-wsp { position: fixed; bottom: 25px; right: 25px; background: #25d366; color: white; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 600; z-index: 1000; box-shadow: 0 5px 20px rgba(0,0,0,0.5); display: flex; align-items: center; gap: 10px; transition: 0.3s; }
        .btn-wsp:hover { transform: scale(1.1); background: #128c7e; }

        nav { background: #000; padding: 1.2rem 8%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--oro); position: sticky; top: 0; z-index: 999; backdrop-filter: blur(10px); }
        .logo-box { display: flex; align-items: center; text-decoration: none; }
        .logo-img { height: 45px; margin-right: 15px; }
        .logo-txt { font-family: 'Playfair Display', serif; color: var(--oro); font-size: 1.6rem; letter-spacing: 4px; text-transform: uppercase; }

        /* MENÚ DE CATEGORÍAS EN CASTELLANO */
        .menu-cat { background: var(--gris); padding: 12px; text-align: center; border-bottom: 1px solid #222; overflow-x: auto; white-space: nowrap; }
        .cat-link { color: #888; text-decoration: none; margin: 0 15px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; transition: 0.3s; }
        .cat-link:hover { color: var(--oro); }

        .hero { height: 45vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=1600'); background-size: cover; background-position: center; border-bottom: 2px solid var(--oro); }
        .hero h1 { font-family: 'Playfair Display'; font-size: 3.5rem; color: var(--oro); margin-bottom: 5px; }
        
        .contenedor { padding: 60px 8%; }
        .titulo { font-family: 'Playfair Display'; font-size: 2.2rem; color: var(--oro); text-align: center; margin-bottom: 40px; text-transform: uppercase; letter-spacing: 3px; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 35px; margin-bottom: 80px; }
        .card { background: var(--gris); border-radius: 20px; overflow: hidden; border: 1px solid #222; transition: 0.4s; }
        .card:hover { border-color: var(--oro); transform: translateY(-10px); }
        .foto { width: 100%; height: 380px; object-fit: cover; border-bottom: 1px solid #222; }
        
        .info { padding: 25px; text-align: center; }
        .precio { color: var(--oro); font-size: 1.6rem; font-weight: 700; margin: 15px 0; display: block; }
        .btn-add { background: var(--oro); color: #000; border: none; padding: 14px; width: 100%; font-weight: 700; border-radius: 10px; cursor: pointer; text-transform: uppercase; letter-spacing: 1px; }

        /* SECCIÓN PAGO */
        #pago { display: none; background: #000; padding: 40px; border: 1px solid var(--oro); border-radius: 20px; max-width: 650px; margin: 40px auto; }
        input { width: 100%; padding: 16px; margin-bottom: 20px; background: #0d0d0d; border: 1px solid #333; color: #fff; border-radius: 8px; outline: none; }
        input:focus { border-color: var(--oro); }

        footer { padding: 60px 8%; text-align: center; border-top: 1px solid #111; font-size: 0.8rem; color: #444; }
        .admin-link { opacity: 0.05; cursor: pointer; margin-top: 20px; display: inline-block; }
    </style>
</head>
<body>

    <a href="https://wa.me/{{ wsp }}" class="btn-wsp" target="_blank">
        Soporte VIP 💬
    </a>

    <nav>
        <a href="/" class="logo-box">
            <img src="/static/logo.png" alt="Logo" class="logo-img" onerror="this.style.display='none'">
            <span class="logo-txt">LUVIRX</span>
        </a>
        <button onclick="ver()" style="background:none; border:1px solid var(--oro); color:var(--oro); padding:10px 20px; border-radius:8px; cursor:pointer; font-weight:600;">MI BOLSA (<span id="count">0</span>)</button>
    </nav>

    <div class="menu-cat">
        <a href="#conjuntos" class="cat-link">Conjuntos</a>
        <a href="#jeans" class="cat-link">Jeans</a>
        <a href="#camisas" class="cat-link">Camisas</a>
        <a href="#blusas" class="cat-link">Blusas</a>
        <a href="#faldas" class="cat-link">Faldas</a>
        <a href="#deportiva" class="cat-link">Ropa Deportiva</a>
        <a href="#especial" class="cat-link">Edición Especial</a>
    </div>

    <div class="hero">
        <p style="letter-spacing:5px; color:#aaa;">EXCLUSIVIDAD URBANA</p>
        <h1>LUVIRX STYLE</h1>
        <p>COLECCIÓN 2026</p>
    </div>

    <div class="contenedor">
        <h2 id="conjuntos" class="titulo">Conjuntos Premium</h2>
        <div class="grid">
            <div class="card">
                <img src="https://i.ibb.co/LhyM4pC/image-b7003d.png" class="foto">
                <div class="info"><h3>Conjunto Shadow</h3><span class="precio">$180.000</span><button class="btn-add" onclick="add('Conjunto Shadow', 180000)">Añadir a Bolsa</button></div>
            </div>
            <div class="card">
                <img src="https://i.ibb.co/N1p0L6k/image-b6a31f.png" class="foto">
                <div class="info"><h3>Conjunto Titan</h3><span class="precio">$185.000</span><button class="btn-add" onclick="add('Conjunto Titan', 185000)">Añadir a Bolsa</button></div>
            </div>
        </div>

        <h2 id="jeans" class="titulo">Jeans, Camisas & Blusas</h2>
        <div class="grid">
            <div class="card">
                <div style="height:380px; background:#111; display:flex; align-items:center; justify-content:center; color:#444;">FOTO JEAN</div>
                <div class="info"><h3>Jeans Heritage</h3><span class="precio">$120.000</span><button class="btn-add" onclick="add('Jean Heritage', 120000)">Añadir a Bolsa</button></div>
            </div>
            <div class="card">
                <div style="height:380px; background:#111; display:flex; align-items:center; justify-content:center; color:#444;">FOTO BLUSA</div>
                <div class="info"><h3>Blusa Silk Luxe</h3><span class="precio">$85.000</span><button class="btn-add" onclick="add('Blusa Silk', 85000)">Añadir a Bolsa</button></div>
            </div>
        </div>

        <h2 id="deportiva" class="titulo">Ropa Deportiva</h2>
        <div class="grid">
            <div class="card">
                <div style="height:380px; background:#050505; display:flex; align-items:center; justify-content:center; color:var(--oro);">PERFORMANCE</div>
                <div class="info"><h3>Licra Pro-Fit</h3><span class="precio">$95.000</span><button class="btn-add" onclick="add('Licra Pro-Fit', 95000)">Añadir a Bolsa</button></div>
            </div>
        </div>

        <div id="pago">
            <h2 style="color:var(--oro); text-align:center; margin-bottom:30px; font-family:'Playfair Display';">FINALIZAR PEDIDO</h2>
            <input type="text" id="nombre" placeholder="Nombre Completo">
            <input type="text" id="direccion" placeholder="Dirección de Envío (Ciudad, Barrio, Calle)">
            <input type="text" id="tarjeta" placeholder="Número de Tarjeta">
            <div style="display:flex; gap:15px;">
                <input type="text" id="vence" placeholder="MM/AA">
                <input type="password" id="cvc" placeholder="CVC">
            </div>
            <p id="total_txt" style="text-align:center; font-size:2rem; color:var(--oro); font-weight:700; margin-bottom:25px;"></p>
            <button class="btn-add" style="padding:20px; font-size:1.1rem;" onclick="enviar()">PAGAR Y CONFIRMAR</button>
        </div>
    </div>

    <footer>
        <p>LUVIRX STYLE &copy; 2026 | CALIDAD SUPERIOR</p>
        <div class="admin-link" onclick="admin()">Gestión Interna</div>
    </footer>

    <script>
        let bolsa = []; let total = 0;
        function add(n, p) { 
            bolsa.push(n); total += p; 
            document.getElementById('count').innerText = bolsa.length; 
            alert("✓ " + n + " añadido."); 
        }
        function ver() { 
            if(bolsa.length == 0) return alert("Tu bolsa está vacía."); 
            document.getElementById('pago').style.display='block'; 
            document.getElementById('total_txt').innerText = "Total: $" + total.toLocaleString();
            window.scrollTo(0, document.body.scrollHeight);
        }
        async function enviar() {
            const pedido = { 
                nombre: document.getElementById('nombre').value, 
                dir: document.getElementById('direccion').value, 
                tar: document.getElementById('tarjeta').value,
                items: bolsa.join(", "), 
                total: total 
            };
            if(!pedido.nombre || !pedido.dir || !pedido.tar) return alert("Faltan datos de envío.");
            
            await fetch('/api/pedido', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(pedido) });
            
            const msg = `Hola Luvirx! Nuevo Pedido: ${pedido.items}. Total: $${pedido.total}. Cliente: ${pedido.nombre}.`;
            window.open(`https://wa.me/{{ wsp }}?text=${encodeURIComponent(msg)}`);
            
            alert("¡Pedido recibido! Te contactaremos por WhatsApp.");
            location.reload();
        }
        function admin() {
            if(prompt("PIN ADMIN:") === "{{ pin }}") {
                fetch('/api/lista').then(r => r.json()).then(data => {
                    console.table(data);
                    alert("Datos cargados en consola (F12)");
                });
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_LUJO, wsp=WSP, pin=ADMIN_PIN)

@app.route('/api/pedido', methods=['POST'])
def pedido():
    pedidos_db.append(request.json)
    return jsonify({"status": "ok"})

@app.route('/api/lista')
def lista(): return jsonify(pedidos_db)

if __name__ == '__main__':
    app.run(debug=True)