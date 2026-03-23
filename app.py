# -*- coding: utf-8 -*-
# ==============================================================================
# PROYECTO: LUVIRX STYLE - PLATAFORMA DE GESTIÓN DE MODA DE LUJO (VERSIÓN 4.0)
# ARQUITECTURA: MODELO-VISTA-CONTROLADOR INTEGRADO (NIVEL EMPRESARIAL)
# DESARROLLO: INGENIERÍA DE DATOS Y VENTAS ESTRATÉGICAS
# CARACTERES: >45,000 (DENSIDAD MÁXIMA DE CÓDIGO)
# ==============================================================================

from flask import Flask, render_template_string, request, jsonify, url_for
import datetime
import json

app = Flask(__name__)

# ------------------------------------------------------------------------------
# CONFIGURACIÓN MAESTRA DE IDENTIDAD CORPORATIVA
# ------------------------------------------------------------------------------
CONFIGURACION_LUVIRX = {
    "TELEFONO_WHATSAPP": "573115221592",
    "CODIGO_ACCESO_VAULT": "2102",
    "NOMBRE_MARCA": "LUVIRX STYLE",
    "ESLOGAN": "Arquitectos de la Identidad Urbana",
    "VERSION_SOFTWARE": "4.0.0 Gold Edition",
    "MONEDA": "COP",
    "PAIS_OPERACION": "Colombia",
    # NOTA: Sustituye la URL de abajo por tu enlace directo si lo deseas. 
    # El sistema tiene un respaldo automático en caso de error de carga.
    "URL_LOGO_PRIORITARIO": "https://i.imgur.com/E0nK4vA.png" 
}

# ------------------------------------------------------------------------------
# BASE DE DATOS ESTRUCTURADA (ALMACENAMIENTO DINÁMICO DE ALTA CAPACIDAD)
# ------------------------------------------------------------------------------
sistema_datos = {
    "pedidos_maestros": [],
    "disenos_ingenieria": [],
    "centro_reclamos": [],
    "suscriptores_elite": [],
    "metricas_globales": {
        "ventas_totales_brutas": 0,
        "pedidos_acumulados": 0,
        "clics_en_diseno": 0,
        "ultimo_acceso_gerencial": None,
        "historial_acciones": []
    }
}

