#!/usr/bin/env python
# coding: utf-8

# # Pagina https://www.fondosdecultura.cl/area/

# In[1]:


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging

# Configuración del sistema de logs
logging.basicConfig(
    filename="fondos_cultura_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_info(message):
    """Función para registrar mensajes informativos."""
    print(message)
    logging.info(message)

def log_error(message):
    """Función para registrar mensajes de error."""
    print(f"❌ {message}")
    logging.error(message)

# Lista de categorías
urls = [
    "arquitectura", "artes-visuales", "artes-escenicas", "artesania", "audiovisual", "circo", "evaluadores",
    "danza", "diseno", "economia-creativa", "educacion", "folclor", "formacion-residencias", "fotografia",
    "gestion-cultural", "infraestructura", "interdisciplinas", "libro-lectura", "micsur", "musica",
    "narracion-oral", "nuevos-medios", "opera", "organizaciones", "patrimonio", "pueblos-originarios",
    "regiones", "teatro", "titeres", "turismo-cultural"
]

url_base = "https://www.fondosdecultura.cl/area/{}/"

def guardar_en_json(datos, archivo="fondos_cultura.json"):
    """Guarda los datos en un archivo JSON."""
    try:
        # Leer el archivo existente (si existe) para agregar nuevos datos
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                data_existente = json.load(f)
        except FileNotFoundError:
            data_existente = []

        # Agregar las nuevas convocatorias al archivo existente
        data_existente.extend(datos)

        # Guardar los datos actualizados en el archivo JSON
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(data_existente, f, ensure_ascii=False, indent=4)

        log_info(f"Datos guardados exitosamente en {archivo}")
    except Exception as e:
        log_error(f"Error al guardar en JSON: {e}")

def obtener_convocatoria():
    """Obtiene y procesa las convocatorias abiertas."""
    convocatorias_abiertas = []  # Lista para almacenar las convocatorias abiertas

    for categoria in urls:
        url = url_base.format(categoria)

        try:
            # Realizar la solicitud HTTP
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Lanzar excepción si hay un error HTTP

            # Parsear el contenido HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Buscar todos los divs con clase "col-md-4" (las convocatorias)
            convocatorias = soup.find_all("div", class_="col-md-4")
            if not convocatorias:
                log_info(f"Página {url} sin convocatorias")
                continue

            # Bandera para verificar si hay al menos una convocatoria abierta
            hay_convocatorias_abiertas = False

            # Procesar cada convocatoria
            for convocatoria in convocatorias:
                try:
                    # Extraer el título desde el <h5 class="card-title">
                    titulo = convocatoria.find("h5", class_="card-title").text.strip()

                    # Extraer el enlace desde el <a href>
                    link = convocatoria.find("a")["href"]

                    # Extraer las fechas desde el <p class="card-text">
                    fecha_texto = convocatoria.find("p", class_="card-text").text.strip()

                    # Verificar si la fecha de cierre está presente
                    if "Fecha de cierre:" in fecha_texto:
                        # Extraer la fecha de cierre
                        fecha_cierre_str = fecha_texto.replace("Fecha de cierre:", "").strip()
                        try:
                            # Convertir la fecha de cierre a un objeto datetime
                            fecha_cierre = datetime.strptime(fecha_cierre_str, "%d/%m/%Y - %H:%M")
                            hoy = datetime.now()

                            # Clasificar como abierta si la fecha de cierre es posterior a hoy
                            if fecha_cierre > hoy:
                                hay_convocatorias_abiertas = True

                                # Datos de la convocatoria abierta
                                convocatoria_data = {
                                    "categoria": categoria,
                                    "titulo": titulo,
                                    "enlace": link,
                                    "fecha_cierre": fecha_cierre_str
                                }

                                # Agregar los datos a la lista de convocatorias abiertas
                                convocatorias_abiertas.append(convocatoria_data)

                                # Imprimir los datos de la convocatoria abierta
                                log_info(f"✅ Convocatoria ABIERTA encontrada:")
                                log_info(f"🔗 Enlace: {link}")
                                log_info(f"📝 Título: {titulo}")
                                log_info(f"📅 Fecha de cierre: {fecha_cierre_str}")
                                log_info("-" * 40)

                        except ValueError:
                            # Ignorar convocatorias con formato de fecha inválido
                            log_error(f"Formato de fecha inválido: {fecha_cierre_str}")
                            continue

                except Exception as e:
                    log_error(f"Error al procesar una convocatoria en {url}: {e}")

            # Si no se encontraron convocatorias abiertas, imprimir mensaje
            if not hay_convocatorias_abiertas:
                log_info(f"Página {url} sin convocatorias abiertas")

        except requests.exceptions.HTTPError as http_err:
            log_error(f"Error HTTP al acceder a {url}: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            log_error(f"Error de conexión al acceder a {url}: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            log_error(f"Tiempo de espera agotado al acceder a {url}: {timeout_err}")
        except Exception as e:
            log_error(f"Error inesperado al acceder a {url}: {e}")

    # Guardar todas las convocatorias abiertas en un archivo JSON
    if convocatorias_abiertas:
        guardar_en_json(convocatorias_abiertas)

if __name__ == "__main__":
    obtener_convocatoria()


# In[ ]:




