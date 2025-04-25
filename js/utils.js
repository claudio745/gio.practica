export const eventosInactividad = ['mousedown', 'wheel', 'keydown', 'touchstart', 'mousemove'];
let scrollInterval = null;
let temporizadorInactividad;
let subiendo = false;
const TIEMPO_SIN_INTERACCION = 10000;

export function iniciarScrollAutomatico() {
  if (scrollInterval) return;

  scrollInterval = setInterval(() => {
    const { scrollY, innerHeight } = window;
    const scrollHeight = document.documentElement.scrollHeight;

    if (scrollY + innerHeight >= scrollHeight - 1 && !subiendo) subiendo = true;

    window.scrollBy({ top: subiendo ? -2 : 2, behavior: 'smooth' });

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
