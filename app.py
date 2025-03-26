import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Sistema Contable Básico")

st.markdown(
    """
    <style>
    .stDataFrame {
        background-color: #001F3F; /* Azul oscuro */
        color: #FFD700; /* Dorado */
    }
    .stDataFrame th {
        background-color: #001F3F; /* Azul oscuro */
        color: #FFD700; /* Dorado */
    }
    .stDataFrame td {
        background-color: #001F3F; /* Azul oscuro */
        color: #FFD700; /* Dorado */
    }
    .stDataFrame {
        width: 100%; /* Extender el tamaño de las tablas */
    }
    </style>
    """,
    unsafe_allow_html=True
)

if 'transacciones' not in st.session_state:
    st.session_state.transacciones = []

if 'balances' not in st.session_state:
    st.session_state.balances = {
        "Activo": {"Caja": 0, "Bancos": 0, "Mercancías": 0, "Terrenos": 0, "Edificios": 0, "Equipo de cómputo": 0, "Mobiliario y equipo": 0, "Muebles y enseres": 0, "IVA pagado": 0,"IVA por acreditar": 0, "Rentas pagadas por anticipado": 0, "Clientes": 0, "Equipo de transporte": 0, "Papelería": 0},
        "Pasivo": {"Acreedores": 0, "Documentos por pagar": 0, "IVA trasladado": 0, "IVA por trasladar": 0,"Anticipo de clientes":0},
        "Capital": {"Capital Social": 0, "Utilidad del Periodo": 0},
        "Extra": {"Costo de lo vendido": 0, "Venta": 0, "Gastos generales": 0, "Depreciación Acumulada Edificios": 0, "Depreciación Acumulada Equipo de cómputo": 0, "Depreciación Acumulada Mobiliario y equipo": 0, "Depreciación Acumulada Muebles y enseres": 0, "Depreciación Acumulada Equipo de transporte": 0}
    }

if 'libro_mayor' not in st.session_state:
    st.session_state.libro_mayor = {}

def mostrar_balance_general():
    st.subheader("Balance General")
    
    activo = st.session_state.balances["Activo"]
    Extra = st.session_state.balances["Extra"]
    balance_activo = {
        "Activo Circulante": {
            "Caja": activo["Caja"],
            "Bancos": activo["Bancos"],
            "Mercancías": activo["Mercancías"],
            "IVA pagado": activo["IVA pagado"],
            "IVA por acreditar": activo.get("IVA por acreditar", 0),
            "Rentas pagadas por anticipado": activo["Rentas pagadas por anticipado"],
            "Papelería": activo["Papelería"],
            "Clientes": activo["Clientes"]
        },
        "Activo No Circulante": {
            "Terrenos": activo["Terrenos"],
            "Edificios": activo["Edificios"] + Extra["Depreciación Acumulada Edificios"],
            "Equipo de cómputo": activo["Equipo de cómputo"] + Extra["Depreciación Acumulada Equipo de cómputo"],
            "Mobiliario y equipo": activo["Mobiliario y equipo"] + Extra["Depreciación Acumulada Mobiliario y equipo"],
            "Muebles y enseres": activo["Muebles y enseres"] + Extra["Depreciación Acumulada Muebles y enseres"],
            "Equipo de transporte": activo["Equipo de transporte"] + Extra["Depreciación Acumulada Equipo de transporte"]
        }
    }

    df_circulante = pd.DataFrame.from_dict(balance_activo["Activo Circulante"], orient="index", columns=["Monto"])
    subtotal_circulante = df_circulante["Monto"].sum()

    df_no_circulante = pd.DataFrame.from_dict(balance_activo["Activo No Circulante"], orient="index", columns=["Monto"])
    subtotal_no_circulante = df_no_circulante["Monto"].sum()

    st.write("### Activo")
    
    st.write("**Circulante**")
    st.dataframe(df_circulante)
    st.write(f"**Total Activo Circulante:** ${subtotal_circulante:,.2f}")
    
    st.write("**No Circulante**")
    st.dataframe(df_no_circulante)
    st.write(f"**Total Activo No Circulante:** ${subtotal_no_circulante:,.2f}")
    
    st.write(f"**Total Activo:** ${subtotal_circulante + subtotal_no_circulante:,.2f}")



    st.write("### Pasivo")
    pasivo_df = pd.DataFrame.from_dict(st.session_state.balances["Pasivo"], orient="index", columns=["Monto"])
    pasivo_df["Monto"] = pasivo_df["Monto"].abs()
    st.dataframe(pasivo_df)
    total_pasivo = pasivo_df["Monto"].sum()  
    st.write(f"**Total Pasivo:** ${total_pasivo:,.2f}")

    st.write("### Capital")
    capital_df = pd.DataFrame.from_dict(st.session_state.balances["Capital"], orient="index", columns=["Monto"])
    capital_df["Monto"] = capital_df["Monto"].abs()
    st.dataframe(capital_df)
    total_capital = capital_df["Monto"].sum()  
    st.write(f"**Total Capital:** ${total_capital:,.2f}")

    st.write(f"**Total Pasivo + Capital:** ${total_pasivo + total_capital:,.2f}")

