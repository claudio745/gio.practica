export function cargarComponentes(id, archivo) {
    fetch(archivo)
      .then(res => {
        if (!res.ok) throw new Error(`No se pudo cargar ${archivo}`);
        return res.text();
      })
      .then(html => {
        const container = document.getElementById(id);
        if (container) {
          container.innerHTML = html;
        } else {
          console.warn(`Elemento con id "${id}" no encontrado.`);
        }
      })
      .catch(err => console.error(`Error cargando ${archivo}:`, err));
  }
  