import { renderers } from './renderers.js';

function cargarDatosScraper(url, contenedorId, callback) {
  const container = document.getElementById(contenedorId);
  
  if (!container) {
    return;
  }

  // Mostrar spinner
  container.innerHTML = '<div class="spinner">Cargando...</div>';

  fetch(url + '?_=' + new Date().getTime()) // para evitar cache
    .then(response => response.json())
    .then(data => {
      container.innerHTML = ''; // Limpiar contenido previo
      data.forEach(item => {
        const card = callback(item);
        container.appendChild(card);
      });
    })
    .catch(error => {
      console.error('Error al cargar datos:', error);
      container.innerHTML = '<div class="error">Error al cargar los datos.</div>';
    });
}

const fuentes = [
  ['json/fondos_gob.json', 'scraper1-data', renderers.scraper1],
  ['json/fondos_anid.json', 'scraper2-data', renderers.scraper2],
  ['json/fondos_cultura.json', 'scraper3-data', renderers.scraper3],
  ['json/concursos_gore_valparaiso.json', 'scraper4-data', renderers.scraper4]
];

export function cargarTodosLosDatos() {
  fuentes.forEach(([url, contenedorId, renderer]) => {
    cargarDatosScraper(url, contenedorId, renderer);
  });
}


cargarTodosLosDatos();


setInterval(() => {
  const scrollY = window.scrollY;
  cargarTodosLosDatos();
  setTimeout(() => {
    window.scrollTo(0, scrollY);
  }, 100); 
}, 30000);  //30 segundos pa probar 

