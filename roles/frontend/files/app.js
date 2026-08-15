const statusEl = document.getElementById("status");
const listEl = document.getElementById("todo-list");
const formEl = document.getElementById("todo-form");
const titleInput = document.getElementById("todo-title");

const api = (path, options) => fetch(`${window.API_BASE_URL}${path}`, options);

async function checkHealth() {
  try {
    const res = await api("/health");
    if (!res.ok) throw new Error("bad status");
    statusEl.textContent = "бэкенд доступен";
    statusEl.className = "status ok";
  } catch (e) {
    statusEl.textContent = "бэкенд недоступен — проверь API_BASE_URL в config.js";
    statusEl.className = "status error";
  }
}

function renderTodo(todo) {
  const li = document.createElement("li");
  li.className = todo.done ? "done" : "";
  li.dataset.id = todo.id;

  const title = document.createElement("span");
  title.className = "title";
  title.textContent = todo.title;
  title.onclick = () => toggleTodo(todo.id);

  const del = document.createElement("button");
  del.className = "delete";
  del.textContent = "✕";
  del.onclick = () => deleteTodo(todo.id);

  li.append(title, del);
  return li;
}

async function loadTodos() {
  const res = await api("/api/todos");
  const todos = await res.json();
  listEl.innerHTML = "";
  todos.forEach((t) => listEl.appendChild(renderTodo(t)));
}

async function toggleTodo(id) {
  await api(`/api/todos/${id}`, { method: "PATCH" });
  loadTodos();
}

async function deleteTodo(id) {
  await api(`/api/todos/${id}`, { method: "DELETE" });
  loadTodos();
}

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = titleInput.value.trim();
  if (!title) return;
  await api("/api/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  titleInput.value = "";
  loadTodos();
});

checkHealth();
loadTodos();
