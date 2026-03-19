from flask import Flask, render_template_string

app = Flask(__name__)

# CONFIGURACIÓN REAL
WHATSAPP_NUMBER = "573115221592" 

HTML_CODE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style | Checkout</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #000; --card: #111; --accent: #d4af37; --text: #fff; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Montserrat', sans-serif; }
        body { background: var(--bg); color: var(--text); padding-bottom: 100px; }
        
        nav { background: #000; padding: 1.5rem; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid var(--accent); }
        .logo { font-weight: 700; letter-spacing: 5px; color: var(--accent); text-transform: uppercase; text-decoration: none; }
        .cart-icon { cursor: pointer; color: var(--accent); position: relative; }
        #cart-count { background: red; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px; position: absolute; top: -10px; right: -10px; }

        .container { padding: 40px 5%; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .card { background: var(--card); padding: 20px; border-radius: 10px; border: 1px solid #222; text-align: center; }
        .price { color: var(--accent); font-weight: bold; display: block; margin: 10px 0; }
        
        .btn-add { background: var(--accent); color: #000; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; width: 100%; text-transform: uppercase; }

        /* SECCIÓN CARRITO Y PAGO */
        #checkout-section { display: none; background: #0a0a0a; padding: 30px; border: 1px solid var(--accent); margin-top: 40px; border-radius: 15px; }
        .form-group { margin-bottom: 15px; text-align: left; }
        label { display: block; color: var(--accent); font-size: 0.8rem; margin-bottom: 5px; }
        input { width: 100%; padding: 12px; background: #111; border: 1px solid #333; color: #fff; border-radius: 5px; }
        .btn-pay { background: #fff; color: #000; border: none; padding: 15px; width: 100%; font-weight: bold; cursor: pointer; margin-top: 20px; }

        /* MENSAJE GRACIAS */
        #thanks-msg { display: none; text-align: center; padding: 50px; }
        #thanks-msg h2 { color: var(--accent); font-size: 2.5rem; }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">Luvirx</a>
        <div class="cart-icon" onclick="showCheckout()">🛒 <span id="cart-count">0</span></div>
    </nav>

    <div class="container" id="main-content">
        <h2 style="text-align:center; margin-bottom:30px; letter-spacing:3px;">NUESTROS PRODUCTOS</h2>
        <div class="grid">
            <div class="card">
                <h3>Urban Set Premium</h3>
                <span class="price">$180.000</span>
                <button class="btn-add" onclick="addToCart('Urban Set Premium', 180000)">Agregar al Carrito</button>
            </div>
            <div class="card">
                <h3>Slim Fit Heritage</h3>
                <span class="price">$120.000</span>
                <button class="btn-add" onclick="addToCart('Slim Fit Heritage', 120000)">Agregar al Carrito</button>
            </div>
            <div class="card">
                <h3>Special Edition Jacket</h3>
                <span class="price">$250.000</span>
                <button class="btn-add" onclick="addToCart('Special Edition Jacket', 250000)">Agregar al Carrito</button>
            </div>
        </div>

        <div id="checkout-section">
            <h2 style="color:var(--accent); margin-bottom:20px;">Tu Carrito (<span id="total-price">$0</span>)</h2>
            <div class="form-group">
                <label>Nombre Completo</label>
                <input type="text" placeholder="Como aparece en la tarjeta">
            </div>
            <div class="form-group">
                <label>Número de Tarjeta (Débito/Crédito)</label>
                <input type="text" placeholder="0000 0000 0000 0000">
            </div>
            <div style="display:flex; gap:10px;">
                <div class="form-group" style="flex:2;">
                    <label>Fecha Expiración</label>
                    <input type="text" placeholder="MM/AA">
                </div>
                <div class="form-group" style="flex:1;">
                    <label>CVC</label>
                    <input type="password" placeholder="123">
                </div>
            </div>
            <button class="btn-pay" onclick="processPayment()">FINALIZAR COMPRA</button>
        </div>

        <div id="thanks-msg">
            <h2>¡GRACIAS POR TU COMPRA!</h2>
            <p style="margin-top:20px;">Tu pedido de <b>Luvirx Style</b> está siendo procesado.</p>
            <p style="color:#888; font-size:0.8rem; margin-top:10px;">Te contactaremos al WhatsApp 3115221592 para el envío.</p>
            <button class="btn-pay" onclick="location.reload()">VOLVER A LA TIENDA</button>
        </div>
    </div>

    <script>
        let cart = [];
        let total = 0;

        function addToCart(name, price) {
            cart.push(name);
            total += price;
            document.getElementById('cart-count').innerText = cart.length;
            alert(name + " agregado al carrito");
        }

        function showCheckout() {
            if(cart.length === 0) {
                alert("El carrito está vacío");
                return;
            }
            document.getElementById('checkout-section').style.display = 'block';
            document.getElementById('total-price').innerText = "$" + total.toLocaleString();
            window.scrollTo(0, document.body.scrollHeight);
        }

        function processPayment() {
            document.getElementById('checkout-section').style.display = 'none';
            document.getElementById('main-content').querySelectorAll('.grid, h2').forEach(el => el.style.display = 'none');
            document.getElementById('thanks-msg').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(debug=True)