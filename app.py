from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def home():
    # Buscamos tu logo en la carpeta static
    logo_url = url_for('static', filename='logo_luvirx.jpeg')
    
    return f"""
    <!DOCTYPE html>
    <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Luvirx Style - Mobile</title>
            <link rel="icon" type="image/jpeg" href="{logo_url}">
            <style>
                body {{ 
                    background-color: #000; color: #d4af37; 
                    font-family: sans-serif; text-align: center; margin: 0; padding: 20px;
                }}
                img {{ max-width: 80%; border-radius: 10px; margin-top: 20px; }}
                .btn {{
                    display: inline-block; padding: 15px 30px; 
                    background: #d4af37; color: #000; 
                    text-decoration: none; font-weight: bold; border-radius: 25px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <img src="{logo_url}" alt="Logo Luvirx">
            <h1>LUVIRX STYLE</h1>
            <p>Elegancia exclusiva en tu dispositivo</p>
            <a href="#" class="btn">ENTRAR</a>
        </body>
    </html>
    """

if __name__ == "__main__":
    # IMPORTANTE: host='0.0.0.0' permite la conexión desde tu celular
    app.run(debug=True, host='0.0.0.0')
