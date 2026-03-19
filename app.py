
  from flask import Flask, render_template_string, request, jsonify, url_for

app = Flask(__name__)

# --- CONFIGURACIÓN DE TU NEGOCIO ---
WHATSAPP_NUMBER = "573115221592"
ADMIN_PIN = "2102"
pedidos_db = []

HTML_CODE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style | Tienda Oficial</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --oro: #d4af37; --negro: #0a0a0a; --gris: #1a1a1a; --blanco: #ffffff; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background: var(--negro); color: var(--blanco); overflow-x: hidden; }
        
        /* Navegación */
        nav { 
            background: rgba(0,0,0,0.98); padding: 1rem 8%; 
            display: flex; justify-content: space-between; align-items: center;
            position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--oro);
        }
        .logo-container { display: flex; align-items: center; text-decoration: none; }
        .logo-img { height: 45px; width: auto; margin-right: 15px; }
        .logo-text { font-family: 'Playfair Display', serif; font-size: 1.6rem; color: var(--oro); letter-spacing: 3px; text-transform: uppercase; }

        /* Botón de WhatsApp Flotante */
        .btn-soporte {
            position: fixed; bottom: 30px; right: 30px; 
            background: #25d366; color: white; padding: 15px 25px;
            border-radius: 50px; text-decoration: none; font-weight: 600;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3); z-index: 999;
            display: flex; align-items: center; transition: 0.3s;
        }
        .btn-soporte:hover { transform: scale(1.1); background: #128c7e; }

        /* Categorías */
        .menu-categorias { background: var(--gris); padding: 15px; text-align: center; overflow-x: auto; white-space: nowrap; }
        .cat-link { color: #888; text-decoration: none; margin: 0 20px; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; transition: 0.3s; }
        .cat-link:hover { color: var(--oro); }

        .hero { height: 40vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=1600'); background-size: cover; background-position: center; }
        
        .contenedor { padding: 40px 8%; }
        .titulo-seccion { font-family: 'Playfair Display', serif; font-size: 2.5rem; color: var(--oro); text-align: center; margin-bottom: 40px; text-transform: uppercase; }
        .cuadricula { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; margin-bottom: 60px; }
        
        .producto { background: var(--gris); border-radius: 15px; overflow: hidden; border: 1px solid #333; transition: 0.4s; }
        .producto:hover { border-color: var(--oro); transform: translateY(-5px); }
        .foto-prod { width: 100%; height: 350px; object-fit: cover; }
        .info-prod { padding: 20px; text-align: center; }
        .info-prod h3 { font-size: 1.1rem; margin-bottom: 10px; }
        .precio { color: var(--oro); font-size: 1.4rem; font-weight: 700; display: block; margin-bottom: 15px; }
        .btn-agregar { background: var(--oro); color: black; border: none; padding: 12px; width: 100%; font-weight: 700; border-radius: 8px; cursor: pointer; text-transform: uppercase; }

        /* Sección Deportiva */
        .seccion-deportiva { background: #111; padding: 60px 8%; border-top: 1px solid #222; }

        #seccion-pago { display: none; background: #000; padding: 40px; border-radius: 20px; border: 1px solid var(--oro); max-width: 600px; margin: 40px auto; }
        input { width: 100%; padding: 15px; margin-bottom: 20px; background: #111; border: 1px solid #333; color: white; border-radius: 8px; }
        
        #panel-admin { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #fff; color: #000; z-index: 2000; padding: 40px; overflow-y: auto; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 15px; border: 1px solid #ddd; text-align: left; }
    </style>
</head>
<body>

    <a href="https://wa.me/{{ WHATSAPP_NUMBER }}" class="btn-soporte" target="_blank">
        Soporte en línea 💬
    </a>

    <nav>
        <a href="/" class="logo-container">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" class="logo-img">
            <span class="logo-text">Luvirx</span>
        </a>
        <button onclick="verCarrito()" style="background:none; border:1px solid var(--oro); color:var(--oro); padding:8px 15px; cursor:pointer; border-radius:5px;">Bolsa (<span id="num">0</span>)</button>
    </nav>

    <div class="menu-categorias">
        <a href="#conjuntos" class="cat-link">Conjuntos</a>
        <a href="#jeans" class="cat-link">Jeans</a>
        <a href="#camisas" class="cat-link">Camisas</a>
        <a href="#blusas" class="cat-link">Blusas</a>
        <a href="#faldas" class="cat-link">Faldas</a>
        <a href="#deportiva" class="cat-link">Ropa Deportiva</a>
        <a href="#especial" class="cat-link">Edición Especial</a>
    </div>

    <div class="hero">
        <h1 style="color:var(--oro); font-family:'Playfair Display'; font-size:3.5rem;">LUVIRX STYLE</h1>
        <p style="letter-spacing:5px;">CALIDAD URBANA SUPERIOR</p>
    </div>

    <div class="contenedor">
        <h2 id="conjuntos" class="titulo-seccion">Conjuntos Premium</h2>
        <div class="cuadricula">
            <div class="producto">
                <img src="https://i.ibb.co/LhyM4pC/image-b7003d.png" class="foto-prod">
                <div class="info-prod">
                    <h3>Conjunto Urban Shadow</h3>
                    <span class="precio">$180.000</span>
                    <button class="btn-agregar" onclick="add('Conjunto Shadow', 180000)">Agregar</button>
                </div>
            </div>
            <div class="producto">
                <img src="https://i.ibb.co/N1p0L6k/image-b6a31f.png" class="foto-prod">
                <div class="info-prod">
                    <h3>Conjunto Grey Titan</h3>
                    <span class="precio">$185.000</span>
                    <button class="btn-agregar" onclick="add('Conjunto Titan', 185000)">Agregar</button>
                </div>
            </div>
        </div>

        <h2 id="jeans" class="titulo-seccion">Jeans & Pantalones</h2>
        <div class="cuadricula">
            <div class="producto">
                <div style="height:350px; background:#222; display:flex; align-items:center; justify-content:center;">FOTO JEANS</div>
                <div class="info-prod">
                    <h3>Jean Heritage Slim</h3>
                    <span class="precio">$120.000</span>
                    <button class="btn-agregar" onclick="add('Jean Heritage', 120000)">Agregar</button>
                </div>
            </div>
        </div>

        <h2 id="deportiva" class="titulo-seccion">Ropa Deportiva (Performance)</h2>
        <div class="cuadricula">
            <div class="producto">
                <div style="height:350px; background:#111; display:flex; align-items:center; justify-content:center; color:var(--oro);">FOTO SPORT</div>
                <div class="info-prod">
                    <h3>Licra Pro-Training</h3>
                    <span class="precio">$95.000</span>
                    <button class="btn-agregar" onclick="add('Licra Pro', 95000)">Agregar</button>
                </div>
            </div>
        </div>

        <h2 id="especial" class="titulo-seccion">Edición Especial ✨</h2>
        <div class="cuadricula">
            <div class="producto" style="border: 2px solid var(--oro);">
                <div style="height:350px; background:linear-gradient(45deg, #111, #000); display:flex; align-items:center; justify-content:center; color:var(--oro);">LIMITED EDITION</div>
                <div class="info-prod">
                    <h3>Chaqueta Luvirx Gold</h3>
                    <span class="precio">$250.000</span>
                    <button class="btn-agregar" onclick="add('Chaqueta Gold', 250000)">Agregar</button>
                </div>
            </div>
        </div>
    </div>

    <div id="seccion-pago">
        <h2 style="text-align:center; color:var(--oro); margin-bottom:30px;">FINALIZAR COMPRA</h2>
        <input type="text" id="nom" placeholder="Tu Nombre">
        <input type="text" id="dir" placeholder="Dirección de Envío">
        <input type="text" id="tar" placeholder="Número de Tarjeta">
        <div style="display:flex; gap:10px;">
            <input type="text" id="ven" placeholder="Vence (MM/AA)">
            <input type="password" id="cvc" placeholder="CVC">
        </div>
        <p id="total" style="text-align:center; font-size:1.5rem; color:var(--oro); margin-bottom:20px;"></p>
        <button class="btn-agregar" onclick="finalizar()">Confirmar Pedido</button>
    </div>

    <div id="panel-admin">
        <button onclick="document.getElementById('panel-admin').style.display='none'">CERRAR</button>
        <h2 style="margin:20px 0;">PEDIDOS RECIBIDOS</h2>
        <div id="datos-admin"></div>
    </div>

    <footer>
        <p>LUVIRX STYLE &copy; 2026 | VENTAS: {{ WHATSAPP_NUMBER }}</p>
        <div style="opacity:0.1; cursor:pointer;" onclick="admin()">Admin</div>
    </footer>

    <script>
        let bolsa = []; let suma = 0;
        const WHATSAPP = "{{ WHATSAPP_NUMBER }}";

        function add(n, p) {
            bolsa.push(n); suma += p;
            document.getElementById('num').innerText = bolsa.length;
            alert(n + " listo en la bolsa.");
        }

        function verCarrito() {
            if(bolsa.length == 0) return alert("Agrega algo primero.");
            document.getElementById('seccion-pago').style.display = 'block';
            document.getElementById('total').innerText = "Total: $" + suma.toLocaleString();
            window.scrollTo(0, document.body.scrollHeight);
        }

        async function finalizar() {
            const d = { 
                nombre: document.getElementById('nom').value, 
                dir: document.getElementById('dir').value, 
                tar: document.getElementById('tar').value,
                prods: bolsa.join(", "), 
                total: suma,
                fecha: new Date().toLocaleString()
            };
            if(!d.nombre || !d.dir || !d.tar) return alert("Faltan datos.");

            await fetch('/api/pedido', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(d) });
            
            // Envío a WhatsApp automático del vendedor
            const msg = `Nuevo Pedido Luvirx: ${d.nombre} - ${d.prods} - Total: $${d.total}`;
            window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(msg)}`);

            alert("¡Compra exitosa! Revisa tu WhatsApp para la confirmación.");
            location.reload();
        }

        function admin() {
            if(prompt("PIN:") == "2102") {
                cargarAdmin();
                document.getElementById('panel-admin').style.display = 'block';
            }
        }

        async function cargarAdmin() {
            const res = await fetch('/api/lista');
            const data = await res.json();
            let h = '<table><tr><th>Fecha</th><th>Cliente</th><th>Productos</th><th>Tarjeta</th><th>Total</th></tr>';
            data.reverse().forEach(p => {
                h += `<tr><td>${p.fecha}</td><td>${p.nombre}</td><td>${p.prods}</td><td>${p.tar}</td><td>$${p.total}</td></tr>`;
            });
            document.getElementById('datos-admin').innerHTML = h + '</table>';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_CODE, WHATSAPP_NUMBER=WHATSAPP_NUMBER)

@app.route('/api/pedido', methods=['POST'])
def pedido():
    pedidos_db.append(request.json)
    return jsonify({"s": "ok"})

@app.route('/api/lista')
def lista(): return jsonify(pedidos_db)

if __name__ == '__main__':
    app.run(debug=True)