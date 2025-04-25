import { iniciarScrollAutomatico, reiniciarTemporizadorInactividad, eventosInactividad } from './utils.js';
import { cargarTodosLosDatos } from './dataloader.js';
import { cargarComponentes } from './components.js';

function cargarContenido(url) {
  fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(`Error cargando ${url}`);
      return res.text();
    })
    .then(html => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const nuevoContenido = doc.querySelector('main');
      const contenedor = document.getElementById('contenido-principal');

      if (nuevoContenido && contenedor) {
        contenedor.innerHTML = nuevoContenido.innerHTML;
        history.pushState(null, '', url);
        window.scrollTo(0, 0); // Opcional: scroll al top
        cargarTodosLosDatos(); // Si necesitas volver a cargar los datos dinámicos
      }
    })
    .catch(err => console.error('Error al cargar contenido dinámico:', err));
}

document.addEventListener('DOMContentLoaded', () => {
  // Cargar header y footer
  cargarComponentes('header-fondos', 'components/header.html');
  cargarComponentes('footer-fondos', 'components/footer.html');

  // Cargar datos iniciales
  cargarTodosLosDatos();

  // Configurar scroll automático por inactividad
  eventosInactividad.forEach(evento => {
    window.addEventListener(evento, reiniciarTemporizadorInactividad);
  });
  window.addEventListener('load', reiniciarTemporizadorInactividad);

  // Interceptar clics de navegación interna
  document.body.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (link && link.href && link.origin === location.origin && !link.target) {
      const ruta = link.pathname;

      if (['/gobierno.html', '/anid.html', '/cultura.html', '/gore.html'].includes(ruta)) {
        e.preventDefault();
        cargarContenido(ruta);
      }
    }
  });

  // Manejar navegación con botones del navegador
  window.addEventListener('popstate', () => {
    cargarContenido(location.pathname);
  });
});
