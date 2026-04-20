const form = document.getElementById("submission-form");
const list = document.getElementById("submission-list");
const idInput = document.getElementById("submission-id");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const messageInput = document.getElementById("message");
const submitBtn = document.getElementById("submit-btn");
const cancelBtn = document.getElementById("cancel-btn");

async function api(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "API error");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function resetForm() {
  form.reset();
  idInput.value = "";
  submitBtn.textContent = "Ajouter";
  cancelBtn.hidden = true;
}

function renderItem(item) {
  const li = document.createElement("li");

  li.innerHTML = `
    <div class="item-head">
      <strong>${item.name}</strong>
      <small>${new Date(item.created_at).toLocaleString()}</small>
    </div>
    <p>${item.email}</p>
    <p>${item.message}</p>
    <div class="item-actions">
      <button type="button" data-action="edit" data-id="${item.id}">Modifier</button>
      <button type="button" class="danger" data-action="delete" data-id="${item.id}">Supprimer</button>
    </div>
  `;

  return li;
}

async function loadSubmissions() {
  const items = await api("/submissions");
  list.innerHTML = "";

  for (const item of items) {
    list.appendChild(renderItem(item));
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    name: nameInput.value.trim(),
    email: emailInput.value.trim(),
    message: messageInput.value.trim(),
  };

  const id = idInput.value;
  if (id) {
    await api(`/submissions/${id}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  } else {
    await api("/submissions", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  resetForm();
  await loadSubmissions();
});

cancelBtn.addEventListener("click", () => {
  resetForm();
});

list.addEventListener("click", async (event) => {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement)) {
    return;
  }

  const id = target.dataset.id;
  const action = target.dataset.action;
  if (!id || !action) {
    return;
  }

  if (action === "delete") {
    await api(`/submissions/${id}`, { method: "DELETE" });
    await loadSubmissions();
    return;
  }

  if (action === "edit") {
    const item = await api(`/submissions/${id}`);
    idInput.value = item.id;
    nameInput.value = item.name;
    emailInput.value = item.email;
    messageInput.value = item.message;
    submitBtn.textContent = "Mettre a jour";
    cancelBtn.hidden = false;
  }
});

loadSubmissions().catch((error) => {
  list.innerHTML = `<li>Erreur de chargement: ${error.message}</li>`;
});