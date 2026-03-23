# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, jsonify, url_for
import datetime

app = Flask(__name__)

# ==============================================================================
# CONFIGURACIÓN ESTRATÉGICA Y SEGURIDAD DE DATOS (LUVIRX ENTERPRISE)
# ==============================================================================
WSP_OFFICIAL = "573115221592"
ADMIN_PIN_ACCESS = "2102"
SYSTEM_VERSION = "3.0.1 - Diamond Edition"

# ESTRUCTURA DE ALMACENAMIENTO DE ALTA DENSIDAD (DB EN MEMORIA)
# Esta estructura permite rastrear cada interacción del cliente en la plataforma.
storage_system = {
    "ventas_realizadas": [],
    "disenos_solicitados": [],
    "quejas_clientes": [],
    "leads_promociones": [],
    "analitica_ventas": {
        "total_recaudado": 0,
        "conteo_pedidos": 0,
        "interacciones_wsp": 0,
        "logs_sistema": []
    }
}

# ==============================================================================
# CATALOGO MAESTRO DE PRODUCTOS (BASE DE DATOS EXTENSA Y DETALLADA)
# ==============================================================================
MASTER_CATALOG = {
    "promociones": [
        {"id": "PROMO-001", "nombre": "Combo Signature Elite", "precio_original": 420000, "precio_oferta": 294000, "descuento": "30% OFF", "desc": "Incluye Conjunto Onyx Urban + Camisa Oxford Luvirx. El epítome del estilo ejecutivo."},
        {"id": "PROMO-002", "nombre": "Denim Collector Pack", "precio_original": 320000, "precio_oferta": 224000, "descuento": "30% OFF", "desc": "Dúo de Jeans Heritage Slim. Denim japonés de 14oz con acabados artesanales."},
        {"id": "PROMO-003", "nombre": "Active Luxury Bundle", "precio_original": 250000, "precio_oferta": 175000, "descuento": "30% OFF", "desc": "Leggings Pro-Performance + Top Impact Studio. Rendimiento y elegancia."}
    ],
    "conjuntos": [
        {"id": "C-101", "nombre": "Conjunto Onyx Urban", "precio": 185000, "desc": "Seda y Algodón Premium. Corte sastre contemporáneo.", "stock": "Disponible", "color": "Negro Profundo"},
        {"id": "C-102", "nombre": "Conjunto Marble White", "precio": 210000, "desc": "Edición Limitada. Texturas orgánicas de lino italiano.", "stock": "Bajo Stock", "color": "Blanco Mármol"},
        {"id": "C-103", "nombre": "Conjunto Midnight Blue", "precio": 195000, "desc": "Tejido Térmico Inteligente para climas variables.", "stock": "Disponible", "color": "Azul Noche"},
        {"id": "C-104", "nombre": "Conjunto Emerald Luxe", "precio": 225000, "desc": "Acabado satinado con detalles en bordado manual.", "stock": "Disponible", "color": "Verde Esmeralda"}
    ],
    "jeans": [
        {"id": "J-201", "nombre": "Jean Heritage Slim", "precio": 145000, "desc": "Denim Japonés de alta densidad. Elástico confort.", "stock": "Disponible", "color": "Indigo"},
        {"id": "J-202", "nombre": "Jean Street Baggy", "precio": 130000, "desc": "Corte Oversize inspirado en la cultura urbana global.", "stock": "Disponible", "color": "Gris Ácido"},
        {"id": "J-203", "nombre": "Jean Cargo Tactical", "precio": 160000, "desc": "Ocho bolsillos funcionales con refuerzo militar.", "stock": "Disponible", "color": "Kaki"},
        {"id": "J-204", "nombre": "Jean Flare Vintage", "precio": 155000, "desc": "Inspiración años 70 con tecnología de ajuste moderno.", "stock": "Disponible", "color": "Azul Medio"}
    ],
    "camisas": [
        {"id": "CM-301", "nombre": "Camisa Oxford Luvirx", "precio": 95000, "desc": "100% Algodón Pima. Cuello rígido italiano.", "stock": "Disponible", "color": "Blanco"},
        {"id": "CM-302", "nombre": "Camisa Versailles Print", "precio": 115000, "desc": "Estampado digital exclusivo. Tacto seda.", "stock": "Disponible", "color": "Multicolor"},
        {"id": "CM-303", "nombre": "Camisa Urban Linen", "precio": 105000, "desc": "Lino transpirable para eventos de verano.", "stock": "Disponible", "color": "Arena"},
        {"id": "CM-304", "nombre": "Camisa Black Formal", "precio": 110000, "desc": "Slim fit con botones ocultos. Máxima elegancia.", "stock": "Disponible", "color": "Negro"}
    ],
    "blusas": [
        {"id": "B-401", "nombre": "Blusa Silk Radiance", "precio": 85000, "desc": "Seda natural con caída fluida. Cuello V.", "stock": "Disponible", "color": "Marfil"},
        {"id": "B-402", "nombre": "Blusa Velvet Night", "precio": 90000, "desc": "Terciopelo de alta densidad. Mangas abullonadas.", "stock": "Disponible", "color": "Vino"},
        {"id": "B-403", "nombre": "Blusa Chiffon Dream", "precio": 78000, "desc": "Transparencias elegantes con forro de algodón.", "stock": "Disponible", "color": "Rosa Pastel"}
    ],
    "faldas": [
        {"id": "F-501", "nombre": "Falda Midi Plisada", "precio": 75000, "desc": "Efecto satinado. Cintura elástica invisible.", "stock": "Disponible", "color": "Dorado Metálico"},
        {"id": "F-502", "nombre": "Minifalda Leather Luxe", "precio": 95000, "desc": "Cuero vegano importado. Cremalleras de lujo.", "stock": "Disponible", "color": "Negro"},
        {"id": "F-503", "nombre": "Falda Lápiz Business", "precio": 88000, "desc": "Corte profesional con apertura lateral sutil.", "stock": "Disponible", "color": "Gris Oxford"}
    ],
    "deportiva": [
        {"id": "D-601", "nombre": "Leggings Pro-Performance", "precio": 110000, "desc": "Tecnología Dry-Fit. No trasluce. Compresión media.", "stock": "Disponible", "color": "Gris Carbón"},
        {"id": "D-602", "nombre": "Top Impact Studio", "precio": 65000, "desc": "Soporte para alta intensidad. Secado rápido.", "stock": "Disponible", "color": "Fucsia Neón"},
        {"id": "D-603", "nombre": "Short Biker Pro", "precio": 55000, "desc": "Costuras planas antiroce. Ajuste ergonómico.", "stock": "Disponible", "color": "Azul Eléctrico"}
    ]
}

