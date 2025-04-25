export const eventosInactividad = ['mousedown', 'wheel', 'keydown', 'touchstart', 'mousemove'];
let scrollInterval = null;
let temporizadorInactividad;
let subiendo = false;
const TIEMPO_SIN_INTERACCION = 10000;


export const rutas = ['/gobierno.html', '/anid.html', '/cultura.html', '/gore.html'];


export function obtenerSiguienteRuta(rutaActual) {
  const index = rutas.indexOf(rutaActual);
  if (index === -1) return null;
  return rutas[(index + 1) % rutas.length]; // Hace el ciclo
}

function noTieneScroll() {
  return document.documentElement.scrollHeight <= window.innerHeight;
}

export function iniciarScrollAutomatico() {
  if (scrollInterval) return;

  if (noTieneScroll()) {
    const siguienteRuta = obtenerSiguienteRuta(location.pathname);
    if (siguienteRuta) {
      setTimeout(() => {
        window.location.href = siguienteRuta;
      }, 10000); // espera 10 segundos para dar tiempo a leer 
    }
    return;
  }

  scrollInterval = setInterval(() => {
    const { scrollY, innerHeight } = window;
    const scrollHeight = document.documentElement.scrollHeight;

    if (scrollY + innerHeight >= scrollHeight - 1 && !subiendo) {
      const siguienteRuta = obtenerSiguienteRuta(location.pathname);
      if (siguienteRuta) {
        setTimeout(()=>{
          window.location.href = siguienteRuta;
        return;
        },10000);
        
      } else {
        subiendo = true;
      }
    }

    window.scrollBy({ top: subiendo ? -2 : 1.5, behavior: 'smooth' });

    if (scrollY <= 0) subiendo = false;
  }, 50);
}


export function detenerScrollAutomatico() {
  clearInterval(scrollInterval);
  scrollInterval = null;
}

export function reiniciarTemporizadorInactividad() {
  detenerScrollAutomatico();
  clearTimeout(temporizadorInactividad);
  temporizadorInactividad = setTimeout(iniciarScrollAutomatico, TIEMPO_SIN_INTERACCION);
}
