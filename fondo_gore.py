#!/usr/bin/env python
# coding: utf-8

# In[13]:


import requests
from bs4 import BeautifulSoup
import logging
import json

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de logs (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato de los logs
    handlers=[
        logging.FileHandler("gore_valparaiso.log"),  # Cambiamos el nombre del archivo de logs
        logging.StreamHandler()  # Muestra los logs en la consola
    ]
)

# URL de la página
url = "http://www.fondosconcursables.gorev.cl/bases.php"

try:
    # Log: Inicio del proceso
    logging.info(f"Iniciando solicitud HTTP a la URL: {url}")

    # Realizar la solicitud HTTP
    response = requests.get(url, timeout=10)  # Agregamos un timeout para evitar bloqueos

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        logging.info("Solicitud HTTP exitosa. Procesando contenido HTML...")
        
        # Parsear el contenido HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar todos los bloques con la clase "col-md-12" (posibles títulos de concursos)
        col_md_12_divs = soup.find_all('div', class_='col-md-12')
        if not col_md_12_divs:
            logging.error("No se encontraron divs con la clase 'col-md-12'.")
            raise ValueError("Divs 'col-md-12' no encontrados.")

        # Filtrar solo los bloques que corresponden a concursos
        titulos_concursos = []
        for col_md_12_div in col_md_12_divs:
            card_body = col_md_12_div.find('div', class_='card-body')
            if card_body and (titulo_element := card_body.find('h5', class_='card-title')):
                titulo = titulo_element.text.strip()
                if "línea" in titulo.lower():  # Filtrar por palabra clave
                    titulos_concursos.append(titulo)
                    logging.info(f"Título de concurso encontrado: {titulo}")
                else:
                    logging.warning(f"Título ignorado (no es un concurso): {titulo}")
            else:
                logging.warning("No se encontró el elemento <h5 class='card-title'> dentro de 'card-body'.")

        # Buscar todos los bloques con la clase "col-md-6" (fechas de inicio y término)
        col_md_6_divs = soup.find_all('div', class_='col-md-6')
        if not col_md_6_divs:
            logging.error("No se encontraron divs con la clase 'col-md-6'.")
            raise ValueError("Divs 'col-md-6' no encontrados.")

        # Lista para almacenar todos los concursos
        concursos = []

        # Iterar sobre cada título de concurso filtrado
        for i, titulo in enumerate(titulos_concursos):
            # Asociar las fechas correspondientes al concurso actual
            fecha_inicio, fecha_termino = None, None

            # Cada concurso tiene dos bloques de fechas (inicio y término)
            start_index = i * 2  # Cada concurso tiene 2 bloques de fechas
            end_index = start_index + 2

            for col_md_6_div in col_md_6_divs[start_index:end_index]:
                # Buscar el título dentro del "card-header"
                if (card_header := col_md_6_div.find('div', class_='card-header')) and \
                   (titulo_fecha_element := card_header.find('h5', class_='card-title')):
                    titulo_fecha = titulo_fecha_element.text.strip()

                    # Buscar el contenido del "card-body"
                    if (card_body_fecha := col_md_6_div.find('div', class_='card-body')) and \
                       (card_text_fecha := card_body_fecha.find('p', class_='card-text')):
                        fecha = card_text_fecha.text.strip()

                        # Clasificar la fecha según el título
                        if "inicio" in titulo_fecha.lower():
                            fecha_inicio = fecha
                            logging.info(f"Fecha de inicio encontrada: {fecha_inicio}")
                        elif "cierre" in titulo_fecha.lower() or "término" in titulo_fecha.lower():
                            fecha_termino = fecha
                            logging.info(f"Fecha de término encontrada: {fecha_termino}")
                    else:
                        logging.warning("No se encontró el elemento <p class='card-text'>.")
                else:
                    logging.error("No se encontró el elemento <h5 class='card-title'> o <div class='card-header'>.")

            # Almacenar el concurso en la lista
            concursos.append({
                "titulo": titulo,
                "fecha_inicio": fecha_inicio,
                "fecha_termino": fecha_termino
            })

        # Guardar los resultados en un archivo JSON
        with open("concursos_gore_valparaiso.json", "w", encoding="utf-8") as json_file:
            json.dump(concursos, json_file, ensure_ascii=False, indent=4)
            logging.info("Resultados guardados en el archivo 'concursos_gore_valparaiso.json'.")

        # Mostrar resultados finales
        print("-" * 50)
        print("Resultados Finales:")
        for i, concurso in enumerate(concursos, start=1):
            print(f"Concurso {i}:")
            print(f"Título: {concurso['titulo']}")
            print(f"Fecha de inicio: {concurso['fecha_inicio']}")
            print(f"Fecha de término: {concurso['fecha_termino']}")
            print("-" * 50)

    else:
        logging.error(f"No se pudo acceder a la página. Código de estado: {response.status_code}")
        raise ConnectionError(f"Error: No se pudo acceder a la página. Código de estado: {response.status_code}")

except requests.exceptions.RequestException as e:
    # Log: Error de conexión
    logging.error(f"Error de conexión: {e}")
    print(f"Error de conexión: {e}")

except Exception as e:
    # Log: Cualquier otro error
    logging.error(f"Error inesperado: {e}")
    print(f"Error inesperado: {e}")


# In[ ]:




