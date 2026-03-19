from flask import Flask, render_template_string

app = Flask(__name__)

# Diseño HTML y CSS Profesional Integrado - Luvirx Style v3.0
# Mantiene tus datos reales y agrega una Bienvenida de Diseñador
HTML_CODE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Luvirx Style | Luxury Urban Fashion</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0a0a0a;
            --card-bg: #161616;
            --text: #ffffff;
            --accent: #d4af37; /* Dorado Premium */
            --gray: #888888;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; scroll-behavior: smooth; }
        body { font-family: 'Montserrat', sans-serif; background-color: var(--bg); color: var(--text); overflow-x: hidden; }

        /* Barra de Navegación Estilo Glassmorphism (Vidrio Esmerilado) */
        nav { 
            background: rgba(22, 22, 22, 0.8); 
            backdrop-filter: blur(10px);
            padding: 1rem 5%; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            position: sticky; 
            top: 0; 
            z-index: 1000;
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        }
        .logo { font-weight: 700; font-size: 1.8rem; letter-spacing: 4px; color: var(--accent); text-transform: uppercase; }
        .nav-links a { text-decoration: none; color: var(--text); margin-left: 20px; font-size: 0.8rem; font-weight: 300; transition: 0.3s; text-transform: uppercase; }
        .nav-links a:hover { color: var(--accent); }

        /* NUEVA SECCIÓN DE BIENVENIDA DE DISEÑADOR (Hero Section) */
        .welcome-hero { 
            height: 75vh; 
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=1600&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed; /* Efecto Parallax */
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            text-align: center; 
            padding: 20px;
        }
        .welcome-hero p.brand-intro { font-weight: 300; letter-spacing: 6px; color: var(--accent); text-transform: uppercase; font-size: 0.9rem; margin-bottom: 15px; }
        .welcome-hero h1 { font-size: 4rem; margin-bottom: 20px; letter-spacing: 12px; font-weight: 700; text-transform: uppercase; line-height: 1.1; }
        .welcome-hero h1 span { color: var(--accent); }
        .welcome-hero p.tagline { font-weight: 300; letter-spacing: 4px; color: #ccc; font-size: 1.1rem; margin-bottom: 40px; max-width: 600px; }
        
        /* Botón de bienvenida que baja al catálogo */
        .btn-discover { 
            background: transparent; 
            color: var(--accent); 
            padding: 15px 40px; 
            border: 2px solid var(--accent); 
            text-decoration: none; 
            font-size: 0.9rem; 
            letter-spacing: 3px;
            transition: 0.4s;
            text-transform: uppercase;
            font-weight: 700;
        }
        .btn-discover:hover { background: var(--accent); color: var(--bg); transform: scale(1.05); }

        /* Contenedor de Secciones del Catálogo */
        .container { padding: 80px 8% 40px; }
        .section-header { margin-bottom: 40px; }
        .section-header h2 { font-size: 2rem; letter-spacing: 3px; text-transform: uppercase; position: relative; display: inline-block; padding-bottom: 10px; }
        .section-header h2::after { content: ''; width: 60%; height: 2px; background: var(--accent); position: absolute; bottom: 0; left: 0; }

        /* Grid de Productos Moderno (Cartas) */
        .product-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 40px; 
            margin-bottom: 80px; 
        }
        .product-card { 
            background: var(--card-bg); 
            border-radius: 15px; 
            overflow: hidden; 
            transition: 0.4s ease-out; 
            border: 1px solid rgba(255,255,255,0.03);
            position: relative;
        }
        .product-card:hover { transform: translateY(-15px); border-color: rgba(212, 175, 55, 0.4); box-shadow: 0 15px 35px rgba(212, 175, 55, 0.1); }
        
        /* Caja de imagen placeholder elegante */
        .product-img-box { 
            width: 100%; 
            height: 380px; 
            background: #1a1a1a; 
            display: flex; 
            align-items: center;