def mostrar_estado_resultados():
    st.subheader("Estado de Resultados")

    ventas = abs(st.session_state.balances["Extra"].get("Venta", 0))
    costo_ventas = abs(st.session_state.balances["Extra"].get("Costo de lo vendido", 0))
    gastos_generales = abs(st.session_state.balances["Extra"].get("Gastos generales", 0))

    utilidad_bruta = ventas - costo_ventas

    utilidad_periodo = utilidad_bruta - gastos_generales


    estado_resultados = {
        "Concepto": ["Ventas", "Costo de lo vendido", "Utilidad Bruta", "Gastos generales", "Utilidad del Periodo"],
        "Monto": [ventas, costo_ventas, utilidad_bruta, gastos_generales, utilidad_periodo]
    }

    estado_resultados_df = pd.DataFrame(estado_resultados)
    st.session_state.balances["Capital"]["Utilidad del Periodo"] = utilidad_bruta - gastos_generales
    st.dataframe(estado_resultados_df)

    st.write(f"**Utilidad Bruta:** {utilidad_bruta}")
    st.write(f"**Utilidad del Periodo:** {utilidad_periodo}")

def mostrar_estado_cambios_capital():
    st.subheader("Estado de Cambios en el Capital Contable")

    capital_social = abs(st.session_state.balances["Capital"].get("Capital Social", 0)) 
    utilidad_periodo = st.session_state.balances["Capital"].get("Utilidad del Periodo", 0)

    reserva_legal = (utilidad_periodo * 0.05) / 12

    estado_cambios = {
        "Concepto": [
            "Saldo inicial",
            "Aumentos:",
            "Capital social",
            "Reserva legal",
            "Resultado del ejercicio (Utilidad)",
            "Total",
            "Disminuciones:",
            "Decreto de dividendos:",
            "Reserva legal:",
            "Reembolso a socios",
            "Total",
            "Incremento neto",
            "Saldo final"
        ],
        "Capital contribuido": [
            0,
            None,
            capital_social,
            0,
            0,
            capital_social,
            None,
            0,
            0,
            0,
            0,
            capital_social,
            capital_social
        ],
        "Capital ganado": [
            0,
            None,
            0,
            reserva_legal,
            utilidad_periodo,
            reserva_legal + utilidad_periodo,
            None,
            0,
            reserva_legal,
            0,
            reserva_legal,
            utilidad_periodo,
            utilidad_periodo
        ],
        "Capital contable": [
            0,
            None,
            capital_social,
            reserva_legal,
            utilidad_periodo,
            capital_social + reserva_legal + utilidad_periodo,
            None,
            0,
            reserva_legal,
            0,
            reserva_legal,
            capital_social + utilidad_periodo,
            capital_social + utilidad_periodo
        ]
    }

    estado_cambios_df = pd.DataFrame(estado_cambios)

    st.dataframe(estado_cambios_df)

