import { iniciarScrollAutomatico, reiniciarTemporizadorInactividad, eventosInactividad } from './utils.js';
import { cargarTodosLosDatos,  } from './dataloader.js';
import { cargarComponentes } from './components.js';

document.addEventListener('DOMContentLoaded', () => {
  cargarTodosLosDatos();
  cargarComponentes('header-fondos', 'components/header.html');
  cargarComponentes('footer-fondos', 'components/footer.html');
  // Scroll automático por inactividad
  eventosInactividad.forEach(evento => {
    window.addEventListener(evento, reiniciarTemporizadorInactividad);
  });

  window.addEventListener('load', reiniciarTemporizadorInactividad);
});
