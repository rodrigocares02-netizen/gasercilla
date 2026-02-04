import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
from database import save_order, get_orders

# page config
st.set_page_config(page_title="Gas Ercilla - Pedidos", page_icon="🚚", layout="wide")

# load custom css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# sidebar logo/hero image
st.sidebar.image("https://raw.githubusercontent.com/streamlit/streamlit/develop/examples/demo-usage/images/logo.png", width=100) # Placeholder for now, can be changed to our generated image
st.sidebar.title("Gas Ercilla")
st.sidebar.markdown("Tu gas de siempre, ahora más rápido. 🚚")

# Main Content
col1, col2 = st.columns([2, 3])

with col1:
    st.image("logo.png", use_container_width=True)
    st.markdown("""
    ### Horario de Atención
    🕒 Lunes a Sábado: 09:00 - 20:00
    🕒 Domingos y Festivos: 10:00 - 15:00
    """)

with col2:
    st.title("🚚 Realiza tu Pedido")
    
    # Precios
    precios = {
        "5 kg": 10500,
        "11 kg": 16500,
        "15 kg": 22500,
        "45 kg": 65000
    }

    with st.form("pedido_gas", clear_on_submit=False):
        nombre = st.text_input("👤 Tu Nombre")
        opcion_gas = st.selectbox("📦 ¿Qué cilindro necesitas?", list(precios.keys()))
        cantidad = st.number_input("🔢 Cantidad", min_value=1, value=1)
        direccion = st.text_input("📍 Dirección de entrega (Ej: Calle Comercio #123)")
        metodo_pago = st.radio("💳 Método de Pago", ["Efectivo", "Transferencia", "Tarjeta (Redelcom)"], horizontal=True)
        
        submit = st.form_submit_button("Confirmar Pedido y Enviar WhatsApp ✅")

    if submit:
        if not nombre or not direccion:
            st.error("Por favor, completa tu nombre y dirección.")
        else:
            total = precios[opcion_gas] * cantidad
            fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Save to local DB
            order_data = {
                "Fecha": fecha_hora,
                "Cliente": nombre,
                "Pedido": f"{cantidad} x {opcion_gas}",
                "Dirección": direccion,
                "Total": total,
                "Pago": metodo_pago
            }
            save_order(order_data)
            
            # Success Message
            st.success(f"¡Muchas gracias {nombre}! Tu pedido por ${total:,} ha sido registrado.")
            
            # WhatsApp Redirect Logic
            mensaje_wa = (
                f"*NUEVO PEDIDO - GAS ERCILLA*\n"
                f"📅 Fecha: {fecha_hora}\n"
                f"👤 Cliente: {nombre}\n"
                f"📦 Pedido: {cantidad} x {opcion_gas}\n"
                f"📍 Dirección: {direccion}\n"
                f"💰 Total: ${total:,}\n"
                f"💳 Pago: {metodo_pago}"
            )
            
            # Encode for URL
            encoded_msg = urllib.parse.quote(mensaje_wa)
            wa_url = f"https://wa.me/56961499736?text={encoded_msg}"
            
            # Provide link as button
            st.markdown(f"""
                <a href="{wa_url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25D366; color: white; padding: 15px 25px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 1.2rem;">
                        📱 Abrir WhatsApp y Enviar Mensaje
                    </div>
                </a>
            """, unsafe_allow_html=True)

# Admin View (Simple implementation for now)
if st.sidebar.checkbox("🔒 Modo Admin"):
    st.divider()
    st.subheader("📊 Panel de Pedidos Recientes")
    orders_df = get_orders()
    if not orders_df.empty:
        st.dataframe(orders_df.sort_values(by="Fecha", ascending=False), use_container_width=True)
    else:
        st.info("Aún no hay pedidos registrados.")
