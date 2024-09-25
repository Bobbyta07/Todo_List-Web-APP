document.getElementById('addTaskBtn').addEventListener('click', addTask);

function addTask() {
  const taskInput = document.getElementById('taskInput').value;
  const timerInput = document.getElementById('timerInput').value;

  if (taskInput === '' || timerInput === '') {
    alert('Please enter both a task and a timer.');
    return;
  }

  // Create a new list item (task)
  const listItem = document.createElement('li');
  listItem.className = 'list-group-item';

  const taskSpan = document.createElement('span');
  taskSpan.className = 'mod'
  taskSpan.innerText = taskInput;

  const timerSpan = document.createElement('span');
  timerSpan.className = 'badge bg-success';
  timerSpan.innerText = `${timerInput} minutes`;

  const removeBtn = document.createElement('button');
  removeBtn.className = 'btn btn-danger btn-sm';
  removeBtn.innerText = 'Remove';
  removeBtn.addEventListener('click', () => listItem.remove());

  listItem.appendChild(taskSpan);
  listItem.appendChild(timerSpan);
  listItem.appendChild(removeBtn);

  document.getElementById('todoList').appendChild(listItem);

  // Start countdown
  startCountdown(timerInput, timerSpan);

  // Clear input fields
  document.getElementById('taskInput').value = '';
  document.getElementById('timerInput').value = '';
}

function startCountdown(minutes, timerSpan) {
  let timeRemaining = minutes * 60;

  const countdown = setInterval(() => {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;

    timerSpan.innerText = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

    if (timeRemaining <= 0) {
      clearInterval(countdown);
      timerSpan.innerText = 'Time up!';
      timerSpan.classList.replace('bg-success', 'bg-danger');
    }

    timeRemaining--;
  }, 1000);
}