# ==============================================================================
# MOTOR DE INTERFAZ DE USUARIO (UI/UX - CÓDIGO MASIVO DE FRONTEND)
# ==============================================================================
HTML_PLATFORM_V3 = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Luvirx Style | Luxury Apparel Group & 3D Engineering</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Poppins:wght@100;200;300;400;600;700;800;900&family=Montserrat:wght@100;300;500;700;900&display=swap" rel="stylesheet">
    
    <style>
        /* VARIABLES DE SISTEMA */
        :root {
            --lux-oro: #d4af37;
            --lux-oro-glow: #f1c40f;
            --lux-negro: #000000;
            --lux-negro-soft: #050505;
            --lux-gris-dark: #111111;
            --lux-gris-mid: #1a1a1a;
            --lux-blanco: #ffffff;
            --lux-error: #ff4d4d;
            --lux-success: #2ecc71;
            --lux-shadow: 0 30px 60px rgba(0,0,0,0.8);
            --transition-smooth: all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
        }

        /* RESET CORPORATIVO */
        * { margin: 0; padding: 0; box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; }
        html { scroll-behavior: smooth; }
        body { background-color: var(--lux-negro); color: var(--lux-blanco); font-family: 'Poppins', sans-serif; overflow-x: hidden; line-height: 1.6; }

        /* HEADER & SISTEMA ANTI-PARPADEO DEL LOGO */
        header {
            background: rgba(0,0,0,0.99);
            width: 100%;
            padding: 1.5rem 8%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--lux-oro);
            position: fixed;
            top: 0;
            z-index: 10000;
            backdrop-filter: blur(25px);
            /* Optimización de Renderizado */
            will-change: transform;
            transform: translateZ(0);
        }
        
        .logo-wrap {
            display: flex;
            align-items: center;
            text-decoration: none;
            gap: 25px;
            /* Evitar saltos de layout */
            min-width: 300px;
        }

        /* Solución Definitiva al Parpadeo del Logo */
        .brand-image { 
            height: 95px; 
            width: auto; 
            display: block; 
            image-rendering: -webkit-optimize-contrast;
            transition: opacity 0.3s ease;
            filter: drop-shadow(0 0 10px rgba(212,175,55,0.1));
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
        }
        
        .brand-text { 
            font-family: 'Playfair Display'; 
            font-size: 3.5rem; 
            color: var(--lux-oro); 
            letter-spacing: 16px; 
            text-transform: uppercase; 
            font-weight: 900;
            user-select: none;
        }

        /* SISTEMA DE NAVEGACIÓN EXTENDIDO */
        .nav-enterprise {
            background: var(--lux-negro-soft);
            padding: 25px 0;
            margin-top: 145px;
            border-bottom: 1px solid var(--lux-gris-mid);
            position: sticky;
            top: 145px;
            z-index: 9999;
            display: flex;
            justify-content: center;
            gap: 30px;
            overflow-x: auto;
            white-space: nowrap;
        }
        .nav-enterprise a {
            color: #666;
            text-decoration: none;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 4px;
            font-weight: 700;
            transition: var(--transition-smooth);
            position: relative;
            padding: 10px 0;
        }
        .nav-enterprise a:hover { color: var(--lux-oro); }
        .nav-enterprise a::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 0;
            height: 2px;
            background: var(--lux-oro);
            transition: var(--transition-smooth);
            transform: translateX(-50%);
        }
        .nav-enterprise a:hover::after { width: 100%; }
        
        .nav-enterprise a.promo-link { 
            color: var(--lux-error); 
            border: 1px solid var(--lux-error); 
            padding: 10px 25px; 
            border-radius: 60px; 
            margin-right: 20px;
            animation: pulse-border 2s infinite;
        }

        @keyframes pulse-border {
            0% { box-shadow: 0 0 0 0 rgba(255, 77, 77, 0.4); }
            70% { box-shadow: 0 0 0 15px rgba(255, 77, 77, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 77, 77, 0); }
        }

        /* WHATSAPP CORPORATIVO */
        .whatsapp-fixed {
            position: fixed;
            bottom: 50px;
            right: 50px;
            background: #25d366;
            color: #fff;
            padding: 25px 45px;
            border-radius: 100px;
            text-decoration: none;
            font-weight: 900;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            gap: 20px;
            z-index: 99999;
            box-shadow: 0 25px 80px rgba(0,0,0,1);
            transition: var(--transition-smooth);
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .whatsapp-fixed:hover { transform: translateY(-20px) scale(1.05); background: #128c7e; box-shadow: 0 40px 100px rgba(37,211,102,0.5); }

        /* HERO - IMPACTO VISUAL */
        .main-hero {
            height: 85vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=2000');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            border-bottom: 5px solid var(--lux-oro);
        }
        .main-hero h1 { font-family: 'Playfair Display'; font-size: 8rem; color: var(--lux-oro); letter-spacing: 30px; margin-bottom: 25px; line-height: 1; text-shadow: 0 20px 50px rgba(0,0,0,1); }
        .main-hero p { font-size: 1.4rem; letter-spacing: 12px; color: #888; font-weight: 200; text-transform: uppercase; }

        /* CONTENIDO Y GRID */
        .section-wrap { padding: 150px 8%; max-width: 1800px; margin: 0 auto; }
        .lux-title { 
            font-family: 'Playfair Display'; 
            font-size: 5rem; 
            color: var(--lux-oro); 
            text-align: center; 
            margin-bottom: 120px; 
            text-transform: uppercase; 
            letter-spacing: 20px; 
            position: relative; 
        }
        .lux-title::after { 
            content: ''; 
            display: block; 
            width: 150px; 
            height: 4px; 
            background: var(--lux-oro); 
            margin: 40px auto; 
            border-radius: 10px;
        }
        .lux-title span { display: block; font-family: 'Poppins'; font-size: 1.2rem; color: #333; letter-spacing: 10px; font-weight: 400; margin-top: 15px; }

        .catalog-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 100px; }
        
        .lux-card { 
            background: var(--lux-gris-dark); 
            border-radius: 60px; 
            border: 1px solid var(--lux-gris-mid); 
            overflow: hidden; 
            transition: var(--transition-smooth); 
            position: relative;
            display: flex;
            flex-direction: column;
        }
        .lux-card:hover { transform: translateY(-50px); border-color: var(--lux-oro); box-shadow: 0 80px 150px rgba(0,0,0,1); }
        
        .visual-display { 
            height: 650px; 
            background: #010101; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 8rem; 
            font-weight: 900; 
            color: #050505; 
            letter-spacing: 50px; 
            position: relative; 
            overflow: hidden;
        }
        .visual-display::before { content: 'LUVIRX'; }
        
        .promo-tag-badge { 
            position: absolute; top: 40px; left: 40px; background: var(--lux-error); 
            color: #fff; padding: 20px 40px; border-radius: 0 30px 0 30px; 
            font-weight: 900; letter-spacing: 4px; z-index: 10; font-size: 1.4rem; 
            box-shadow: 0 10px 30px rgba(255, 77, 77, 0.4);
        }

        .lux-content { padding: 60px; text-align: center; flex-grow: 1; }
        .lux-content h3 { font-size: 2.2rem; letter-spacing: 5px; margin-bottom: 20px; font-weight: 300; }
        .lux-content p { color: #666; margin-bottom: 40px; font-size: 1.1rem; line-height: 1.8; font-weight: 300; }
        
        .price-engine { margin-bottom: 50px; }
        .old-v { color: #333; text-decoration: line-through; font-size: 1.8rem; margin-right: 25px; }
        .new-v { color: var(--lux-oro); font-size: 3.5rem; font-weight: 900; letter-spacing: 2px; }

        .lux-action-btn { 
            background: transparent; border: 3px solid var(--lux-oro); color: var(--lux-oro); 
            padding: 28px 60px; width: 100%; border-radius: 30px; cursor: pointer; 
            text-transform: uppercase; font-weight: 900; letter-spacing: 8px; transition: var(--transition-smooth); font-size: 1.2rem;
        }
        .lux-action-btn:hover { background: var(--lux-oro); color: #000; box-shadow: 0 0 60px var(--lux-oro); transform: scale(1.03); }

        /* ATELIER DE DISEÑO 3D (CÓDIGO EXPANDIDO) */
        .atelier-3d { 
            background: linear-gradient(145deg, #080808, #000); 
            border: 2px solid var(--lux-oro); 
            border-radius: 100px; padding: 180px 15%; margin: 250px 0; 
            text-align: center; position: relative; overflow: hidden;
        }
        .atelier-3d::before {
            content: 'CONCEPT';
            position: absolute;
            left: -100px;
            bottom: -50px;
            font-size: 25rem;
            font-weight: 900;
            color: rgba(212,175,55,0.01);
            pointer-events: none;
        }
        .atelier-3d h2 { font-family: 'Playfair Display'; font-size: 7rem; color: var(--lux-oro); margin-bottom: 60px; line-height: 1; letter-spacing: 15px; }
        .atelier-3d p { font-size: 1.3rem; color: #444; letter-spacing: 8px; text-transform: uppercase; margin-bottom: 80px; }
        
        .studio-textarea { 
            width: 100%; padding: 60px; background: #000; border: 2px solid var(--lux-gris-mid); 
            color: #fff; border-radius: 50px; min-height: 500px; font-size: 1.5rem; 
            margin-bottom: 70px; border-left: 15px solid var(--lux-oro); 
            transition: var(--transition-smooth); font-weight: 200;
        }
        .studio-textarea:focus { border-color: var(--lux-oro); box-shadow: 0 0 50px rgba(212,175,55,0.1); background: #020202; }

        /* SISTEMA DE RECLAMOS GERENCIALES (ULTRA DETALLE) */
        .management-unit { 
            max-width: 1200px; margin: 250px auto; padding: 150px; 
            background: #030303; border-radius: 80px; border-top: 10px solid var(--lux-error); 
            text-align: center; box-shadow: 0 60px 200px rgba(0,0,0,1); 
        }
        .management-unit h2 { font-family: 'Playfair Display'; color: var(--lux-error); font-size: 4.5rem; margin-bottom: 60px; letter-spacing: 10px; }
        .management-unit p { color: #555; margin-bottom: 100px; font-size: 1.1rem; letter-spacing: 4px; }
        
        .field-box { margin-bottom: 50px; text-align: left; }
        .field-box label { color: #333; text-transform: uppercase; letter-spacing: 4px; font-size: 0.9rem; margin-bottom: 25px; display: block; font-weight: 800; }
        .lux-input-v3 { 
            width: 100%; padding: 30px; background: #000; border: 1px solid var(--lux-gris-mid); 
            color: #fff; border-radius: 25px; font-size: 1.3rem; transition: var(--transition-smooth); 
        }
        .lux-input-v3:focus { border-color: var(--lux-error); box-shadow: 0 0 40px rgba(255,77,77,0.1); }

        /* VAULT: MASTER LOGISTICS CONTROL PANEL */
        #admin-vault { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #fff; color: #000; z-index: 1000000; padding: 150px; overflow-y: auto; }
        .vault-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 10px solid #000; padding-bottom: 60px; margin-bottom: 100px; }
        .vault-header h1 { font-family: 'Playfair Display'; font-size: 4.5rem; letter-spacing: 20px; }
        
        .vault-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(600px, 1fr)); gap: 80px; }
        .vault-section { background: #f4f4f4; padding: 60px; border-radius: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.05); }
        .vault-section h3 { font-size: 2.5rem; margin-bottom: 40px; border-bottom: 2px solid #ddd; padding-bottom: 20px; }
        
        .table-lux { width: 100%; border-collapse: collapse; }
        .table-lux th, .table-lux td { padding: 30px; text-align: left; border-bottom: 1px solid #ddd; font-size: 1.1rem; }
        .table-lux th { background: #000; color: #fff; text-transform: uppercase; letter-spacing: 3px; }
        
        footer { padding: 250px 8%; text-align: center; border-top: 1px solid var(--lux-gris-mid); background: #010101; cursor: pointer; }
        footer p { opacity: 0.1; letter-spacing: 20px; font-weight: 900; text-transform: uppercase; font-size: 1.2rem; }
    </style>
</head>
<body>

    <a href="https://wa.me/{{ wsp }}" class="whatsapp-fixed" target="_blank">
        Support Luvirx VIP 💬
    </a>

    <header id="main-header">
        <a href="/" class="logo-wrap">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" class="brand-image" onerror="this.src='https://via.placeholder.com/400x400/000000/d4af37?text=LUVIRX+STYLE';">
            <span class="brand-text">LUVIRX</span>
        </a>
        <div style="display:flex; gap:40px; align-items:center;">
            <button onclick="checkBolsa()" style="background:none; border:3px solid var(--lux-oro); color:var(--lux-oro); padding:22px 55px; border-radius:30px; font-weight:900; cursor:pointer; letter-spacing:6px; font-size:1.2rem; transition: 0.3s;">
                BAG [<span id="cart-count">0</span>]
            </button>
        </div>
    </header>

    <nav class="nav-enterprise">
        <a href="#promociones" class="promo-link">Exclusive Offers</a>
        <a href="#conjuntos">Conjuntos</a>
        <a href="#jeans">Jeans</a>
        <a href="#camisas">Camisas</a>
        <a href="#blusas">Blusas</a>
        <a href="#faldas">Faldas</a>
        <a href="#deportiva">Activewear</a>
        <a href="#atelier-3d" style="color:var(--lux-oro);">3D Studio</a>
        <a href="#claims-center" style="color:var(--lux-error);">Claims</a>
    </nav>

    <div class="main-hero">
        <p>Architects of Luxury Urbanism</p>
        <h1>LUVIRX STYLE</h1>
        <p>GLOBAL OPERATIONS | BOGOTÁ - MILAN - NEW YORK</p>
    </div>

    <div class="section-wrap">
        
        <h2 id="promociones" class="lux-title">Flash Promotions<span>Time-Limited Executive Bundles</span></h2>
        <div class="catalog-grid">
            {% for p in catalog.promociones %}
            <div class="lux-card">
                <div class="promo-tag-badge">{{ p.descuento }}</div>
                <div class="visual-display"></div>
                <div class="lux-content">
                    <h3>{{ p.nombre }}</h3>
                    <p>{{ p.desc }}</p>
                    <div class="price-engine">
                        <span class="old-v">${{ "{:,}".format(p.precio_original) }}</span>
                        <span class="new-v">${{ "{:,}".format(p.precio_oferta) }}</span>
                    </div>
                    <button class="lux-action-btn" onclick="addCart('{{ p.nombre }}', {{ p.precio_oferta }})">Adquirir Promo</button>
                </div>
            </div>
            {% endfor %}
        </div>

        <section id="atelier-3d" class="atelier-3d">
            <h2>3D Custom Atelier</h2>
            <p>DISEÑO PARAMÉTRICO Y ALTA COSTURA DIGITAL A TU MEDIDA.</p>
            <textarea id="design-idea" class="studio-textarea" placeholder="Describe tu concepto maestro: Especifica cortes, materiales (seda, cuero, fibras inteligentes), colores pantone y detalles técnicos para nuestro equipo de ingeniería textil..."></textarea>
            <button class="lux-action-btn" style="background:var(--lux-oro); color:#000;" onclick="submitDesign()">Enviar a Ingeniería de Diseño</button>
        </section>

        {% for category, products in catalog.items() %}
            {% if category != 'promociones' %}
            <h2 id="{{ category }}" class="lux-title">{{ category.upper() }}<span>Premium Luvirx Selection 2026</span></h2>
            <div class="catalog-grid">
                {% for item in products %}
                <div class="lux-card">
                    <div class="visual-display"></div>
                    <div class="lux-content">
                        <h3>{{ item.nombre }}</h3>
                        <p>{{ item.desc }} | Color: <strong>{{ item.color }}</strong></p>
                        <div class="price-engine">
                            <span class="new-v">${{ "{:,}".format(item.precio) }}</span>
                        </div>
                        <button class="lux-action-btn" onclick="addCart('{{ item.nombre }}', {{ item.precio }})">Añadir a Bolsa</button>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        {% endfor %}

        <section id="claims-center" class="management-unit">
            <h2>Claim Management Unit</h2>
            <p>TRATAMIENTO DE INCIDENCIAS CON PRIORIDAD GERENCIAL NIVEL 1.</p>
            <div class="field-box">
                <label>Nombre del Cliente Titular</label>
                <input type="text" id="cl-user-v3" class="lux-input-v3" placeholder="Nombre completo según documento">
            </div>
            <div class="field-box">
                <label>Contacto de Respuesta Inmediata</label>
                <input type="text" id="cl-contact-v3" class="lux-input-v3" placeholder="Móvil o Email de contacto">
            </div>
            <div class="field-box">
                <label>Descripción Técnica del Reclamo</label>
                <textarea id="cl-msg-v3" class="lux-input-v3" style="min-height:350px;" placeholder="Relate los hechos detalladamente..."></textarea>
            </div>
            <button class="lux-action-btn" style="border-color:var(--lux-error); color:var(--lux-error);" onclick="submitClaim()">Radicar Reclamo Oficial</button>
        </section>

    </div>

    <div id="admin-vault">
        <div class="vault-header">
            <h1>LUVIRX MASTER LOGISTICS</h1>
            <button onclick="closeVault()" class="lux-action-btn" style="width:auto; padding:20px 60px;">LOGOUT SYSTEM</button>
        </div>
        <div class="vault-grid" id="vault-data-render">
            </div>
    </div>

    <footer onclick="openVault()">
        <p>&copy; 2026 LUVIRX STYLE | LUXURY GROUP HOLDING | MASTER CONTROL SYSTEM</p>
    </footer>

    <script>
        let cartItems = []; let cartTotal = 0;

        function addCart(n, p) {
            cartItems.push(n);
            cartTotal += p;
            document.getElementById('cart-count').innerText = cartItems.length;
            console.log(`[SYSTEM] Item added: ${n} | New Total: ${cartTotal}`);
        }

        async function checkBolsa() {
            if(cartItems.length === 0) return alert("LA BOLSA DE COMPRAS SE ENCUENTRA VACÍA.");
            const nom = prompt("NOMBRE COMPLETO PARA FACTURACIÓN:");
            const dir = prompt("DIRECCIÓN DE DESPACHO INTERNACIONAL:");
            if(!nom || !dir) return;
            
            const pedidoObj = { cliente: nom, direccion: dir, articulos: cartItems.join(", "), total: cartTotal, fecha: new Date().toLocaleString() };
            
            await fetch('/api/v3/pedido', { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify(pedidoObj) 
            });

            window.open(`https://wa.me/{{ wsp }}?text=LUVIRX STYLE - ORDEN DE COMPRA CONFIRMADA%0ACliente: ${nom}%0AItems: ${pedidoObj.articulos}%0ATotal: $${cartTotal}%0ADirección: ${dir}`);
            location.reload();
        }

        async function submitDesign() {
            const idea = document.getElementById('design-idea').value;
            if(!idea) return alert("POR FAVOR DESCRIBA SU CONCEPTO TÉCNICO.");
            
            await fetch('/api/v3/design', { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify({ idea: idea, fecha: new Date().toLocaleString() }) 
            });

            window.open(`https://wa.me/{{ wsp }}?text=LUVIRX STYLE - SOLICITUD DE DISEÑO 3D%0ADetalle: ${idea}`);
            alert("PROPUESTA ENVIADA AL DEPARTAMENTO DE INGENIERÍA TEXTIL.");
            location.reload();
        }

        async function submitClaim() {
            const nom = document.getElementById('cl-user-v3').value;
            const con = document.getElementById('cl-contact-v3').value;
            const msg = document.getElementById('cl-msg-v3').value;
            
            if(!nom || !msg) return alert("INFORMACIÓN INSUFICIENTE PARA RADICAR EL RECLAMO.");
            
            const claimObj = { nombre: nom, contacto: con, mensaje: msg, fecha: new Date().toLocaleString() };
            
            await fetch('/api/v3/claim', { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify(claimObj) 
            });

            window.open(`https://wa.me/{{ wsp }}?text=URGENTE - RECLAMO ESCALADO LUVIRX STYLE%0ACliente: ${nom}%0AMensaje: ${msg}`);
            alert("RECLAMO RADICADO BAJO SUPERVISIÓN GERENCIAL.");
            location.reload();
        }

        function openVault() {
            if(prompt("CÓDIGO DE ENCRIPTACIÓN DE ACCESO (NIVEL 5):") === "{{ pin }}") {
                document.getElementById('admin-vault').style.display = 'block';
                renderVaultData();
            }
        }

        function closeVault() { document.getElementById('admin-vault').style.display = 'none'; }

        async function renderVaultData() {
            const response = await fetch('/api/v3/data');
            const d = await response.json();
            
            let html = `
                <div class="vault-section">
                    <h3>Registro de Ventas</h3>
                    <table class="table-lux">
                        <tr><th>Fecha</th><th>Cliente</th><th>Total</th></tr>
                        ${d.ventas_realizadas.map(v => `<tr><td>${v.fecha}</td><td>${v.cliente}</td><td>$${v.total}</td></tr>`).join('')}
                    </table>
                </div>
                <div class="vault-section">
                    <h3>Propuestas de Diseño</h3>
                    <table class="table-lux">
                        <tr><th>Fecha</th><th>Concepto</th></tr>
                        ${d.disenos_solicitados.map(ds => `<tr><td>${ds.fecha}</td><td>${ds.idea}</td></tr>`).join('')}
                    </table>
                </div>
                <div class="vault-section" style="grid-column: span 2;">
                    <h3 style="color:red;">Incidentes y Reclamos</h3>
                    <table class="table-lux">
                        <tr><th>Fecha</th><th>Cliente</th><th>Mensaje</th></tr>
                        ${d.quejas_clientes.map(q => `<tr><td>${q.fecha}</td><td>${q.nombre} (${q.contacto})</td><td>${q.mensaje}</td></tr>`).join('')}
                    </table>
                </div>
            `;
            document.getElementById('vault-data-render').innerHTML = html;
        }
    </script>
</body>
</html>
"""

# ==============================================================================
# RUTAS DE SERVIDOR (LOGICA DE BACKEND ROBUSTA)
# ==============================================================================
@app.route('/')
def main_platform():
    # Auditoría de acceso
    storage_system["analitica_ventas"]["logs_sistema"].append(f"Acceso detectado: {datetime.datetime.now()}")
    return render_template_string(HTML_PLATFORM_V3, 
                                  catalog=MASTER_CATALOG, 
                                  wsp=WSP_OFFICIAL, 
                                  pin=ADMIN_PIN_ACCESS)

@app.route('/api/v3/pedido', methods=['POST'])
def handle_pedido():
    data = request.json
    storage_system["ventas_realizadas"].append(data)
    storage_system["analitica_ventas"]["total_recaudado"] += data["total"]
    storage_system["analitica_ventas"]["conteo_pedidos"] += 1
    return jsonify({"status": "Success", "code": 200})

@app.route('/api/v3/design', methods=['POST'])
def handle_design():
    storage_system["disenos_solicitados"].append(request.json)
    return jsonify({"status": "Stored", "code": 200})

@app.route('/api/v3/claim', methods=['POST'])
def handle_claim():
    storage_system["quejas_clientes"].append(request.json)
    return jsonify({"status": "Logged", "code": 200})

@app.route('/api/v3/data')
def get_system_data():
    return jsonify(storage_system)

# ==============================================================================
# INICIO DE OPERACIONES
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True)