from flask import Flask, render_template_string

app = Flask(__name__)

# VERSION TURBO - CARGA INSTANTÁNEA
HTML_CODE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style | Luxury Shop</title>
    <style>
        body { margin: 0; background-color: #000; color: #fff; font-family: sans-serif; text-align: center; scroll-behavior: smooth; }
        nav { background: #111; padding: 15px; position: sticky; top: 0; border-bottom: 1px solid #d4af37; z-index: 100; }
        nav a { color: #fff; text-decoration: none; margin: 0 10px; font-size: 12px; text-transform: uppercase; }
        .hero { height: 60vh; display: flex; flex-direction: column; justify-content: center; align-items: center; background: linear-gradient(#000, #111); border-bottom: 1px solid #222; }
        .hero h1 { font-size: 3rem; letter-spacing: 5px; margin: 0; color: #d4af37; }
        .hero p { letter-spacing: 3px; color: #888; }
        .btn-start { margin-top: 20px; padding: 10px 25px; border: 1px solid #d4af37; color: #d4af37; text-decoration: none; text-transform: uppercase; font-size: 12px; }
        .container { padding: 40px 20px; }
        .section-title { color: #d4af37; text-transform: uppercase; letter-spacing: 2px; margin: 40px 0 20px; border-bottom: 1px solid #222; padding-bottom: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .card { background: #0a0a0a; padding: 20px; border-radius: 5px; border: 1px solid #111; }
        .price { color: #d4af37; font-weight: bold; font-size: 1.2rem; }
        .btn-wa { display: block; margin-top: 15px; padding: 10px; background: #fff; color: #000; text-decoration: none; font-size: 11px; font-weight: bold; border-radius: 3px; }
        footer { padding: 40px; color: #444; font-size: 10px; letter-spacing: 2px; }
    </style>
</head>
<body>
    <nav>
        <a href="#conjuntos">Conjuntos</a>
        <a href="#jeans">Jeans</a>
        <a href="#camisas">Camisas</a>
        <a href="#special">Special</a>
    </nav>

    <section class="hero">
        <p>BIENVENIDO A</p>
        <h1>LUVIRX STYLE</h1>
        <p>EXCLUSIVIDAD URBANA</p>
        <a href="#catalogo" class="btn-start">Ver Colección</a>
    </section>

    <div id="catalogo" class="container">
        <h2 id="conjuntos" class="section-title">Conjuntos</h2>
        <div class="grid">
            <div class="card">
                <h3>Urban Set Premium</h3>
                <p class="price">$180.000</p>
                <a href="https://wa.me/573000000000" class="btn-wa">PEDIR POR WHATSAPP</a>
            </div>
        </div>

        <h2 id="jeans" class="section-title">Jeans</h2>
        <div class="grid">
            <div class="card">
                <h3>Slim Fit Classic</h3>
                <p class="price">$120.000</p>
                <a href="https://wa.me/573000000000" class="btn-wa">PEDIR POR WHATSAPP</a>
            </div>
        </div>

        <h2 id="camisas" class="section-title">Camisas</h2>
        <div class="grid">
            <div class="card">
                <h3>Camisa Lino</h3>
                <p class="price">$95.000</p>
                <a href="https://wa.me/573000000000" class="btn-wa">PEDIR POR WHATSAPP</a>
            </div>
        </div>

        <h2 id="special" class="section-title" style="color: #fff; background: #d4af37; padding: 5px;">Special Edition ✨</h2>
        <div class="grid">
            <div class="card" style="border-color: #d4af37;">
                <h3>Chaqueta Gold Heritage</h3>
                <p class="price">$250.000</p>
                <a href="https://wa.me/573000000000" class="btn-wa" style="background: #d4af37; color: #000;">APARTAR EDICIÓN ESPECIAL</a>
            </div>
        </div>
    </div>

    <footer>LUVIRX STYLE &copy; 2026 - CALIDAD GARANTIZADA</footer>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(debug=True)