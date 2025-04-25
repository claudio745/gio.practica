import { iniciarScrollAutomatico, reiniciarTemporizadorInactividad, eventosInactividad } from './utils.js';
import { cargarTodosLosDatos } from './dataloader.js';
import { cargarComponentes } from './components.js';


document.addEventListener('DOMContentLoaded', () => {
  // Cargar header y footer
  cargarComponentes('header-fondos', 'components/header.html');
  cargarComponentes('footer-fondos', 'components/footer.html');

  // Cargar datos iniciales
  cargarTodosLosDatos();
  reiniciarTemporizadorInactividad();
  eventosInactividad.forEach(evento => {
    window.addEventListener(evento, reiniciarTemporizadorInactividad);
  });

  // Manejar navegación con botones del navegador
  window.addEventListener('popstate', () => {
    cargarContenido(location.pathname);
  });
});
