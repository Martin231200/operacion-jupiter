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

    p.opciones.forEach((op, idx) => {
      const btn = document.createElement('button');
      btn.textContent = op;
      btn.onclick = () => {
        Array.from(optsWrap.children).forEach(b => b.disabled = true);
        feedback.style.display = 'block';
        if (idx === p.correcta) {
          btn.classList.add('correct');
          feedback.classList.add('correct');
          feedback.innerHTML = '<span class="quiz-icon">&#10003;</span>Correcto. ' + p.exp;
        } else {
          btn.classList.add('incorrect');
          feedback.classList.add('incorrect');
          feedback.innerHTML = '<span class="quiz-icon">&#10007;</span>No exactamente. ' + p.exp;
          Array.from(optsWrap.children)[p.correcta].classList.add('correct');
        }
      };
      optsWrap.appendChild(btn);
    });

    card.appendChild(optsWrap);
    card.appendChild(feedback);
    root.appendChild(card);
  });
}
