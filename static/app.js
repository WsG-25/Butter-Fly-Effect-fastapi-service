const API = {
  products: "/products",
  dbCheck: "/db-check",
};

const form = document.getElementById("product-form");
const formTitle = document.getElementById("form-title");
const productIdInput = document.getElementById("product-id");
const submitBtn = document.getElementById("submit-btn");
const cancelEditBtn = document.getElementById("cancel-edit");
const formMessage = document.getElementById("form-message");
const productsBody = document.getElementById("products-body");
const dbStatus = document.getElementById("db-status");
const catalogSummary = document.getElementById("catalog-summary");

const EMPTY_COLSPAN = 7;

function showMessage(text, type = "success") {
  formMessage.textContent = text;
  formMessage.className = `message visible ${type}`;
}

function clearMessage() {
  formMessage.textContent = "";
  formMessage.className = "message";
}

function formatMoney(value) {
  return Number(value).toFixed(2);
}

function getFormPayload() {
  return {
    name: document.getElementById("name").value.trim(),
    unit: document.getElementById("unit").value,
    cost_per_unit: parseFloat(document.getElementById("cost_per_unit").value),
    price_per_unit: parseFloat(document.getElementById("price_per_unit").value),
    quantity_in_stock: parseInt(
      document.getElementById("quantity_in_stock").value,
      10
    ),
  };
}

function resetForm() {
  form.reset();
  productIdInput.value = "";
  formTitle.textContent = "Add product";
  submitBtn.textContent = "Save product";
  cancelEditBtn.hidden = true;
  clearMessage();
}

function startEdit(product) {
  productIdInput.value = String(product.id);
  document.getElementById("name").value = product.name;
  document.getElementById("unit").value = product.unit;
  document.getElementById("cost_per_unit").value = product.cost_per_unit;
  document.getElementById("price_per_unit").value = product.price_per_unit;
  document.getElementById("quantity_in_stock").value = product.quantity_in_stock;
  formTitle.textContent = `Edit product #${product.id}`;
  submitBtn.textContent = "Update product";
  cancelEditBtn.hidden = false;
  clearMessage();
  form.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function parseErrorResponse(response) {
  try {
    const data = await response.json();
    if (data.detail) {
      if (Array.isArray(data.detail)) {
        return data.detail.map((d) => d.msg || JSON.stringify(d)).join("; ");
      }
      return String(data.detail);
    }
    return response.statusText || "Request failed";
  } catch {
    return response.statusText || "Request failed";
  }
}

async function loadDbStatus() {
  try {
    const res = await fetch(API.dbCheck);
    if (!res.ok) throw new Error("unreachable");
    const data = await res.json();
    const count = data.products_in_database ?? data.product_count ?? "?";
    dbStatus.innerHTML = `Database: <strong>connected</strong> (${count} products)`;
  } catch {
    dbStatus.textContent = "Database: unavailable — start PostgreSQL and the API";
  }
}

function sortProducts(products) {
  return [...products].sort((a, b) => {
    if (a.id !== b.id) return a.id - b.id;
    return a.name.localeCompare(b.name, undefined, { sensitivity: "base" });
  });
}

function updateCatalogSummary(count) {
  if (count === 0) {
    catalogSummary.textContent = "No products — IDs start at 1 when you add items.";
    return;
  }
  catalogSummary.textContent = `${count} product${count === 1 ? "" : "s"} · sorted by ID (1, 2, 3…)`;
}

function renderProducts(products) {
  const sorted = sortProducts(products);
  updateCatalogSummary(sorted.length);

  if (!sorted.length) {
    productsBody.innerHTML =
      `<tr><td colspan="${EMPTY_COLSPAN}" class="empty">No products yet. Add one above.</td></tr>`;
    return;
  }

  productsBody.innerHTML = sorted
    .map(
      (p) => `
    <tr data-id="${p.id}">
      <td class="col-id"><span class="id-badge">${p.id}</span></td>
      <td class="col-name">${escapeHtml(p.name)}</td>
      <td class="col-unit"><span class="unit-pill">${escapeHtml(p.unit)}</span></td>
      <td class="col-money">$${formatMoney(p.cost_per_unit)}</td>
      <td class="col-money">$${formatMoney(p.price_per_unit)}</td>
      <td class="col-stock">${p.quantity_in_stock}</td>
      <td class="col-actions">
        <div class="actions-cell">
          <button type="button" class="btn-small edit-btn" data-id="${p.id}">Edit</button>
          <button type="button" class="btn-danger delete-btn" data-id="${p.id}">Delete</button>
        </div>
      </td>
    </tr>`
    )
    .join("");

  productsBody.querySelectorAll(".edit-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = Number(btn.dataset.id);
      const product = sorted.find((x) => x.id === id);
      if (product) startEdit(product);
    });
  });

  productsBody.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", () => deleteProduct(Number(btn.dataset.id)));
  });
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

async function loadProducts() {
  try {
    const res = await fetch(API.products);
    if (!res.ok) throw new Error(await parseErrorResponse(res));
    const products = await res.json();
    renderProducts(products);
  } catch (err) {
    productsBody.innerHTML = `<tr><td colspan="${EMPTY_COLSPAN}" class="empty">${escapeHtml(
      err.message || "Failed to load products"
    )}</td></tr>`;
  }
}

async function createProduct(payload) {
  const res = await fetch(API.products, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await parseErrorResponse(res));
  return res.json();
}

async function updateProduct(id, payload) {
  const res = await fetch(`${API.products}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await parseErrorResponse(res));
  return res.json();
}

async function deleteProduct(id) {
  if (!confirm(`Delete product #${id}?`)) return;
  clearMessage();
  try {
    const res = await fetch(`${API.products}/${id}`, { method: "DELETE" });
    if (!res.ok && res.status !== 204) {
      throw new Error(await parseErrorResponse(res));
    }
    showMessage(`Product #${id} deleted.`, "success");
    await refresh();
  } catch (err) {
    showMessage(err.message || "Delete failed", "error");
  }
}

async function refresh() {
  await Promise.all([loadProducts(), loadDbStatus()]);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearMessage();
  const payload = getFormPayload();
  const editId = productIdInput.value;

  try {
    if (editId) {
      await updateProduct(Number(editId), payload);
      showMessage(`Product #${editId} updated.`, "success");
      resetForm();
    } else {
      const created = await createProduct(payload);
      showMessage(`Product "${created.name}" created (id ${created.id}).`, "success");
      form.reset();
    }
    await refresh();
  } catch (err) {
    showMessage(err.message || "Save failed", "error");
  }
});

cancelEditBtn.addEventListener("click", resetForm);

refresh();
