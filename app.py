from flask import Flask, render_template_string

app = Flask(__name__)

# DISEÑO LIMPIO SIN ERRORES 502
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style</title>
    <style>
        body { background-color: #0a0a0a; color: #d4af37; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
        .hero { padding: 100px 20px; border-bottom: 1px solid #333; }
        h1 { font-size: 3rem; letter-spacing: 5px; text-transform: uppercase; }
        .section { margin-top: 50px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; padding: 20px; }
        .card { background: #161616; padding: 20px; border: 1px solid #d4af37; border-radius: 10px; }
        .price { font-size: 1.5rem; font-weight: bold; margin: 15px 0; }
        .btn { display: inline-block; padding: 12px 25px; background: #d4af37; color: #000; text-decoration: none; font-weight: bold; border-radius: 5px; }
        nav { background: #000; padding: 20px; border-bottom: 1px solid #d4af37; position: sticky; top: 0; }
        nav a { color: #fff; text-decoration: none; margin: 0 10px; font-size: 0.8rem; text-transform: uppercase; }
    </style>
</head>
<body>
    <nav>
        <a href="#conjuntos">Conjuntos</a>
        <a href="#jeans">Jeans</a>
        <a href="#camisas">Camisas</a>
        <a href="#special">Special Edition</a>
    </nav>

    <div class="hero">
        <p style="letter-spacing: 5px;">BIENVENIDO A</p>
        <h1>LUVIRX STYLE</h1>
        <p>ELEGANCIA Y EXCLUSIVIDAD</p>
    </div>

    <div class="grid">
        <div id="conjuntos" class="card">
            <h2>CONJUNTOS</h2>
            <p class="price">$180.000</p>
            <a href="https://wa.me/573000000000" class="btn">PEDIR WHATSAPP</a>
        </div>
        <div id="jeans" class="card">
            <h2>JEANS</h2>
            <p class="price">$120.000</p>
            <a href="https://wa.me/573000000000" class="btn">PEDIR WHATSAPP</a>
        </div>
        <div id="camisas" class="card">
            <h2>CAMISAS</h2>
            <p class="price">$95.000</p>
            <a href="https://wa.me/573000000000" class="btn">PEDIR WHATSAPP</a>
        </div>
        <div id="special" class="card" style="border-width: 3px;">
            <h2>SPECIAL EDITION ✨</h2>
            <p class="price">$250.000</p>
            <a href="https://wa.me/573000000000" class="btn" style="background: #fff;">APARTAR AHORA</a>
        </div>
    </div>
    
    <footer style="margin-top: 50px; color: #555;">&copy; 2026 LUVIRX STYLE</footer>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(debug=True)