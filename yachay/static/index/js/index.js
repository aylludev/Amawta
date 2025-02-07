document.addEventListener("DOMContentLoaded", function() {
  var cy = cytoscape({
    container: document.getElementById('cy'),

    elements: [], // Los datos se cargarán dinámicamente desde Django

    style: [
      {
        selector: 'node',
        style: {
          'background-color': '#007bff',
          'label': 'data(label)',
          'color': '#ffffff',
          'text-valign': 'center',
          'text-halign': 'center',
          'font-size': '14px',
          'width': 40,
          'height': 40,
          'border-width': 2,
          'border-color': '#0056b3'
        }
      },
      {
        selector: 'edge',
        style: {
          'width': 2,
          'line-color': '#cccccc',
          'target-arrow-shape': 'triangle',
          'target-arrow-color': '#cccccc',
          'curve-style': 'bezier'
        }
      },
      {
        selector: 'node:selected',
        style: {
          'background-color': '#ffcc00',
          'border-color': '#ff9900',
          'border-width': 4
        }
      }
    ]
  });

  // Cargar datos desde Django (requiere que configures una API o una vista que devuelva los datos)
  fetch('/yachay/graph_data/')
    .then(response => response.json())
    .then(data => {
      cy.add(data);
      updateNodeSizes();
    });

  // Función para actualizar dinámicamente el tamaño de los nodos
  function updateNodeSizes() {
    cy.nodes().forEach(function(node) {
      let degree = node.degree(); // Cantidad de conexiones
      let newSize = Math.min(40 + degree * 5, 100);

      node.style({
        'width': newSize,
        'height': newSize
      });
    });
  }

  // Escuchar cambios en la estructura del gráfico (agregar/borrar enlaces)
  cy.on('add remove', 'edge', function() {
    updateNodeSizes();
  });
});

let selectedNodes = [];
cy.on('tap', 'node', function(event) {
  let node = event.target;

  // Si ya hemos seleccionado dos nodos, reiniciamos la selección
  if (selectedNodes.length === 2) {
    selectedNodes = [];
  }

  selectedNodes.push(node);

  if (selectedNodes.length === 2) {
    let sourceId = selectedNodes[0].id();
    let targetId = selectedNodes[1].id();

    if (sourceId !== targetId) {
      // Enviar al backend para guardar la relación
      fetch('/yachay/links/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')  // CSRF token para Django
        },
        body: JSON.stringify({ source: sourceId, target: targetId })
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Agregar el enlace al gráfico si la creación en el backend fue exitosa
            cy.add({
              group: 'edges',
              data: { id: `edge_${sourceId}_${targetId}`, source: sourceId, target: targetId }
            });
          } else {
            alert('Error al crear el enlace.');
          }
        })
        .catch(error => console.error('Error:', error));
    }
  }
});

// Función para obtener el CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

cy.on('tap', function(event) {
  if (event.target === cy) {
    // Redirigir a la página de creación de notas
    window.location.href = '/yachay/notes/add';
    console.log(window.location.href);
  }
});

