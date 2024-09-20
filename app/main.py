import streamlit as st
from models.manage_model import ModelPredictor, CustomTransformer
from datetime import datetime

ORDER_ID = 0
SATURATION = 0
CREATED_AT = ""
TO_USER_DISTANCE = 1
TOTAL_EARNINGS = 1000
DISTANCE_TO_STORE = 0
COUNTRY = "PE"
CITY = "lima"
TIP = 0

city_list_from_file = []
with open("app/various_files/towns.txt", 'r') as file:
  city_list_from_file = file.read().strip().split('\n')
city_list_from_file = tuple(city_list_from_file)


model_predictor = ModelPredictor()
model_predictor.load_model()

st.markdown("""
         <style>
         .big-font1 {
            font-size:30px !important;
            color: yellow !important;
            vertical-align: bottom !important;
            padding-top: 500;
         }
         .big-font2 {
            font-size:30px !important;
            color: green !important;
            vertical-align: bottom !important;
         }
         .big-font3 {
            font-size:30px !important;
            color: red !important;
            vertical-align: bottom !important;
         }
         </style>
         """, unsafe_allow_html=True)
st.markdown(
    f'<div style="text-align: center;"><img src="app/various_files/image.png" style="max-width: 40%; height: auto;"></div>',
    unsafe_allow_html=True
)
st.title("Clasificación de orden tomada/no tomada RAPPI")

# Iniciar el formulario
with st.form(key='my_form'):
    
    # Primera fila con dos columnas para los campos numéricos
    col1, col2 = st.columns(2)
    
    with col1:
        TO_USER_DISTANCE = st.text_input("TO_USER_DISTANCE", value="0")
        
    with col2:
        TOTAL_EARNINGS = st.text_input("TOTAL_EARNINGS", value="0")
    
    # Segunda fila con dos columnas para el campo de fecha y la primera opción múltiple
    col3, col4 = st.columns(2)
    
    with col3:
        CREATED_AT = st.date_input("Seleccione una fecha", value=datetime.today())
    
    with col4:
        DISTANCE_TO_STORE = st.text_input("DISTANCE_TO_STORE", value="0")
    
    # Tercera fila con una columna para la segunda opción múltiple
    col5, col6 = st.columns(2)
    
    with col5:
        COUNTRY = st.selectbox("Seleccione un pais", ("CO", "PE"))
    with col6:
        CITY = st.selectbox("Seleccione una ciudad", city_list_from_file)

    col7, col8 = st.columns(2)
    with col7:
        TIP = st.text_input("TIP", value="0")
    
    # Botón de envío
    submit_button = st.form_submit_button(label='Predecir')

# Mostrar los resultados si el formulario ha sido enviado
if submit_button:
    data_to_classify = {"ORDER_ID": [ORDER_ID],
                    "SATURATION":[SATURATION],
                    "CREATED_AT":[CREATED_AT],
                    "TIP":[TIP],
                    "TO_USER_DISTANCE":[TO_USER_DISTANCE],
                    "TOTAL_EARNINGS":[TOTAL_EARNINGS],
                    "DISTANCE_TO_STORE":[DISTANCE_TO_STORE],
                    "COUNTRY":[COUNTRY],
                    "CITY":[CITY]}

    prediction = model_predictor.run(data_to_classify)

    if prediction==1:
            st.markdown("""
                  <p class="big-font2">La orden fue tomada</p>
                  """,unsafe_allow_html=True)
    elif prediction==0:
            st.markdown("""
                  <p class="big-font3">La orden no fue tomada</p>
                  """,unsafe_allow_html=True)
    