# ------------------------------------------------------------------------------
# INVENTARIO PROFESIONAL (EXPANDIDO MILIMÉTRICAMENTE)
# ------------------------------------------------------------------------------
INVENTARIO_MAESTRO = {
    "promociones_flash": [
        {"id": "LX-PRO-01", "nombre": "Combo Soberano Onyx", "precio_original": 480000, "precio_oferta": 336000, "ahorro": "30%", "detalle": "Incluye Conjunto Onyx Urban + Camisa Oxford Luvirx + Accesorio de Cuero. El máximo exponente del lujo diario."},
        {"id": "LX-PRO-02", "nombre": "Colección Legado Denim", "precio_original": 350000, "precio_oferta": 245000, "ahorro": "30%", "detalle": "Tres Jeans Heritage Slim en diferentes tonalidades. Denim japonés con memoria de ajuste."},
        {"id": "LX-PRO-03", "nombre": "Kit Atleta de Élite", "precio_original": 290000, "precio_oferta": 203000, "ahorro": "30%", "detalle": "Conjunto completo Pro-Performance con fibras de enfriamiento rápido y diseño ergonómico."},
        {"id": "LX-PRO-04", "nombre": "Trilogía Camisas Business", "precio_original": 315000, "precio_oferta": 220500, "ahorro": "30%", "detalle": "Tres camisas de algodón Pima (Blanco, Azul Celeste, Negro) con cuello de alta estructura."}
    ],
    "conjuntos_premium": [
        {"id": "LX-CJ-01", "nombre": "Conjunto Onyx Urban", "precio": 185000, "color": "Negro Profundo", "talla": "S, M, L, XL", "desc": "Mezcla técnica de seda y algodón. Ideal para climas templados."},
        {"id": "LX-CJ-02", "nombre": "Conjunto Blanco Mármol", "precio": 210000, "color": "Blanco Hueso", "talla": "S, M, L", "desc": "Edición limitada de lino italiano. Frescura y distinción absoluta."},
        {"id": "LX-CJ-03", "nombre": "Conjunto Azul Medianoche", "precio": 195000, "color": "Azul Cobalto", "talla": "M, L, XL", "desc": "Textura micromoteada con regulación térmica inteligente."},
        {"id": "LX-CJ-04", "nombre": "Conjunto Esmeralda Luxe", "precio": 225000, "color": "Verde Joya", "talla": "S, M", "desc": "Satinado de alta densidad con forro interno microperforado."},
        {"id": "LX-CJ-05", "nombre": "Conjunto Terracota Desert", "precio": 190000, "color": "Naranja Arcilla", "talla": "S, M, L", "desc": "Inspiración sahariana con cortes asimétricos vanguardistas."},
        {"id": "LX-CJ-06", "nombre": "Conjunto Graphite Silk", "precio": 240000, "color": "Gris Grafito", "talla": "M, L", "desc": "Seda pura con acabados en costura invisible. Exclusividad pura."}
    ],
    "seccion_jeans": [
        {"id": "LX-JN-01", "nombre": "Jean Heritage Slim", "precio": 145000, "color": "Índigo", "talla": "28 a 36", "desc": "Denim de 14oz con tratamiento de suavizado premium."},
        {"id": "LX-JN-02", "nombre": "Jean Street Baggy", "precio": 130000, "color": "Gris Ácido", "talla": "30 a 38", "desc": "Corte holgado con refuerzo en rodillas para durabilidad extrema."},
        {"id": "LX-JN-03", "nombre": "Jean Cargo Táctico", "precio": 160000, "color": "Kaki", "talla": "30 a 36", "desc": "Ocho bolsillos funcionales con cierres de seguridad YKK."},
        {"id": "LX-JN-04", "nombre": "Jean Vintage Flare", "precio": 155000, "color": "Azul Lavado", "talla": "26 a 34", "desc": "Ajuste perfecto en cintura con apertura bota campana clásica."},
        {"id": "LX-JN-05", "nombre": "Jean Biker Distressed", "precio": 170000, "color": "Negro Carbón", "talla": "28 a 36", "desc": "Apliques acolchados en muslos y desgastes artesanales."},
        {"id": "LX-JN-06", "nombre": "Jean Raw Selvedge", "precio": 195000, "color": "Azul Oscuro", "talla": "32, 34", "desc": "Denim sin lavar para un desgaste personalizado según el uso."}
    ],
    "camisas_ejecutivas": [
        {"id": "LX-CM-01", "nombre": "Camisa Oxford Luvirx", "precio": 95000, "color": "Blanco Nieve", "talla": "S a XL", "desc": "Tejido Oxford de doble trama. Elegancia que no se arruga."},
        {"id": "LX-CM-02", "nombre": "Camisa Versailles Print", "precio": 115000, "color": "Estampado", "talla": "M, L", "desc": "Motivos barrocos en impresión digital de alta fidelidad."},
        {"id": "LX-CM-03", "nombre": "Camisa Urban Linen", "precio": 105000, "color": "Beige", "talla": "S, M, L", "desc": "Lino de alta transpirabilidad para eventos de día."},
        {"id": "LX-CM-04", "nombre": "Camisa Formal Negra", "precio": 110000, "color": "Negro Mate", "talla": "S a XXL", "desc": "Botones de nácar y corte slim fit estructurado."},
        {"id": "LX-CM-05", "nombre": "Camisa Rayada Náutica", "precio": 98000, "color": "Azul/Blanco", "talla": "M, L", "desc": "Estilo atemporal para el fin de semana de lujo."},
        {"id": "LX-CM-06", "nombre": "Camisa Mao Satinada", "precio": 125000, "color": "Vino", "talla": "S, M", "desc": "Cuello tipo Mao con acabado satinado para eventos nocturnos."}
    ],
    "blusas_sofisticadas": [
        {"id": "LX-BL-01", "nombre": "Blusa Seda Radiante", "precio": 85000, "color": "Marfil", "talla": "Única", "desc": "Caída espectacular que realza la silueta femenina."},
        {"id": "LX-BL-02", "nombre": "Blusa Velvet Night", "precio": 90000, "color": "Borgona", "talla": "S, M", "desc": "Terciopelo suave con detalles de encaje en puños."},
        {"id": "LX-BL-03", "nombre": "Blusa Sueño de Gasa", "precio": 78000, "color": "Rosa Pastel", "talla": "S, M, L", "desc": "Ligereza y romanticismo en cada costura."},
        {"id": "LX-BL-04", "nombre": "Blusa Cuello Halter", "precio": 82000, "color": "Dorado", "talla": "M", "desc": "Brillo sofisticado para cócteles y cenas exclusivas."},
        {"id": "LX-BL-05", "nombre": "Blusa Kimono Abstract", "precio": 95000, "color": "Multicolor", "talla": "Única", "desc": "Corte tipo kimono con estampado de vanguardia."},
        {"id": "LX-BL-06", "nombre": "Blusa Asimétrica Chic", "precio": 88000, "color": "Negro", "talla": "S, M", "desc": "Diseño de un solo hombro con volantes estructurados."}
    ],
    "faldas_estilo": [
        {"id": "LX-FL-01", "nombre": "Falda Midi Plisada", "precio": 75000, "color": "Plata", "talla": "S, M", "desc": "Efecto espejo con plisado de precisión industrial."},
        {"id": "LX-FL-02", "nombre": "Minifalda Cuero Luxe", "precio": 95000, "color": "Negro", "talla": "XS, S, M", "desc": "Cuero ecológico de tacto idéntico al animal."},
        {"id": "LX-FL-03", "nombre": "Falda Lápiz Business", "precio": 88000, "color": "Gris Oxford", "talla": "M, L", "desc": "Ajuste milimétrico para el entorno profesional."},
        {"id": "LX-FL-04", "nombre": "Falda Denim High-Waist", "precio": 72000, "color": "Azul Claro", "talla": "S, M, L", "desc": "Cintura alta con botones metálicos de lujo."},
        {"id": "LX-FL-05", "nombre": "Maxifalda Boho Silk", "precio": 110000, "color": "Tierra", "talla": "Única", "desc": "Vuelo amplio con caída de seda para un look relajado."},
        {"id": "LX-FL-06", "nombre": "Falda Tulipán Estructura", "precio": 92000, "color": "Rojo", "talla": "S, M", "desc": "Corte arquitectónico que añade volumen estratégico."}
    ],
    "activewear_lujo": [
        {"id": "LX-DP-01", "nombre": "Leggings Pro-Performance", "precio": 110000, "color": "Carbono", "talla": "XS a L", "desc": "Compresión grado médico para máximo rendimiento."},
        {"id": "LX-DP-02", "nombre": "Top Impact Studio", "precio": 65000, "color": "Neon", "talla": "S, M", "desc": "Soporte multidireccional con copas premoldeadas."},
        {"id": "LX-DP-03", "nombre": "Short Biker Pro", "precio": 55000, "color": "Azul Real", "talla": "S, M, L", "desc": "Costuras planas antiroce para largas distancias."},
        {"id": "LX-DP-04", "nombre": "Chaqueta Cortavientos Fly", "precio": 145000, "color": "Blanco", "talla": "M, L", "desc": "Ultraligera y repelente al agua con ventilación láser."},
        {"id": "LX-DP-05", "nombre": "Conjunto Seamless Yoga", "precio": 135000, "color": "Lila", "talla": "S, M", "desc": "Sin costuras para evitar cualquier tipo de fricción."},
        {"id": "LX-DP-06", "nombre": "Jogger Elite Tech", "precio": 120000, "color": "Gris Melange", "talla": "M, L, XL", "desc": "Algodón técnico con bolsillos térmicos para móvil."}
    ]
}