def mostrar_estado_flujo_efectivo():
    st.subheader("Estado de Flujo de Efectivo")
    
    
    utilidad_periodo = st.session_state.balances["Capital"]["Utilidad del Periodo"]
    isr = utilidad_periodo * 0.30  
    ptu = utilidad_periodo * 0.10  
    utilidad_neta = utilidad_periodo - (isr + ptu)
    Depre1 = abs(st.session_state.balances["Extra"].get("Depreciación Acumulada Edificios", 0))
    Depre2 = abs(st.session_state.balances["Extra"].get("Depreciación Acumulada Equipo de cómputo", 0))
    Depre3 = abs(st.session_state.balances["Extra"].get("Depreciación Acumulada Mobiliario y equipo", 0))
    Depre4 = abs(st.session_state.balances["Extra"].get("Depreciación Acumulada Muebles y enseres", 0))
    Depre5 = abs(st.session_state.balances["Extra"].get("Depreciación Acumulada Equipo de transporte", 0))
    DepreciaTotal = Depre1+Depre2+Depre3+Depre4+Depre5

    st.write("### Actividades en Operación")
    operacion_data = {
        "Clientes":st.session_state.balances["Activo"]["Clientes"],
        "Mercancias":st.session_state.balances["Activo"]["Mercancías"],
        "IVA acreditable":st.session_state.balances["Activo"]["IVA pagado"],
        "IVA pendiente de acreditar":st.session_state.balances["Activo"]["IVA por acreditar"],
        "IVA trasladado":st.session_state.balances["Pasivo"]["IVA trasladado"],
        "IVA por trasladar":st.session_state.balances["Pasivo"]["IVA por trasladar"],
        "Proveedores": 0,
        "Provision de ISR": isr*-1,
        "Provision de PTU": ptu*-1,
        "Utilidad del ejercicio": utilidad_neta*-1,
        "Papelería":st.session_state.balances["Activo"]["Papelería"],
        "Rentas pagadas por anticipado":st.session_state.balances["Activo"]["Rentas pagadas por anticipado"],

    }
    df_operacion = pd.DataFrame.from_dict(operacion_data, orient="index", columns=["Monto"])
    st.dataframe(df_operacion)
    total_operacion = df_operacion["Monto"].sum()
    st.write(f"**Total Actividades en operación:** ${total_operacion:,.2f}")
    
    
    
    st.write("### Actividades de Inversión")
    inversion_data = {
        "Terrenos": st.session_state.balances["Activo"]["Terrenos"],
        "Edificios": st.session_state.balances["Activo"]["Edificios"] + st.session_state.balances["Extra"]["Depreciación Acumulada Edificios"],
        "Equipo de cómputo": st.session_state.balances["Activo"]["Equipo de cómputo"] + st.session_state.balances["Extra"]["Depreciación Acumulada Equipo de cómputo"],
        "Mobiliario y equipo": st.session_state.balances["Activo"]["Mobiliario y equipo"] + st.session_state.balances["Extra"]["Depreciación Acumulada Mobiliario y equipo"],
        "Muebles y enseres": st.session_state.balances["Activo"]["Muebles y enseres"] + st.session_state.balances["Extra"]["Depreciación Acumulada Muebles y enseres"],
        "Equipo de transporte": st.session_state.balances["Activo"]["Equipo de transporte"] + st.session_state.balances["Extra"]["Depreciación Acumulada Equipo de transporte"],
    }
    df_inversion = pd.DataFrame.from_dict(inversion_data, orient="index", columns=["Monto"])
    st.dataframe(df_inversion)
    total_inversion = df_inversion["Monto"].sum()
    st.write(f"**Flujos netos de efectivo de inversión:** ${total_inversion:,.2f}")
    
    st.write("### Actividades de Financiamiento")
    financiamiento_data = {
        "Capital Social": st.session_state.balances["Capital"]["Capital Social"],
        "Acreedores diversos": st.session_state.balances["Pasivo"]["Acreedores"],  
        "Financiamiento y otras fuentes":st.session_state.balances["Pasivo"]["Documentos por pagar"],
    }
    df_financiamiento = pd.DataFrame.from_dict(financiamiento_data, orient="index", columns=["Monto"])
    st.dataframe(df_financiamiento)
    total_financiamiento = df_financiamiento["Monto"].sum()
    st.write(f"**Flujos netos de efectivo de financiamiento:** ${total_financiamiento:,.2f}")
    
    st.write("### Incremento Neto de Efectivo")
    caja_final = st.session_state.balances["Activo"]["Caja"]
    bancos_final = st.session_state.balances["Activo"]["Bancos"]
    caja_inicial = 50_000.00  
    bancos_inicial = 1_500_000.00  
    cajaBanco = caja_final+bancos_final
    
    
    st.write(f"**Efectivo al principio (Caja):** ${caja_inicial:,.2f}")
    st.write(f"**Efectivo al final (Caja):** ${caja_final:,.2f}")
    st.write(f"**Efectivo al principio (Bancos):** ${bancos_inicial:,.2f}")
    st.write(f"**Efectivo al final (Bancos):** ${bancos_final:,.2f}")
    st.write(f"**Suma de caja y bancos final:** ${cajaBanco:,.2f}")
    st.write(f"**Efectivo al final del periodo:** ${total_financiamiento + total_inversion + total_operacion :,.2f}")

    st.write("**Fuentes de Efectivo**")
    fuentes_data = {
        "Utilidad del ejercicio": utilidad_neta,
        "Depreciaciones": DepreciaTotal,
        "Cargos a resultados (no efectivo)": 0,
        "ISR": isr,
        "PTU": ptu,
        "Acreedores": abs(st.session_state.balances["Pasivo"]["Acreedores"]), 
        "Financiamiento y otras fuentes": abs(st.session_state.balances["Pasivo"]["Documentos por pagar"]),
        "Proveedores":0,
        "Capital social":abs(st.session_state.balances["Capital"]["Capital Social"]),
        
    }
    df_fuentes = pd.DataFrame.from_dict(fuentes_data, orient="index", columns=["Monto"])
    st.dataframe(df_fuentes)
    total_fuentes = df_fuentes["Monto"].sum()
    Efectivo_operacion=utilidad_neta+DepreciaTotal+isr+ptu+abs(st.session_state.balances["Pasivo"]["Acreedores"])
    st.write(f"**Efectivo generado en la operación:** ${Efectivo_operacion:,.2f}")
    st.write(f"**Suma de las fuentes de efectivo:** ${total_fuentes:,.2f}")

    st.write("**Aplicación de Efectivo**")
    aplicacion_data = {
        "Mercancías": abs(st.session_state.balances["Activo"]["Mercancías"]),
        "Clientes": abs(st.session_state.balances["Activo"]["Clientes"]),
        "Papelería":st.session_state.balances["Activo"]["Papelería"],
        "Rentas pagadas por anticipado": abs(st.session_state.balances["Activo"]["Rentas pagadas por anticipado"]),
        "IVA acreditable": abs(st.session_state.balances["Activo"]["IVA pagado"]),
        "IVA pendiente de acreditar": abs(st.session_state.balances["Activo"]["IVA por acreditar"]),
        "IVA trasladado": (st.session_state.balances["Pasivo"]["IVA trasladado"]),  
        "IVA por trasladar": (st.session_state.balances["Pasivo"]["IVA por trasladar"]),  
        "Terrenos": st.session_state.balances["Activo"]["Terrenos"],
        "Edificios": st.session_state.balances["Activo"]["Edificios"] ,
        "Equipo de cómputo": st.session_state.balances["Activo"]["Equipo de cómputo"] ,
        "Mobiliario y equipo": st.session_state.balances["Activo"]["Mobiliario y equipo"] ,
        "Muebles y enseres": st.session_state.balances["Activo"]["Muebles y enseres"] ,
        "Equipo de transporte": st.session_state.balances["Activo"]["Equipo de transporte"] , 
    }
    df_aplicacion = pd.DataFrame.from_dict(aplicacion_data, orient="index", columns=["Monto"])
    st.dataframe(df_aplicacion)
    total_aplicacion = df_aplicacion["Monto"].sum()
    st.write(f"**Total aplicacion de efectivo:** ${total_aplicacion:,.2f}")
    flujo_neto_operacion = total_fuentes - total_aplicacion
    st.write(f"**Disminución neta del efectivo:** ${flujo_neto_operacion:,.2f}")
    st.write(f"**Efectivo al principio (Caja):** ${caja_inicial:,.2f}")
    st.write(f"**Efectivo al final (Caja):** ${caja_final:,.2f}")
    st.write(f"**Efectivo al principio (Bancos):** ${bancos_inicial:,.2f}")
    st.write(f"**Efectivo al final (Bancos):** ${bancos_final:,.2f}")
    st.write(f"**Suma de caja y bancos final:** ${cajaBanco:,.2f}")



