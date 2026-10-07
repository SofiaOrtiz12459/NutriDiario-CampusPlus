import streamlit as st
import pandas as pd
from datetime import date, datetime, time

st.set_page_config(
    page_title="NutriDiario U",
    page_icon="🥗",
    layout="wide"
)

# =========================
# ESTILO VERDE
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #F5FBF5 0%, #E8F5E9 100%);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #123D25 0%, #1F6B3A 100%);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
h1, h2, h3 {
    color: #174D2A !important;
}
.hero {
    background: linear-gradient(135deg, #14532D, #2E7D32, #66BB6A);
    padding: 30px;
    border-radius: 24px;
    color: white;
    box-shadow: 0 10px 24px rgba(20,83,45,.18);
    margin-bottom: 24px;
}
.hero h1, .hero h2, .hero h3 {
    color: white !important;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 5px 16px rgba(0,0,0,.07);
    margin: 10px 0;
    border-top: 4px solid #43A047;
}
.premium {
    background: linear-gradient(135deg, #E8F5E9, #FFFFFF);
    padding: 22px;
    border-radius: 20px;
    border: 2px solid #66BB6A;
    box-shadow: 0 6px 18px rgba(46,125,50,.12);
}
.badge {
    display: inline-block;
    background: #DFF5E4;
    color: #14532D;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 700;
    margin-bottom: 8px;
}
div[data-testid="stMetric"] {
    background: white;
    border-radius: 18px;
    padding: 16px;
    border-left: 5px solid #2E7D32;
    box-shadow: 0 4px 14px rgba(0,0,0,.06);
}
.stButton > button {
    background: linear-gradient(90deg, #2E7D32, #43A047);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# =========================
# ESTADO
# =========================
defaults = {
    "alimentos": [],
    "agua": 0,
    "nombre": "Estudiante",
    "plan": "Gratis",
    "puntos": 0,
    "racha": 1
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================
# FUNCIONES
# =========================
def totales():
    kcal = sum(float(a.get("Calorías", 0)) for a in st.session_state.alimentos)
    prot = sum(float(a.get("Proteína", 0)) for a in st.session_state.alimentos)
    carb = sum(float(a.get("Carbohidratos", 0)) for a in st.session_state.alimentos)
    grasa = sum(float(a.get("Grasas", 0)) for a in st.session_state.alimentos)
    return kcal, prot, carb, grasa

def recomendacion_campus(presupuesto, minutos, hambre, energia, acceso):
    opciones = []

    if presupuesto <= 6000:
        opciones = [
            ("Avena + banano", 4500, "rápida, económica y fácil de transportar"),
            ("Arepa + huevo", 5500, "combina carbohidrato y proteína"),
            ("Yogur natural + fruta", 6000, "opción práctica entre clases")
        ]
    elif presupuesto <= 12000:
        opciones = [
            ("Arroz + lentejas + huevo", 8500, "comida completa y rendidora"),
            ("Sándwich de pollo + fruta", 10000, "práctico para una pausa corta"),
            ("Bowl de arroz, proteína y verduras", 12000, "opción balanceada para almuerzo")
        ]
    else:
        opciones = [
            ("Almuerzo completo con proteína, arroz y ensalada", 15000, "mejor para una pausa larga"),
            ("Wrap de pollo + fruta + agua", 14000, "portable y fácil de comer"),
            ("Bowl universitario con proteína y vegetales", 17000, "útil para jornadas extensas")
        ]

    if minutos <= 10:
        prioridad = "Necesitas algo que puedas conseguir y comer muy rápido."
        opcion = opciones[0]
    elif minutos <= 25:
        prioridad = "Tienes una pausa corta: conviene priorizar practicidad y saciedad."
        opcion = opciones[min(1, len(opciones)-1)]
    else:
        prioridad = "Tienes tiempo suficiente para una comida más completa."
        opcion = opciones[-1]

    if hambre >= 8:
        ajuste = "Tu nivel de hambre es alto: evita quedarte solo con una bebida o snack pequeño."
    elif hambre >= 5:
        ajuste = "Tu hambre es moderada: una comida o snack estructurado puede ser suficiente."
    else:
        ajuste = "Tu hambre es baja: puedes elegir una porción pequeña y volver a evaluar después."

    if energia <= 4:
        energia_txt = "Prioriza una comida real, agua y una pausa breve antes de continuar estudiando."
    else:
        energia_txt = "Tu energía reportada es aceptable; mantén hidratación y horarios regulares."

    acceso_txt = {
        "Cafetería universitaria": "Busca la alternativa más parecida disponible en la cafetería.",
        "Tienda cercana": "Elige una combinación simple, evitando depender solo de paquetes y bebidas.",
        "Comida desde casa": "Puedes preparar esta opción con antelación y llevarla en un recipiente.",
        "Restaurante": "Pide una porción con proteína, cereal/tubérculo y vegetales cuando sea posible."
    }[acceso]

    return opcion, prioridad, ajuste, energia_txt, acceso_txt

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("## 🥗 NutriDiario U")
st.sidebar.caption("Nutrición pensada para la vida universitaria")
st.sidebar.markdown(f"**Plan actual:** {st.session_state.plan}")

pagina = st.sidebar.radio(
    "Menú",
    [
        "🏠 Inicio",
        "🍽️ Mi diario",
        "➕ Registrar comida",
        "💧 Hidratación",
        "🎓 Modo Campus+",
        "📊 Progreso",
        "🏆 Retos",
        "🥑 Recomendaciones",
        "💎 Membresía",
        "👤 Mi perfil"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("🌱 Come mejor")
st.sidebar.write("💧 Hidrátate")
st.sidebar.write("📚 Organízate")
st.sidebar.write("💰 Cuida tu presupuesto")

# =========================
# INICIO
# =========================
if pagina == "🏠 Inicio":
    st.markdown(f"""
    <div class="hero">
        <h1>🥗 NutriDiario U</h1>
        <p>Hola, {st.session_state.nombre} 👋</p>
        <p>Tu asistente de hábitos para sobrevivir a clases, parciales y días largos de universidad.</p>
    </div>
    """, unsafe_allow_html=True)

    kcal, prot, carb, grasa = totales()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Calorías registradas", f"{kcal:.0f} kcal")
    c2.metric("🥩 Proteína", f"{prot:.1f} g")
    c3.metric("💧 Agua", f"{st.session_state.agua}/8 vasos")
    c4.metric("🏆 Puntos Campus", st.session_state.puntos)

    st.markdown("### 🎓 Semáforo universitario")
    comidas = len(st.session_state.alimentos)

    if st.session_state.agua < 3 or comidas == 0:
        st.error("🔴 Atención: hoy llevas poco registro de comida o hidratación. Revisa tu próxima pausa.")
    elif st.session_state.agua < 6 or comidas < 3:
        st.warning("🟡 Vas a mitad de camino. Organiza una comida o snack para tu siguiente bloque de clases.")
    else:
        st.success("🟢 Buen ritmo de registro. Mantén agua y horarios regulares.")

    st.markdown("### 💧 Hidratación")
    st.progress(min(st.session_state.agua / 8, 1.0))

    st.markdown("### 🎯 Progreso de registro")
    st.progress(min(kcal / 2000, 1.0))
    st.caption("La referencia de 2.000 kcal se usa solo como visualización general, no como meta clínica personalizada.")

# =========================
# DIARIO
# =========================
elif pagina == "🍽️ Mi diario":
    st.title("🍽️ Mi diario nutricional")
    fecha = st.date_input("📅 Fecha", date.today())

    if not st.session_state.alimentos:
        st.info("Aún no has registrado alimentos.")
    else:
        df = pd.DataFrame(st.session_state.alimentos)
        for comida in ["Desayuno", "Almuerzo", "Cena", "Snack"]:
            st.subheader(f"🍴 {comida}")
            filtro = df[df["Comida"] == comida]
            if filtro.empty:
                st.caption("Sin registros.")
            else:
                st.dataframe(filtro, use_container_width=True, hide_index=True)

# =========================
# REGISTRO
# =========================
elif pagina == "➕ Registrar comida":
    st.title("➕ Registrar comida")

    col1, col2 = st.columns(2)
    with col1:
        comida = st.selectbox("Momento", ["Desayuno", "Almuerzo", "Cena", "Snack"])
        alimento = st.text_input("Alimento", placeholder="Ej.: arroz con pollo")
        cantidad = st.number_input("Cantidad aproximada (g)", 0, 2000, 100, 10)
    with col2:
        calorias = st.number_input("Calorías aproximadas", min_value=0.0, value=0.0)
        proteina = st.number_input("Proteína (g)", min_value=0.0, value=0.0)
        carbohidratos = st.number_input("Carbohidratos (g)", min_value=0.0, value=0.0)
        grasas = st.number_input("Grasas (g)", min_value=0.0, value=0.0)

    if st.button("✅ Guardar alimento", use_container_width=True):
        if not alimento.strip():
            st.error("Escribe el nombre del alimento.")
        else:
            st.session_state.alimentos.append({
                "Fecha": str(date.today()),
                "Comida": comida,
                "Alimento": alimento,
                "Cantidad (g)": cantidad,
                "Calorías": calorias,
                "Proteína": proteina,
                "Carbohidratos": carbohidratos,
                "Grasas": grasas
            })
            st.session_state.puntos += 10
            st.success(f"✅ {alimento} guardado. +10 puntos Campus")

# =========================
# AGUA
# =========================
elif pagina == "💧 Hidratación":
    st.title("💧 Hidratación")
    c1, c2, c3 = st.columns(3)
    c1.metric("Vasos", st.session_state.agua)
    c2.metric("Referencia diaria", "8")
    c3.metric("Faltan", max(8 - st.session_state.agua, 0))

    st.progress(min(st.session_state.agua / 8, 1.0))

    a, b = st.columns(2)
    with a:
        if st.button("💧 Añadir un vaso", use_container_width=True):
            st.session_state.agua += 1
            st.session_state.puntos += 2
            st.rerun()
    with b:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.agua = 0
            st.rerun()

# =========================
# MODO CAMPUS+
# =========================
elif pagina == "🎓 Modo Campus+":
    st.title("🎓 Modo Campus+")
    st.markdown("""
    <div class="premium">
        <span class="badge">DIFERENCIAL NUTRIDIARIO</span>
        <h3>¿Qué hago en mi próxima pausa?</h3>
        <p>Combina presupuesto, tiempo disponible, hambre, energía y acceso a comida
        para darte una opción práctica entre clases.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.plan != "Campus+":
        st.warning("🔒 Esta función pertenece a Campus+. Puedes activarla en la sección Membresía para probarla.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            presupuesto = st.number_input("💰 Presupuesto disponible hoy (COP)", 2000, 100000, 10000, 1000)
            minutos = st.slider("⏱️ Minutos libres antes de la siguiente clase", 5, 120, 20)
            acceso = st.selectbox(
                "📍 ¿Dónde puedes conseguir comida?",
                ["Cafetería universitaria", "Tienda cercana", "Comida desde casa", "Restaurante"]
            )
        with col2:
            hambre = st.slider("🍽️ Nivel de hambre", 1, 10, 6)
            energia = st.slider("⚡ Nivel de energía", 1, 10, 6)
            hora_clase = st.time_input("🕐 Próxima clase", value=time(14, 0))

        if st.button("✨ Crear mi decisión Campus+", use_container_width=True):
            opcion, prioridad, ajuste, energia_txt, acceso_txt = recomendacion_campus(
                presupuesto, minutos, hambre, energia, acceso
            )

            nombre_opcion, precio, motivo = opcion

            st.success(f"🥗 Opción sugerida: **{nombre_opcion}**")
            x1, x2, x3 = st.columns(3)
            x1.metric("💰 Costo estimado", f"${precio:,.0f} COP")
            x2.metric("⏱️ Pausa disponible", f"{minutos} min")
            x3.metric("⚡ Energía reportada", f"{energia}/10")

            st.markdown("### 🧠 ¿Por qué esta opción?")
            st.write(f"**Tiempo:** {prioridad}")
            st.write(f"**Hambre:** {ajuste}")
            st.write(f"**Energía:** {energia_txt}")
            st.write(f"**Acceso:** {acceso_txt}")
            st.write(f"**Motivo de la opción:** {motivo}.")

            if precio <= presupuesto:
                ahorro = presupuesto - precio
                st.info(f"💚 Está dentro de tu presupuesto. Te quedarían aproximadamente **${ahorro:,.0f} COP**.")
            else:
                st.error("Esta opción supera tu presupuesto registrado.")

            st.caption("Las sugerencias son educativas y de organización; no constituyen un plan médico o nutricional individual.")

# =========================
# PROGRESO
# =========================
elif pagina == "📊 Progreso":
    st.title("📊 Progreso")
    datos = pd.DataFrame({
        "Día": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
        "Registro de comidas": [3, 4, 3, 4, 2, 3, 3],
        "Vasos de agua": [6, 8, 7, 8, 5, 8, 7]
    })
    st.bar_chart(datos.set_index("Día"))

    c1, c2, c3 = st.columns(3)
    c1.metric("🔥 Racha", f"{st.session_state.racha} días")
    c2.metric("🏆 Puntos", st.session_state.puntos)
    c3.metric("🍽️ Registros", len(st.session_state.alimentos))

# =========================
# RETOS
# =========================
elif pagina == "🏆 Retos":
    st.title("🏆 Retos universitarios")
    st.write("Convierte hábitos pequeños en puntos y rachas.")

    retos = [
        ("💧 Reto Hidratación", "Registra 6 o más vasos de agua.", 20, st.session_state.agua >= 6),
        ("🍽️ Reto Diario", "Registra al menos 3 comidas.", 30, len(st.session_state.alimentos) >= 3),
        ("🎓 Reto Campus", "Usa Modo Campus+ para planear una pausa.", 25, False)
    ]

    for titulo, texto, puntos, cumplido in retos:
        estado = "✅ Cumplido" if cumplido else "⏳ Pendiente"
        st.markdown(f"""
        <div class="card">
            <h3>{titulo}</h3>
            <p>{texto}</p>
            <strong>{estado} · +{puntos} puntos</strong>
        </div>
        """, unsafe_allow_html=True)

# =========================
# RECOMENDACIONES
# =========================
elif pagina == "🥑 Recomendaciones":
    st.title("🥑 Recomendaciones")
    recomendaciones = [
        ("🥣 Antes de clase", "Si tienes una jornada larga, procura no depender únicamente de café."),
        ("🍎 Entre clases", "Lleva una opción fácil de transportar como fruta, yogur o un sándwich."),
        ("💧 Agua visible", "Llevar una botella a la vista puede ayudarte a recordar hidratarte."),
        ("💰 Presupuesto", "Planear 2 o 3 opciones económicas antes de salir puede reducir compras impulsivas."),
        ("📚 Parciales", "En días de estudio intenso, organiza pausas breves para comer y descansar.")
    ]
    for t, d in recomendaciones:
        st.markdown(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>', unsafe_allow_html=True)

# =========================
# MEMBRESÍA
# =========================
elif pagina == "💎 Membresía":
    st.title("💎 Membresía NutriDiario")

    st.markdown("### Elige cómo quieres usar NutriDiario")

    free, plus = st.columns(2)

    with free:
        st.markdown("""
        <div class="card">
            <h2>🌱 Gratis</h2>
            <p><b>$0 COP</b></p>
            <p>✓ Diario de comidas</p>
            <p>✓ Registro de agua</p>
            <p>✓ Dashboard básico</p>
            <p>✓ Recomendaciones generales</p>
            <p>✓ Retos y puntos básicos</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Usar plan Gratis", use_container_width=True):
            st.session_state.plan = "Gratis"
            st.success("Plan Gratis activado.")

    with plus:
        st.markdown("""
        <div class="premium">
            <span class="badge">MÁS COMPLETO</span>
            <h2>🎓 Campus+</h2>
            <p><b>Demo académica</b></p>
            <p>✓ Todo lo del plan Gratis</p>
            <p>✓ Modo Campus+</p>
            <p>✓ Decisión según presupuesto</p>
            <p>✓ Decisión según horario de clases</p>
            <p>✓ Hambre y energía reportadas</p>
            <p>✓ Opciones rápidas entre clases</p>
            <p>✓ Semáforo universitario</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✨ Activar Campus+ (demo)", use_container_width=True):
            st.session_state.plan = "Campus+"
            st.success("🎉 Campus+ activado para esta demostración.")

    st.info(f"Plan activo actualmente: **{st.session_state.plan}**")
    st.caption("Esta versión académica no procesa pagos reales.")

# =========================
# PERFIL
# =========================
elif pagina == "👤 Mi perfil":
    st.title("👤 Mi perfil")
    nombre = st.text_input("Nombre", value=st.session_state.nombre)
    edad = st.number_input("Edad", 16, 80, 20)
    carrera = st.text_input("Carrera", placeholder="Ej.: Ingeniería Industrial")

    c1, c2 = st.columns(2)
    with c1:
        peso = st.number_input("Peso (kg)", 30.0, 200.0, 60.0)
    with c2:
        estatura = st.number_input("Estatura (m)", 1.30, 2.20, 1.65)

    objetivo = st.selectbox(
        "Objetivo general",
        ["Mejorar hábitos", "Organizar mis comidas", "Mantener peso", "Aumentar peso", "Reducir peso"]
    )

    imc = peso / (estatura ** 2)
    st.metric("IMC estimado", f"{imc:.1f}")

    if st.button("💾 Guardar perfil", use_container_width=True):
        st.session_state.nombre = nombre
        st.success("Perfil actualizado.")

st.markdown("---")
st.caption(
    "🌱 NutriDiario U · Bienestar y organización alimentaria para estudiantes universitarios. "
    "No reemplaza la atención de profesionales de salud."
)