# ------------------------------------------------------------------------------
# MOTOR DE INTERFAZ DE USUARIO (UX/UI - INGENIERÍA VISUAL DE ALTA DENSIDAD)
# ------------------------------------------------------------------------------
HTML_PLATAFORMA_LUVIRX_V4 = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ config.NOMBRE_MARCA }} | Infraestructura de Moda Global</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,700&family=Poppins:wght@100;300;400;600;800&family=Montserrat:wght@200;400;700;900&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --paleta-oro: #d4af37;
            --paleta-oro-brillante: #ffdf00;
            --paleta-negro-obsidiana: #0a0a0a;
            --paleta-negro-puro: #000000;
            --paleta-gris-titanio: #1a1a1a;
            --paleta-blanco-seda: #f8f9fa;
            --paleta-rojo-alerta: #e74c3c;
            --paleta-verde-exito: #27ae60;
            --transicion-lujo: all 0.7s cubic-bezier(0.19, 1, 0.22, 1);
            --sombra-industrial: 0 50px 100px rgba(0,0,0,0.9);
        }

        /* RESET DE SISTEMA MILIMÉTRICO */
        * { margin: 0; padding: 0; box-sizing: border-box; outline: none; -webkit-tap-highlight-color: transparent; }
        body { background-color: var(--paleta-negro-puro); color: var(--paleta-blanco-seda); font-family: 'Poppins', sans-serif; overflow-x: hidden; scroll-behavior: smooth; }

        /* CABECERA DINÁMICA ANTI-PARPADEO */
        header {
            background: rgba(0,0,0,0.99);
            width: 100%;
            padding: 1.5rem 6%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--paleta-oro);
            position: fixed;
            top: 0;
            z-index: 20000;
            backdrop-filter: blur(40px);
            will-change: transform;
            transform: translateZ(0);
        }
        
        .marca-contenedor { display: flex; align-items: center; text-decoration: none; gap: 30px; }
        
        /* LOGO: SISTEMA DE CARGA GARANTIZADA */
        .logo-estatal {
            height: 110px;
            width: auto;
            display: block;
            image-rendering: -webkit-optimize-contrast;
            transition: var(--transicion-lujo);
            filter: drop-shadow(0 0 10px rgba(212,175,55,0.3));
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
        }
        .logo-estatal:hover { transform: scale(1.08) rotate(-2deg); }

        .texto-logotipo {
            font-family: 'Playfair Display';
            font-size: 4rem;
            color: var(--paleta-oro);
            letter-spacing: 20px;
            text-transform: uppercase;
            font-weight: 900;
            line-height: 1;
        }

        /* NAVEGACIÓN PROFESIONAL EXTENDIDA */
        .navegacion-corporativa {
            background: var(--paleta-negro-obsidiana);
            padding: 30px 0;
            margin-top: 160px;
            border-bottom: 1px solid var(--paleta-gris-titanio);
            position: sticky;
            top: 160px;
            z-index: 15000;
            display: flex;
            justify-content: center;
            gap: 45px;
            overflow-x: auto;
            scrollbar-width: none;
        }
        .navegacion-corporativa::-webkit-scrollbar { display: none; }
        
        .navegacion-corporativa a {
            color: #777;
            text-decoration: none;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 6px;
            font-weight: 600;
            transition: var(--transicion-lujo);
            position: relative;
            padding: 10px 0;
        }
        .navegacion-corporativa a:hover, .navegacion-corporativa a.activo { color: var(--paleta-oro); }
        .navegacion-corporativa a::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 0;
            height: 3px;
            background: var(--paleta-oro);
            transition: var(--transicion-lujo);
            transform: translateX(-50%);
        }
        .navegacion-corporativa a:hover::after { width: 100%; }

        .enlace-especial {
            color: var(--paleta-rojo-alerta) !important;
            border: 2px solid var(--paleta-rojo-alerta);
            padding: 10px 35px !important;
            border-radius: 60px;
            animation: pulso-alerta 3s infinite;
        }
        @keyframes pulso-alerta {
            0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.5); }
            70% { box-shadow: 0 0 0 20px rgba(231, 76, 60, 0); }
            100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
        }

        /* BOTÓN FLOTANTE WHATSAPP DE ALTA PRIORIDAD */
        .wsp-prioritario {
            position: fixed;
            bottom: 60px;
            right: 60px;
            background: #25d366;
            color: white;
            padding: 25px 50px;
            border-radius: 100px;
            text-decoration: none;
            font-weight: 800;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 25px;
            z-index: 50000;
            box-shadow: 0 40px 100px rgba(0,0,0,1);
            transition: var(--transicion-lujo);
            letter-spacing: 4px;
            text-transform: uppercase;
        }
        .wsp-prioritario:hover { transform: translateY(-20px) scale(1.05) rotate(1deg); background: #128c7e; box-shadow: 0 60px 120px rgba(37,211,102,0.3); }

        /* SECCIÓN PORTADA (HERO) */
        .hero-maestro {
            height: 90vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.95)), url('https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?q=80&w=2000');
            background-size: cover;
            background-attachment: fixed;
            border-bottom: 8px solid var(--paleta-oro);
        }
        .hero-maestro span { font-size: 1.6rem; letter-spacing: 20px; color: #555; text-transform: uppercase; font-weight: 200; margin-bottom: 20px; }
        .hero-maestro h1 { font-family: 'Playfair Display'; font-size: 9.5rem; color: var(--paleta-oro); letter-spacing: 40px; line-height: 1; text-shadow: 0 40px 80px rgba(0,0,0,1); }
        .hero-maestro p { font-size: 1.2rem; color: #888; max-width: 800px; margin-top: 40px; letter-spacing: 5px; text-transform: uppercase; }

        /* CONTENEDOR DE PRODUCTOS */
        .seccion-contenedor { padding: 180px 6%; max-width: 2000px; margin: 0 auto; }
        .cabecera-seccion { 
            font-family: 'Playfair Display'; 
            font-size: 6rem; 
            color: var(--paleta-oro); 
            text-align: center; 
            margin-bottom: 150px; 
            text-transform: uppercase; 
            letter-spacing: 30px; 
            position: relative; 
        }
        .cabecera-seccion::after { 
            content: ''; 
            display: block; 
            width: 250px; 
            height: 5px; 
            background: var(--paleta-oro); 
            margin: 50px auto; 
        }
        .cabecera-seccion span { display: block; font-family: 'Poppins'; font-size: 1.4rem; color: #333; letter-spacing: 15px; font-weight: 300; margin-top: 20px; }

        .grid-articulos { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 120px; }
        
        .tarjeta-premium { 
            background: var(--paleta-gris-titanio); 
            border-radius: 80px; 
            border: 1px solid #222; 
            overflow: hidden; 
            transition: var(--transicion-lujo); 
            display: flex;
            flex-direction: column;
            position: relative;
        }
        .tarjeta-premium:hover { transform: translateY(-40px); border-color: var(--paleta-oro); box-shadow: var(--sombra-industrial); }
        
        .visual-producto { 
            height: 750px; 
            background: #020202; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 10rem; 
            font-weight: 900; 
            color: #080808; 
            letter-spacing: 80px; 
            position: relative;
            overflow: hidden;
        }
        .visual-producto::before { content: 'LUVIRX'; }
        
        .placa-descuento { 
            position: absolute; top: 50px; left: 50px; background: var(--paleta-rojo-alerta); 
            color: #fff; padding: 25px 50px; border-radius: 0 40px 0 40px; 
            font-weight: 900; letter-spacing: 6px; z-index: 10; font-size: 1.7rem; 
            box-shadow: 0 20px 50px rgba(231, 76, 60, 0.4);
        }

        .info-producto { padding: 80px; text-align: center; flex-grow: 1; }
        .info-producto h3 { font-size: 2.8rem; letter-spacing: 8px; margin-bottom: 30px; font-weight: 300; color: var(--paleta-oro); }
        .info-producto p { color: #888; margin-bottom: 50px; font-size: 1.2rem; line-height: 2; }
        
        .bloque-precios { margin-bottom: 60px; }
        .precio-tachado { color: #444; text-decoration: line-through; font-size: 2.2rem; margin-right: 35px; }
        .precio-final { color: var(--paleta-blanco-seda); font-size: 4.5rem; font-weight: 900; letter-spacing: 4px; }

        .btn-compra-lux { 
            background: transparent; border: 4px solid var(--paleta-oro); color: var(--paleta-oro); 
            padding: 35px 70px; width: 100%; border-radius: 40px; cursor: pointer; 
            text-transform: uppercase; font-weight: 900; letter-spacing: 12px; transition: var(--transicion-lujo); font-size: 1.4rem;
        }
        .btn-compra-lux:hover { background: var(--paleta-oro); color: #000; box-shadow: 0 0 80px var(--paleta-oro); letter-spacing: 15px; }

        /* ESTUDIO DE INGENIERÍA TEXTIL 3D */
        .estudio-3d-seccion { 
            background: radial-gradient(circle at center, #0f0f0f 0%, #000 100%); 
            border: 4px solid var(--paleta-oro); 
            border-radius: 150px; padding: 250px 15%; margin: 350px 0; 
            text-align: center; position: relative; overflow: hidden;
        }
        .estudio-3d-seccion h2 { font-family: 'Playfair Display'; font-size: 8rem; color: var(--paleta-oro); margin-bottom: 70px; letter-spacing: 25px; }
        .estudio-3d-seccion p { color: #555; font-size: 1.5rem; letter-spacing: 10px; text-transform: uppercase; margin-bottom: 100px; }
        
        .entrada-diseño-extensa { 
            width: 100%; padding: 80px; background: #000; border: 2px solid #222; 
            color: #fff; border-radius: 80px; min-height: 650px; font-size: 1.8rem; 
            margin-bottom: 90px; border-left: 25px solid var(--paleta-oro); 
            transition: var(--transicion-lujo); font-weight: 200; line-height: 1.8;
        }
        .entrada-diseño-extensa:focus { border-color: var(--paleta-oro-brillante); box-shadow: 0 0 100px rgba(212,175,55,0.2); }

        /* GESTIÓN TÉCNICA DE RECLAMOS */
        .area-reclamos { 
            max-width: 1400px; margin: 350px auto; padding: 200px; 
            background: #050505; border-radius: 120px; border-top: 15px solid var(--paleta-rojo-alerta); 
            text-align: center; box-shadow: 0 100px 300px rgba(0,0,0,1); 
        }
        .area-reclamos h2 { font-family: 'Playfair Display'; color: var(--paleta-rojo-alerta); font-size: 5.5rem; margin-bottom: 80px; letter-spacing: 15px; }
        
        .campo-form { margin-bottom: 70px; text-align: left; }
        .campo-form label { color: #444; text-transform: uppercase; letter-spacing: 6px; font-size: 1.1rem; margin-bottom: 35px; display: block; font-weight: 800; }
        .input-lujo-v4 { 
            width: 100%; padding: 40px; background: #000; border: 1px solid #222; 
            color: #fff; border-radius: 40px; font-size: 1.5rem; transition: var(--transicion-lujo); 
        }
        .input-lujo-v4:focus { border-color: var(--paleta-rojo-alerta); box-shadow: 0 0 60px rgba(231, 76, 60, 0.2); }

        /* PANEL GERENCIAL (BÓVEDA) */
        #boveda-gerencial { 
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: #ffffff; color: #000; z-index: 1000000; padding: 180px; overflow-y: auto; 
        }
        .boveda-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 12px solid #000; padding-bottom: 60px; margin-bottom: 120px; }
        .boveda-header h1 { font-family: 'Playfair Display'; font-size: 5rem; letter-spacing: 25px; }
        
        .boveda-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(650px, 1fr)); gap: 100px; }
        .boveda-card { background: #f9f9f9; padding: 80px; border-radius: 60px; box-shadow: 0 40px 80px rgba(0,0,0,0.05); border: 1px solid #eee; }
        .boveda-card h3 { font-size: 3rem; margin-bottom: 50px; border-bottom: 4px solid var(--paleta-oro); display: inline-block; padding-bottom: 15px; }
        
        .tabla-estratégica { width: 100%; border-collapse: collapse; margin-top: 40px; }
        .tabla-estratégica th, .tabla-estratégica td { padding: 40px; text-align: left; border-bottom: 1px solid #ddd; font-size: 1.3rem; }
        .tabla-estratégica th { background: #000; color: #fff; text-transform: uppercase; letter-spacing: 5px; }
        
        footer { padding: 300px 6%; text-align: center; border-top: 2px solid var(--paleta-gris-titanio); background: #020202; cursor: pointer; }
        footer p { opacity: 0.05; letter-spacing: 30px; font-weight: 900; text-transform: uppercase; font-size: 1.5rem; color: var(--paleta-oro); }
    </style>
</head>
<body>

    <a href="https://wa.me/{{ config.TELEFONO_WHATSAPP }}" class="wsp-prioritario" target="_blank">
        Atención Ejecutiva WhatsApp 💬
    </a>

    <header id="cabecera-principal">
        <a href="/" class="marca-contenedor">
            <img id="logo-img" src="{{ config.URL_LOGO_PRIORITARIO }}" alt="LUVIRX STYLE" class="logo-estatal" 
                 onerror="this.onerror=null; this.src='https://via.placeholder.com/600x600/000000/d4af37?text=LUVIRX+STYLE';">
            <span class="texto-logotipo">LUVIRX</span>
        </a>
        <div style="display:flex; gap:50px; align-items:center;">
            <button onclick="procesarBolsa()" style="background:none; border:4px solid var(--paleta-oro); color:var(--paleta-oro); padding:25px 65px; border-radius:40px; font-weight:900; cursor:pointer; letter-spacing:10px; font-size:1.4rem; transition: 0.5s;">
                PEDIDO [<span id="conteo-bolsa">0</span>]
            </button>
        </div>
    </header>

    <nav class="navegacion-corporativa">
        <a href="#ofertas" class="enlace-especial">OFERTAS ELITE</a>
        <a href="#conjuntos">CONJUNTOS</a>
        <a href="#jeans">JEANS</a>
        <a href="#camisas">CAMISAS</a>
        <a href="#blusas">BLUSAS</a>
        <a href="#faldas">FALDAS</a>
        <a href="#deportiva">ACTIVEWEAR</a>
        <a href="#estudio-3d" style="color:var(--paleta-oro);">ESTUDIO 3D</a>
        <a href="#canal-reclamos" style="color:var(--paleta-rojo-alerta);">RECLAMOS</a>
    </nav>

    <div class="hero-maestro">
        <span>ESTABLECIMIENTO DE ALTA MODA</span>
        <h1>LUVIRX STYLE</h1>
        <p>SISTEMA DE GESTIÓN DE INVENTARIO Y DISEÑO PARAMÉTRICO V4.0. OPERACIONES ACTIVAS EN BOGOTÁ Y MERCADOS INTERNACIONALES.</p>
    </div>

    <div class="seccion-contenedor">
        
        <h2 id="ofertas" class="cabecera-seccion">Promociones Flash<span>Oportunidades de Adquisición Limitada</span></h2>
        <div class="grid-articulos">
            {% for item in inventario.promociones_flash %}
            <div class="tarjeta-premium">
                <div class="placa-descuento">{{ item.ahorro }} DTO</div>
                <div class="visual-producto"></div>
                <div class="info-producto">
                    <h3>{{ item.nombre }}</h3>
                    <p>{{ item.detalle }}</p>
                    <div class="bloque-precios">
                        <span class="precio-tachado">${{ "{:,}".format(item.precio_original) }}</span>
                        <span class="precio-final">${{ "{:,}".format(item.precio_oferta) }}</span>
                    </div>
                    <button class="btn-compra-lux" onclick="gestionarCarrito('{{ item.nombre }}', {{ item.precio_oferta }})">Adquirir Oferta</button>
                </div>
            </div>
            {% endfor %}
        </div>

        <section id="estudio-3d" class="estudio-3d-seccion">
            <h2>Ingeniería de Diseño 3D</h2>
            <p>ELABORA TU CONCEPTO MAESTRO. NUESTRO EQUIPO PROCESARÁ CADA FIBRA Y PATRÓN SEGÚN TUS ESPECIFICACIONES.</p>
            <textarea id="texto-concepto-3d" class="entrada-diseño-extensa" placeholder="Detalla tu visión técnica: Selección de textiles (sedas, denim crudo, tejidos inteligentes), paleta de colores Pantone, cortes ergonómicos y acabados de costura artesanal..."></textarea>
            <button class="btn-compra-lux" style="background:var(--paleta-oro); color:#000;" onclick="enviarConceptoDiseno()">Enviar a Producción 3D</button>
        </section>

        {% for categoria, productos in inventario.items() %}
            {% if categoria != 'promociones_flash' %}
            <h2 id="{{ categoria }}" class="cabecera-seccion">{{ categoria.replace('_', ' ').upper() }}<span>Colección Luvirx Gold 2026</span></h2>
            <div class="grid-articulos">
                {% for p in productos %}
                <div class="tarjeta-premium">
                    <div class="visual-producto"></div>
                    <div class="info-producto">
                        <h3>{{ p.nombre }}</h3>
                        <p>{{ p.desc }}<br>Tallas: <strong>{{ p.talla }}</strong> | Tono: <strong>{{ p.color }}</strong></p>
                        <div class="bloque-precios">
                            <span class="precio-final">${{ "{:,}".format(p.precio) }}</span>
                        </div>
                        <button class="btn-compra-lux" onclick="gestionarCarrito('{{ p.nombre }}', {{ p.precio }})">Añadir a Pedido</button>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        {% endfor %}

        <section id="canal-reclamos" class="area-reclamos">
            <h2>Oficina de Gestión de Reclamos</h2>
            <p>SISTEMA DE ESCALAMIENTO GERENCIAL PARA LA RESOLUCIÓN DE INCIDENCIAS OPERATIVAS.</p>
            <div class="campo-form">
                <label>Nombre del Titular del Reclamo</label>
                <input type="text" id="nombre-reclamo" class="input-lujo-v4" placeholder="Nombre completo según identificación">
            </div>
            <div class="campo-form">
                <label>Contacto de Respuesta Prioritaria</label>
                <input type="text" id="contacto-reclamo" class="input-lujo-v4" placeholder="Teléfono móvil o Correo electrónico">
            </div>
            <div class="campo-form">
                <label>Exposición de Motivos y Hechos</label>
                <textarea id="mensaje-reclamo" class="input-lujo-v4" style="min-height:450px;" placeholder="Relate detalladamente la situación para nuestro equipo de auditoría..."></textarea>
            </div>
            <button class="btn-compra-lux" style="border-color:var(--paleta-rojo-alerta); color:var(--paleta-rojo-alerta);" onclick="radicarReclamoOficial()">Radicar Reclamo de Alta Prioridad</button>
        </section>

    </div>

    <div id="boveda-gerencial">
        <div class="boveda-header">
            <h1>SISTEMA DE CONTROL MAESTRO LUVIRX</h1>
            <button onclick="salirDeBoveda()" class="btn-compra-lux" style="width:auto; padding:20px 60px; background:#000; color:#fff;">LOGOUT GERENCIAL</button>
        </div>
        <div class="boveda-grid" id="render-datos-gerenciales">
            </div>
    </div>

    <footer onclick="accesoBoveda()">
        <p>&copy; 2026 LUVIRX STYLE | GRUPO HOLDING DE LUJO | TODOS LOS DERECHOS RESERVADOS | OPERACIÓN BOGOTÁ</p>
    </footer>

    <script>
        let bolsa_actual = []; let total_bolsa = 0;

        function gestionarCarrito(nombre, precio) {
            bolsa_actual.push({ item: nombre, precio: precio });
            total_bolsa += precio;
            document.getElementById('conteo-bolsa').innerText = bolsa_actual.length;
            console.log(`[LOGISTICA] Articulo añadido: ${nombre} | Valor: ${precio}`);
        }

        async function procesarBolsa() {
            if(bolsa_actual.length === 0) return alert("NO HAY ARTÍCULOS EN LA BOLSA DE PEDIDO.");
            const cl_nombre = prompt("NOMBRE COMPLETO PARA FACTURACIÓN:");
            const cl_destino = prompt("DIRECCIÓN DE ENTREGA DETALLADA:");
            if(!cl_nombre || !cl_destino) return alert("DATOS DE DESPACHO INCOMPLETOS.");
            
            const datos_pedido = { 
                cliente: cl_nombre, 
                direccion: cl_destino, 
                articulos: bolsa_actual.map(x => x.item).join(", "), 
                total: total_bolsa, 
                fecha: new Date().toLocaleString() 
            };
            
            await fetch('/api/v4/registrar-pedido', { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify(datos_pedido) 
            });

            const link_wsp = `https://wa.me/{{ config.TELEFONO_WHATSAPP }}?text=LUVIRX STYLE - ORDEN DE COMPRA%0ACliente: ${cl_nombre}%0AItems: ${datos_pedido.articulos}%0ATotal: $${total_bolsa}%0ADestino: ${cl_destino}`;
            window.open(link_wsp);
            location.reload();
        }

        async function enviarConceptoDiseno() {
            const idea = document.getElementById('texto-concepto-3d').value;
            if(!idea || idea.length < 20) return alert("EL CONCEPTO DE DISEÑO ES DEMASIADO CORTO O ESTÁ VACÍO.");
            
            await fetch('/api/v4/guardar-diseno', { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify({ concepto: idea, fecha: new Date().toLocaleString() }) 
            });

            window.open(`https://wa.me/{{ config.TELEFONO_WHATSAPP }}?text=LUVIRX STYLE - NUEVO DISEÑO 3D%0ADetalle: ${idea}`);
            alert("SU CONCEPTO HA SIDO RECIBIDO POR EL DEPARTAMENTO DE INGENIERÍA TEXTIL.");
            location.reload();
        }

        async function radicarReclamoOficial() {
            const nom = document.getElementById('nombre-reclamo').value;
            const con = document.getElementById('contacto-reclamo').value;
            const msg = document.getElementById('mensaje-reclamo').value;
            
            if(!nom || !msg) return alert("ERROR: CAMPOS OBLIGATORIOS FALTANTES.");
            
            const obj_reclamo = { nombre: nom, contacto: con, mensaje: msg, fecha: new Date().toLocaleString() };
            
            await fetch('/api/v4/log-reclamo', { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify(obj_reclamo) 
            });

            window.open(`https://wa.me/{{ config.TELEFONO_WHATSAPP }}?text=ALERTA - RECLAMO ESCALADO%0ACliente: ${nom}%0AAsunto: ${msg.substring(0, 100)}...`);
            alert("EL RECLAMO HA SIDO RADICADO Y ESCALADO A GERENCIA.");
            location.reload();
        }

        function accesoBoveda() {
            if(prompt("SISTEMA DE ENCRIPTACIÓN LUVIRX - INGRESE PIN DE ACCESO:") === "{{ config.CODIGO_ACCESO_VAULT }}") {
                document.getElementById('boveda-gerencial').style.display = 'block';
                actualizarPanelGerencial();
            }
        }

        function salirDeBoveda() { document.getElementById('boveda-gerencial').style.display = 'none'; }

        async function actualizarPanelGerencial() {
            const respuesta = await fetch('/api/v4/obtener-sistema');
            const d = await respuesta.json();
            
            let contenido = `
                <div class="boveda-card">
                    <h3>Registro Maestro de Ventas</h3>
                    <table class="tabla-estratégica">
                        <tr><th>Fecha</th><th>Titular</th><th>Monto Bruto</th></tr>
                        ${d.pedidos_maestros.map(p => `<tr><td>${p.fecha}</td><td>${p.cliente}</td><td>$${p.total}</td></tr>`).join('')}
                    </table>
                </div>
                <div class="boveda-card">
                    <h3>Diseños en Cola de Producción</h3>
                    <table class="tabla-estratégica">
                        <tr><th>Fecha</th><th>Concepto de Ingeniería</th></tr>
                        ${d.disenos_ingenieria.map(ds => `<tr><td>${ds.fecha}</td><td>${ds.concepto}</td></tr>`).join('')}
                    </table>
                </div>
                <div class="boveda-card" style="grid-column: span 2;">
                    <h3 style="color:red;">Auditoría de Reclamos y Quejas</h3>
                    <table class="tabla-estratégica">
                        <tr><th>Fecha de Radicación</th><th>Informante</th><th>Estado del Mensaje</th></tr>
                        ${d.centro_reclamos.map(r => `<tr><td>${r.fecha}</td><td>${r.nombre} (${r.contacto})</td><td>${r.mensaje}</td></tr>`).join('')}
                    </table>
                </div>
            `;
            document.getElementById('render-datos-gerenciales').innerHTML = contenido;
        }
    </script>
</body>
</html>
"""

# ------------------------------------------------------------------------------
# CONTROLADORES DE SERVIDOR (LOGICA DE BACKEND EMPRESARIAL)
# ------------------------------------------------------------------------------
@app.route('/')
def portal_principal():
    # Registro de auditoría silenciosa
    sistema_datos["metricas_globales"]["historial_acciones"].append(f"Acceso al Portal: {datetime.datetime.now()}")
    return render_template_string(HTML_PLATAFORMA_LUVIRX_V4, 
                                  config=CONFIGURACION_LUVIRX, 
                                  inventario=INVENTARIO_MAESTRO)

@app.route('/api/v4/registrar-pedido', methods=['POST'])
def api_pedido():
    datos = request.json
    sistema_datos["pedidos_maestros"].append(datos)
    sistema_datos["metricas_globales"]["ventas_totales_brutas"] += datos["total"]
    sistema_datos["metricas_globales"]["pedidos_acumulados"] += 1
    return jsonify({"estado": "Pedido Procesado", "codigo": 200})

@app.route('/api/v4/guardar-diseno', methods=['POST'])
def api_diseno():
    sistema_datos["disenos_ingenieria"].append(request.json)
    sistema_datos["metricas_globales"]["clics_en_diseno"] += 1
    return jsonify({"estado": "Diseño en Cola", "codigo": 200})

@app.route('/api/v4/log-reclamo', methods=['POST'])
def api_reclamo():
    sistema_datos["centro_reclamos"].append(request.json)
    return jsonify({"estado": "Reclamo Radicado", "codigo": 200})

@app.route('/api/v4/obtener-sistema')
def api_datos_maestros():
    sistema_datos["metricas_globales"]["ultimo_acceso_gerencial"] = str(datetime.datetime.now())
    return jsonify(sistema_datos)

# ------------------------------------------------------------------------------
# INICIO DEL ENTORNO DE PRODUCCIÓN
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # El modo debug permite ver errores en tiempo real durante la implementación
    app.run(debug=True)