def actualizar_balances(transaccion):
    for cuenta, monto in transaccion["cargos"].items():
        if cuenta in st.session_state.balances["Activo"]:
            st.session_state.balances["Activo"][cuenta] += monto
        elif cuenta in st.session_state.balances["Pasivo"]:
            st.session_state.balances["Pasivo"][cuenta] += monto
        elif cuenta in st.session_state.balances["Capital"]:
            st.session_state.balances["Capital"][cuenta] += monto
        elif cuenta in st.session_state.balances["Extra"]:
            st.session_state.balances["Extra"][cuenta] += monto

        if cuenta not in st.session_state.libro_mayor:
            st.session_state.libro_mayor[cuenta] = {"Cargos": [], "Abonos": []}
        st.session_state.libro_mayor[cuenta]["Cargos"].append(monto)

    for cuenta, monto in transaccion["abonos"].items():
        if cuenta in st.session_state.balances["Activo"]:
            st.session_state.balances["Activo"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Pasivo"]:
            st.session_state.balances["Pasivo"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Capital"]:
            st.session_state.balances["Capital"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Extra"]:
            st.session_state.balances["Extra"][cuenta] -= monto

        if cuenta not in st.session_state.libro_mayor:
            st.session_state.libro_mayor[cuenta] = {"Cargos": [], "Abonos": []}
        st.session_state.libro_mayor[cuenta]["Abonos"].append(monto)

option = st.sidebar.selectbox(
    "Selecciona una operación",
    ["Asiento de apertura", "Compra en efectivo", "Compra a crédito", "Compra combinada", "Anticipo de clientes", "Compra de papelería", "Pago de rentas anticipadas", "Venta de mercancías", "Descuento de renta", "Venta de clientes", "Depreciación de activos"]
)

def registrar_transaccion(transaccion):
    transaccion["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
    st.session_state.transacciones.append(transaccion)
    actualizar_balances(transaccion)
    st.success("Transacción registrada correctamente.")


def mostrar_firmas():
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown("**Propietario**")
        st.image("./firmas/firma_propietario.png", width=150)  
        st.markdown("Alan Díaz Vera")
        st.markdown("""<div style="border-bottom: 2px solid black; width: 80%;"></div>""", 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Revisó**")
        st.image("./firmas/firma_revisor.png", width=150)  
        st.markdown("Nuria González Zúñiga")
        st.markdown("""<div style="border-bottom: 2px solid black; width: 80%;"></div>""", 
                   unsafe_allow_html=True)

if option == "Asiento de apertura":
    st.subheader("Asiento de Apertura")
    caja = st.number_input("Caja", value=50000)
    bancos = st.number_input("Bancos", value=1500000)
    mercancias = st.number_input("Mercancías", value=500000)
    terrenos = st.number_input("Terrenos", value=500000)
    edificios = st.number_input("Edificios", value=1000000)
    eq_computo = st.number_input("Equipo de cómputo", value=150000)
    mob_equipo = st.number_input("Mobiliario y equipo", value=70000)
    muebles_enseres = st.number_input("Muebles y enseres", value=30000)
    capital_social = st.number_input("Capital Social", value=3800000)

    if st.button("Registrar Asiento de Apertura"):
        transaccion = {
            "tipo": "Asiento de apertura",
            "cargos": {
                "Caja": caja,
                "Bancos": bancos,
                "Mercancías": mercancias,
                "Terrenos": terrenos,
                "Edificios": edificios,
                "Equipo de cómputo": eq_computo,
                "Mobiliario y equipo": mob_equipo,
                "Muebles y enseres": muebles_enseres
            },
            "abonos": {
                "Capital Social": capital_social
            }
        }
        registrar_transaccion(transaccion)

elif option == "Compra en efectivo":
    st.subheader("Compra en Efectivo")
    mercancias = st.number_input("Mercancías", value=15000)
    iva = st.number_input("IVA", value=2400)
    caja = st.number_input("Caja", value=17400)

    if st.button("Registrar Compra en Efectivo"):
        transaccion = {
            "tipo": "Compra en efectivo",
            "cargos": {
                "Mercancías": mercancias,
                "IVA pagado": iva
            },
            "abonos": {
                "Caja": caja
            }
        }
        registrar_transaccion(transaccion)

elif option == "Compra a crédito":
    st.subheader("Compra a Crédito")
    equipo_transporte = st.number_input("Equipo de transporte", value=500000)
    iva = st.number_input("IVA", value=80000)
    acreedores = st.number_input("Acreedores", value=580000)

    if st.button("Registrar Compra a Crédito"):
        transaccion = {
            "tipo": "Compra a crédito",
            "cargos": {
                "Equipo de transporte": equipo_transporte,
                "IVA por acreditar": iva
            },
            "abonos": {
                "Acreedores": acreedores
            }
        }
        registrar_transaccion(transaccion)

elif option == "Compra combinada":
    st.subheader("Compra Combinada")
    mercancias = st.number_input("Mercancías", value=20000)
    iva = st.number_input("IVA", value=1600)
    ivaA= st.number_input("IVA por acreditar", value=1600)
    caja = st.number_input("Caja (pago en efectivo)", value=11600)
    documentos_por_pagar = st.number_input("Documentos por pagar (crédito)", value=11600)

    if st.button("Registrar Compra Combinada"):
        transaccion = {
            "tipo": "Compra combinada",
            "cargos": {
                "Mercancías": mercancias,
                "IVA pagado": iva,
                "IVA por acreditar": ivaA
            },
            "abonos": {
                "Caja": caja,
                "Documentos por pagar": documentos_por_pagar
            }
        }
        registrar_transaccion(transaccion)

elif option == "Anticipo de clientes":
    st.subheader("Anticipo de Clientes")
    anticipo = st.number_input("Anticipo de clientes", value=8000)
    iva = st.number_input("IVA", value=1280)
    caja = st.number_input("Caja", value=9280)

    if st.button("Registrar Anticipo de Clientes"):
        transaccion = {
            "tipo": "Anticipo de clientes",
            "cargos": {
                "Caja": caja
            },
            "abonos": {
                "Anticipo de clientes": anticipo,
                "IVA trasladado": iva
            }
        }
        registrar_transaccion(transaccion)

elif option == "Compra de papelería":
    st.subheader("Compra de Papelería")
    papelería = st.number_input("Papelería", value=800)
    iva = st.number_input("IVA", value=128)
    caja = st.number_input("Caja", value=928)

    if st.button("Registrar Compra de Papelería"):
        transaccion = {
            "tipo": "Compra de papelería",
            "cargos": {
                "Papelería": papelería,
                "IVA pagado": iva
            },
            "abonos": {
                "Caja": caja
            }
        }
        registrar_transaccion(transaccion)

elif option == "Pago de rentas anticipadas":
    st.subheader("Pago de Rentas Anticipadas")
    rentas = st.number_input("Rentas pagadas por anticipado", value=6250)
    iva = st.number_input("IVA", value=1000)
    caja = st.number_input("Caja", value=7250)

    if st.button("Registrar Pago de Rentas Anticipadas"):
        transaccion = {
            "tipo": "Pago de rentas anticipadas",
            "cargos": {
                "Rentas pagadas por anticipado": rentas,
                "IVA pagado": iva
            },
            "abonos": {
                "Caja": caja
            }
        }
        registrar_transaccion(transaccion)

elif option == "Venta de mercancías":
    st.subheader("Venta de Mercancías")
    bancos = st.number_input("Bancos", value=348000)
    venta = st.number_input("Venta", value=300000)
    iva_trasladado = st.number_input("IVA trasladado", value=48000)
    costo_venta = st.number_input("Costo de lo vendido", value=150000)
    mercancias = st.number_input("Mercancías", value=150000)

    if st.button("Registrar Venta de Mercancías"):
        transaccion = {
            "tipo": "Venta de mercancías",
            "cargos": {
                "Bancos": bancos,
                "Costo de lo vendido": costo_venta
            },
            "abonos": {
                "Venta": venta,
                "IVA trasladado": iva_trasladado,
                "Mercancías": mercancias
            }
        }
        registrar_transaccion(transaccion)

elif option == "Descuento de renta":
    st.subheader("Descuento de Renta")
    gastos_generales = st.number_input("Gastos generales", value=3125)
    rentas_anticipadas = st.number_input("Rentas pagadas por anticipado", value=3125)

    if st.button("Registrar Descuento de Renta"):
        transaccion = {
            "tipo": "Descuento de renta",
            "cargos": {
                "Gastos generales": gastos_generales
            },
            "abonos": {
                "Rentas pagadas por anticipado": rentas_anticipadas
            }
        }
        registrar_transaccion(transaccion)

elif option == "Venta de clientes":
    st.subheader("Venta de Clientes")
    clientes = st.number_input("Clientes", value=9280)
    anticipo_clientes = st.number_input("Anticipo de clientes", value=8000)
    iva_trasladado = st.number_input("IVA trasladado", value=0)
    iva_por_trasladar = st.number_input("IVA por trasladar", value=1280)
    venta = st.number_input("Venta", value=16000)
    costo_venta = st.number_input("Costo de lo vendido", value=8000)
    mercancias = st.number_input("Mercancías", value=8000)

    if st.button("Registrar Venta de Clientes"):
        transaccion = {
            "tipo": "Venta de clientes",
            "cargos": {
                "Clientes": clientes,
                "Anticipo de clientes": anticipo_clientes,
                "Costo de lo vendido": costo_venta
            },
            "abonos": {
                
                "IVA trasladado": iva_trasladado,
                "IVA por trasladar": iva_por_trasladar,
                "Venta": venta,
                "Mercancías": mercancias
            }
        }
        registrar_transaccion(transaccion)

elif option == "Depreciación de activos":
    st.subheader("Depreciación de Activos")
    gastos_generales = st.number_input("Gastos generales", value=19166.67)
    dep_edificios = st.number_input("Depreciación Acumulada Edificios", value=4166.67)
    dep_eq_computo = st.number_input("Depreciación Acumulada Equipo de cómputo", value=3750)
    dep_mob_equipo = st.number_input("Depreciación Acumulada Mobiliario y equipo", value=583.33)
    dep_muebles_enseres = st.number_input("Depreciación Acumulada Muebles y enseres", value=250)
    dep_eq_transporte = st.number_input("Depreciación Acumulada Equipo de transporte", value=10416.67)

    if st.button("Registrar Depreciación de Activos"):
        transaccion = {
            "tipo": "Depreciación de activos",
            "cargos": {
                "Gastos generales": gastos_generales
            },
            "abonos": {
                "Depreciación Acumulada Edificios": dep_edificios,
                "Depreciación Acumulada Equipo de cómputo": dep_eq_computo,
                "Depreciación Acumulada Mobiliario y equipo": dep_mob_equipo,
                "Depreciación Acumulada Muebles y enseres": dep_muebles_enseres,
                "Depreciación Acumulada Equipo de transporte": dep_eq_transporte
            }
        }
        registrar_transaccion(transaccion)

mostrar_estado_resultados()
mostrar_firmas()
mostrar_balance_general()
mostrar_firmas()
mostrar_estado_cambios_capital()
mostrar_firmas()
mostrar_estado_flujo_efectivo()
mostrar_firmas()

st.subheader("Libro Diario")
for transaccion in st.session_state.transacciones:
    st.write(f"**Transacción:** {transaccion['tipo']} - **Fecha:** {transaccion['fecha']}")
    
    cargos = pd.DataFrame.from_dict(transaccion["cargos"], orient="index", columns=["Monto"])
    cargos["Monto"] = cargos["Monto"].abs()  
    
    abonos = pd.DataFrame.from_dict(transaccion["abonos"], orient="index", columns=["Monto"])
    abonos["Monto"] = abonos["Monto"].abs()  
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Cargos**")
        st.dataframe(cargos)
    with col2:
        st.write("**Abonos**")
        st.dataframe(abonos)
    st.write("---")


st.subheader("Balanza de Comprobación")

balanza = {
    "Cuenta": (
        list(st.session_state.balances["Activo"].keys()) +  
        list(st.session_state.balances["Pasivo"].keys()) +  
        [cuenta for cuenta in st.session_state.balances["Capital"].keys() if cuenta != "Utilidad del Periodo"] +  
        list(st.session_state.balances["Extra"].keys())  
    ),
    "Movimientos Debe": (
        [max(0, st.session_state.balances["Activo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Activo"]] +  
        [max(0, st.session_state.balances["Pasivo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Pasivo"]] +  
        [max(0, st.session_state.balances["Capital"].get(cuenta, 0)) for cuenta in st.session_state.balances["Capital"] if cuenta != "Utilidad del Periodo"] + 
        [max(0, st.session_state.balances["Extra"].get(cuenta, 0)) for cuenta in st.session_state.balances["Extra"]]  
    ),
    "Movimientos Haber": (
        [max(0, -st.session_state.balances["Activo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Activo"]] +  
        [max(0, -st.session_state.balances["Pasivo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Pasivo"]] +  
        [max(0, -st.session_state.balances["Capital"].get(cuenta, 0)) for cuenta in st.session_state.balances["Capital"] if cuenta != "Utilidad del Periodo"] +  
        [max(0, -st.session_state.balances["Extra"].get(cuenta, 0)) for cuenta in st.session_state.balances["Extra"]]  
    ),
    "Saldos Debe": (
        [max(0, st.session_state.balances["Activo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Activo"]] +  
        [max(0, st.session_state.balances["Pasivo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Pasivo"]] +  
        [max(0, st.session_state.balances["Capital"].get(cuenta, 0)) for cuenta in st.session_state.balances["Capital"] if cuenta != "Utilidad del Periodo"] +  
        [max(0, st.session_state.balances["Extra"].get(cuenta, 0)) for cuenta in st.session_state.balances["Extra"]]  
    ),
    "Saldos Haber": (
        [max(0, -st.session_state.balances["Activo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Activo"]] +  
        [max(0, -st.session_state.balances["Pasivo"].get(cuenta, 0)) for cuenta in st.session_state.balances["Pasivo"]] +  
        [max(0, -st.session_state.balances["Capital"].get(cuenta, 0)) for cuenta in st.session_state.balances["Capital"] if cuenta != "Utilidad del Periodo"] +  
        [max(0, -st.session_state.balances["Extra"].get(cuenta, 0)) for cuenta in st.session_state.balances["Extra"]]  
    )
}

balanza_df = pd.DataFrame(balanza)

total_movimientos_debe = balanza_df["Movimientos Debe"].sum()
total_movimientos_haber = balanza_df["Movimientos Haber"].sum()
total_saldos_debe = balanza_df["Saldos Debe"].sum()
total_saldos_haber = balanza_df["Saldos Haber"].sum()

st.dataframe(balanza_df)

st.write(f"**Total Movimientos Debe:** {total_movimientos_debe}")
st.write(f"**Total Movimientos Haber:** {total_movimientos_haber}")
st.write(f"**Total Saldos Debe:** {total_saldos_debe}")
st.write(f"**Total Saldos Haber:** {total_saldos_haber}")



st.subheader("Libro Mayor")

for cuenta, movimientos in st.session_state.libro_mayor.items():
    st.write(f"**Cuenta:** {cuenta}")
    
    cargos = movimientos["Cargos"]
    abonos = movimientos["Abonos"]

    data = []
    
    for i, cargo in enumerate(cargos):
        data.append({"Movimiento": f"Cargo {i+1}", "Monto": cargo, "Tipo": "Cargo"})
    
    for i, abono in enumerate(abonos):
        data.append({"Movimiento": f"Abono {i+1}", "Monto": abono, "Tipo": "Abono"})
    
    df_cuenta = pd.DataFrame(data)
    
    total_cargos = sum(cargos)
    total_abonos = sum(abonos)
    diferencia = total_cargos - total_abonos
    if diferencia > 0:
        mayor = "Cargos"
    elif diferencia < 0:
        mayor = "Abonos"
    else:
        mayor = "Iguales"
    
    df_totales = pd.DataFrame({
        "Movimiento": ["Totales"],
        "Monto": [abs(diferencia)],
        "Tipo": [mayor]
    })
    
    df_final = pd.concat([df_cuenta, df_totales], ignore_index=True)
    
    st.dataframe(df_final)
    st.write("---")
