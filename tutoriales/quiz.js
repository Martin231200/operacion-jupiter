// Baraja una copia del arreglo (Fisher-Yates) sin modificar el original
function barajar(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function renderQuiz(containerId, preguntas) {
  const root = document.getElementById(containerId);
  if (!root) return;
  preguntas.forEach((p, i) => {
    const card = document.createElement('div');
    card.className = 'quiz-card';

    const qEl = document.createElement('p');
    qEl.className = 'quiz-question';
    qEl.textContent = (i + 1) + '. ' + p.q;
    card.appendChild(qEl);

    const optsWrap = document.createElement('div');
    optsWrap.className = 'quiz-options';

    const feedback = document.createElement('div');
    feedback.className = 'quiz-feedback';

    // Cada opción conserva su posición original para saber cuál es la correcta
    const ordenadas = barajar(p.opciones.map((texto, original) => ({ texto, original })));
    let botonCorrecto = null;

    ordenadas.forEach((item) => {
      const op = item.texto;
      const btn = document.createElement('button');
      btn.textContent = op;
      btn.onclick = () => {
        Array.from(optsWrap.children).forEach(b => b.disabled = true);
        feedback.style.display = 'block';
        if (item.original === p.correcta) {
          btn.classList.add('correct');
          feedback.classList.add('correct');
          feedback.innerHTML = '<span class="quiz-icon">&#10003;</span>Correcto. ' + p.exp;
        } else {
          btn.classList.add('incorrect');
          feedback.classList.add('incorrect');
          feedback.innerHTML = '<span class="quiz-icon">&#10007;</span>No exactamente. ' + p.exp;
          botonCorrecto.classList.add('correct');
        }
      };
      if (item.original === p.correcta) botonCorrecto = btn;
      optsWrap.appendChild(btn);
    });

    card.appendChild(optsWrap);
    card.appendChild(feedback);
    root.appendChild(card);
  });
}
