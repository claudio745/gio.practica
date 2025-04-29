function crearBotonVerMas(enlace, color = 'blue') {
    return `<div class="text-center mt-3">
      <a href="${enlace}" target="_blank"
        class="inline-block bg-${color}-600 text-white px-4 py-1.5 rounded hover:bg-${color}-700 transition">
        Ver más
      </a>
    </div>`;
  }
  
  function crearCard(color, titulo, atributos, enlace) {
    const card = document.createElement('div');
    card.className = `bg-${color}-100 border-l-4 border-${color}-500 rounded-lg shadow-lg p-6 hover:shadow-xl transition text-base space-y-1 max-w-xs h-200 flex flex-col justify-between overflow-hidden`;
  
    const lista = atributos.map(([label, valor]) =>
      `<li><strong>${label}:</strong> ${valor}</li>`).join('');
  
    card.innerHTML = `
      <h3 class="text-xl font-semibold text-${color}-600 mb-2 break-words">${titulo}</h3>
      <ul class="list-disc pl-5 space-y-1 text-lg flex-1 overflow-y-auto">${lista}</ul>
      ${crearBotonVerMas(enlace, color)}
    `;
    
    return card;
  }
  
  
  
  export const renderers = {
    scraper1: fondo => crearCard('blue', fondo.nombre, [
      ['Estado', fondo.estado],
      ['Ubicación', fondo.ubicacion],
      ['Origen', fondo.origen],
      ['Beneficiarios', fondo.beneficiarios],
      ['Fechas', fondo.fechas],
      ['Montos', fondo.montos]
    ], fondo.link),
  
    scraper2: fondo => crearCard('green', fondo.titulo, [
      ['Subdirección', fondo.subdireccion],
      ['Inicio', fondo.fecha_inicio],
      ['Cierre', fondo.fecha_cierre],
      ['Fallo', fondo.fecha_fallo]
    ], fondo.enlace_ver_mas),
  
    scraper3: fondo => crearCard('purple', fondo.titulo, [
      ['Categoría', fondo.categoria],
      ['Cierre', fondo.fecha_cierre]
    ], fondo.enlace),
  
    scraper4: fondo => crearCard('pink', fondo.titulo, [
      ['Fecha inicio', fondo.fecha_inicio],
      ['Fecha cierre', fondo.fecha_termino]
    ], fondo.enlace)
  };
  