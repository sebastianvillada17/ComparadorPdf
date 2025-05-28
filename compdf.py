import streamlit as st
import fitz  
import re

#Extraer texto de un PDF 
def extraer_texto(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

def convertir_a_float(valor):
   
    valor = valor.strip().replace('.', '').replace(',', '.')
    try:
        return float(valor)
    except ValueError:
        return None
#Extraer datos de precio e IVA de un texto
def extraer_datos(texto):
    
    precio = re.findall(r'Precio\s*:\s*\$?\s*([\d.,]+)', texto, re.IGNORECASE)
    iva = re.findall(r'IVA\s*:\s*\$?\s*([\d.,]+)', texto, re.IGNORECASE)

    precio = [convertir_a_float(p) for p in precio if convertir_a_float(p) is not None]
    iva = [convertir_a_float(i) for i in iva if convertir_a_float(i) is not None]

    return {
        "precio": precio,
        "iva": iva
    }
def listas_iguales(lista1, lista2, tolerancia=0.01):
    
    if len(lista1) != len(lista2):
        return False
    return all(abs(a - b) <= tolerancia for a, b in zip(lista1, lista2))

def comparar_orden_factura(datos_orden, datos_factura):
  
    diferencias = {}
    for campo in ['precio', 'iva']:
        if not listas_iguales(datos_orden[campo], datos_factura[campo]):
            diferencias[campo] = {
                "orden": datos_orden[campo],
                "factura": datos_factura[campo]
            }
    return diferencias


    
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image("logo.png", width=250)

st.markdown(
    "<h1 style='color: #19277f; text-align: center;'>Muelles y Frenos Simon Bolívar</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='background-color: #19277f; color: white; padding: 12px; border-radius: 8px; font-size: 22px; font-weight: bold; text-align: center;'>
        Herramienta de Comparación entre Orden de Compra y Factura
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='color: black; padding: 5px; 
                font-size: 18px; font-weight: bold; margin-top: 5px;'>
        Por favor sube la orden de compra en formato PDF
    </div>
    """,
    unsafe_allow_html=True
)
orden_pdf = st.file_uploader("", type=["pdf"], key="orden")
if orden_pdf:
    st.success(" Orden de compra subida correctamente.")

st.markdown(
    """
    <div style='color: black; padding: 5px; 
                font-size: 18px; font-weight: bold; margin-top: 20px;'>
        Por favor sube la factura en formato PDF
    </div>
    """,
    unsafe_allow_html=True
)
factura_pdf = st.file_uploader("", type=["pdf"], key="factura")
if factura_pdf:
    st.success("Factura subida correctamente.")


if orden_pdf and factura_pdf:
    if st.button("Comparar archivos"):
        try:
            texto_orden = extraer_texto(orden_pdf.read())
            texto_factura = extraer_texto(factura_pdf.read())

            datos_orden = extraer_datos(texto_orden)
            datos_factura = extraer_datos(texto_factura)

            precios_orden = [int(p) for p in datos_orden['precio']]
            ivas_orden = [int(i) for i in datos_orden['iva']]
            precios_factura = [int(p) for p in datos_factura['precio']]
            ivas_factura = [int(i) for i in datos_factura['iva']]

            st.markdown(
                "<h2 style='color: #19277f; text-align: center;'> Datos Extraídos</h2>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"""
                    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #19277f;'>
                        <h4 style='color: #19277f;'>Orden de Compra</h4>
                        <ul style='font-size:16px;'>
                            <li><strong>Precios:</strong> {precios_orden}</li>
                            <li><strong>IVA:</strong> {ivas_orden}</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"""
                    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #fab70e;'>
                        <h4 style='color: #fab70e;'>Factura</h4>
                        <ul style='font-size:16px;'>
                            <li><strong>Precios:</strong> {precios_factura}</li>
                            <li><strong>IVA:</strong> {ivas_factura}</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            diferencias = comparar_orden_factura(datos_orden, datos_factura)

            st.markdown("<hr>", unsafe_allow_html=True)

            if diferencias:
                st.markdown(
                    """
                    <div style='background-color: #ffe6e6; padding: 16px; border-left: 6px solid red; border-radius: 10px;'>
                        <h3 style='color: red;'> Se encontraron diferencias entre la orden de compra y la factura:</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                for campo, vals in diferencias.items():
                    orden_int = [int(x) for x in vals['orden']]
                    factura_int = [int(x) for x in vals['factura']]
                    st.markdown(
                        f"""
                        <div style='background-color: #fff8e1; padding: 12px; border-radius: 8px; margin-top:10px;'>
                            <h4 style='color: #FAB70E;'> {campo.capitalize()}</h4>
                            <ul style='font-size:16px;'>
                                   <li><strong>Orden:</strong> {orden_int}</li>
                                   <li><strong>Factura:</strong> {factura_int}</li>
                            </ul>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    """
                    <div style='background-color: #e8f5e9; padding: 16px; border-left: 6px solid green; border-radius: 10px;'>
                        <h3 style='color: green;'>La orden de compra y la factura coinciden </h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.markdown(
                f"""
                <div style='background-color: #ffebee; padding: 16px; border-left: 6px solid #d32f2f; border-radius: 10px;'>
                    <h4 style='color: #d32f2f;'> Error al procesar los archivos:</h4>
                    <p>{e}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.markdown(
    """
    <div style='background-color: #fab70e; color: #19277f; padding: 12px; border-radius: 8px; font-size: 18px; font-weight: bold; text-align: center;'>
        Por favor, sube ambos archivos en formato PDF para realizar la comparación.
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <hr style='margin-top:40px; margin-bottom:10px;'>
    <div style='background-color: #19277f; padding: 16px 0 10px 0; border-radius: 8px; text-align: center;'>
        <span style='color: white; font-size: 20px; font-weight: bold;'>Síguenos en nuestras redes sociales:</span><br>
        <a href='https://www.facebook.com/RepuestosSimonBolivar/' target='_blank' style='margin:0 10px; color: #fab70e;'>
            <i class='fab fa-facebook fa-2x'></i>
        </a>
        <a href='https://www.instagram.com/repuestossimonbolivar/' target='_blank' style='margin:0 10px; color: #fab70e;'>
            <i class='fab fa-instagram fa-2x'></i>
        </a>
        <a href='https://api.whatsapp.com/send/?phone=573114914780&text&type=phone_number&app_absent=0' target='_blank' style='margin:0 10px; color: #fab70e;'>
            <i class='fab fa-whatsapp fa-2x'></i>
        </a>
        <a href='https://www.youtube.com/@repuestossimonbolivarcolombia/' target='_blank' style='margin:0 10px; color: #fab70e;'>
            <i class='fab fa-youtube fa-2x'></i>
        </a>
        <a href='https://www.tiktok.com/@repuestossimonbolivar/' target='_blank' style='margin:0 10px; color: #fab70e;'>
            <i class='fab fa-tiktok fa-2x'></i>
        </a>
        <a href='https://co.linkedin.com/company/repuestos-simon-bolivar/' target='_blank' style='margin:0 10px; color: #fab70e;'>
            <i class='fab fa-linkedin fa-2x'></i>
        </a>
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """,
    unsafe_allow_html=True
)