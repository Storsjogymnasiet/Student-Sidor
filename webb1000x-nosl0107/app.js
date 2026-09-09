const PRODUCTS = [
  { id: 1, name: "Linneblazer", category: "Överdelar", price: 1_295, color: "Sand", image: "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?auto=format&fit=crop&w=700&q=85", badge: "Bästsäljare" },
  { id: 2, name: "Alba knit", category: "Överdelar", price: 795, color: "Cream", image: "https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=700&q=85" },
  { id: 3, name: "Mira slip dress", category: "Under & klänning", price: 995, color: "Mörk espresso", image: "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=700&q=85", badge: "Nyhet" },
  { id: 4, name: "Ribbed tee", category: "Överdelar", price: 395, color: "Vit", image: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=700&q=85" },
  { id: 5, name: "Everyday jeans", category: "Under & klänning", price: 895, color: "Blå", image: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=700&q=85" },
  { id: 6, name: "Läderbälte", category: "Accessoarer", price: 295, color: "Brun", image: "https://images.unsplash.com/photo-1624222247344-550fb60583dc?auto=format&fit=crop&w=700&q=85" }
];

const cart = [];
let selectedCategory = "Alla";

const formatPrice = (value) => `${value.toLocaleString("sv-SE")} kr`;
const findProduct = (id) => PRODUCTS.find((product) => product.id === id);

function renderProducts() {
  const query = document.getElementById("search-input").value.trim().toLowerCase();
  const visibleProducts = PRODUCTS.filter((product) => {
    const matchesCategory = selectedCategory === "Alla" || product.category === selectedCategory;
    const matchesSearch = `${product.name} ${product.color}`.toLowerCase().includes(query);
    return matchesCategory && matchesSearch;
  });
  const grid = document.getElementById("product-grid");
  grid.innerHTML = visibleProducts.map((product) => `
    <article class="product-card">
      <div class="product-image">
        <img src="${product.image}" alt="${product.name}, ${product.color}">
        ${product.badge ? `<span class="product-badge">${product.badge}</span>` : ""}
        <button class="add-to-cart" data-id="${product.id}" aria-label="Lägg ${product.name} i kundvagnen">+</button>
      </div>
      <div class="product-info"><div><h3>${product.name}</h3><p>${product.color}</p></div><strong>${formatPrice(product.price)}</strong></div>
    </article>
  `).join("");
  document.getElementById("empty-state").hidden = visibleProducts.length > 0;
  grid.querySelectorAll(".add-to-cart").forEach((button) => button.addEventListener("click", () => addToCart(Number(button.dataset.id))));
}

function addToCart(id) {
  const item = cart.find((entry) => entry.id === id);
  if (item) item.quantity += 1;
  else cart.push({ id, quantity: 1 });
  renderCart();
  openCart();
}

function renderCart() {
  const itemsElement = document.getElementById("cart-items");
  const itemCount = cart.reduce((total, item) => total + item.quantity, 0);
  const total = cart.reduce((sum, item) => sum + findProduct(item.id).price * item.quantity, 0);
  itemsElement.innerHTML = cart.map((item) => {
    const product = findProduct(item.id);
    return `<div class="cart-item"><img src="${product.image}" alt=""><div><h3>${product.name}</h3><p>${formatPrice(product.price)}</p><div class="quantity"><button data-action="decrease" data-id="${product.id}" aria-label="Minska antal">−</button><span>${item.quantity}</span><button data-action="increase" data-id="${product.id}" aria-label="Öka antal">+</button></div></div><button class="remove-item" data-id="${product.id}" aria-label="Ta bort ${product.name}">×</button></div>`;
  }).join("");
  document.getElementById("cart-count").textContent = itemCount;
  document.getElementById("cart-total").textContent = formatPrice(total);
  document.getElementById("cart-empty").hidden = cart.length > 0;
  document.querySelector(".cart-footer").hidden = cart.length === 0;
  itemsElement.querySelectorAll("button").forEach((button) => button.addEventListener("click", () => {
    const item = cart.find((entry) => entry.id === Number(button.dataset.id));
    if (button.classList.contains("remove-item")) cart.splice(cart.indexOf(item), 1);
    else if (button.dataset.action === "increase") item.quantity += 1;
    else if (item.quantity > 1) item.quantity -= 1;
    else cart.splice(cart.indexOf(item), 1);
    renderCart();
  }));
}

function openCart() {
  document.getElementById("cart").classList.add("open");
  document.getElementById("cart").setAttribute("aria-hidden", "false");
  document.getElementById("overlay").classList.add("visible");
}

function closeCart() {
  document.getElementById("cart").classList.remove("open");
  document.getElementById("cart").setAttribute("aria-hidden", "true");
  document.getElementById("overlay").classList.remove("visible");
}

document.querySelectorAll(".filter").forEach((button) => button.addEventListener("click", () => {
  selectedCategory = button.dataset.category;
  document.querySelectorAll(".filter").forEach((tab) => tab.classList.toggle("active", tab === button));
  renderProducts();
}));
document.getElementById("search-input").addEventListener("input", renderProducts);
document.getElementById("cart-toggle").addEventListener("click", openCart);
document.getElementById("cart-close").addEventListener("click", closeCart);
document.getElementById("overlay").addEventListener("click", closeCart);
document.getElementById("clear-cart").addEventListener("click", () => { cart.length = 0; renderCart(); });
document.getElementById("search-toggle").addEventListener("click", () => {
  document.getElementById("search-box").classList.toggle("visible");
  document.getElementById("search-input").focus();
});
document.getElementById("checkout-mail").addEventListener("click", () => {
  const lines = cart.map((item) => `${findProduct(item.id).name} x ${item.quantity} — ${formatPrice(findProduct(item.id).price * item.quantity)}`).join("\n");
  const total = cart.reduce((sum, item) => sum + findProduct(item.id).price * item.quantity, 0);
  window.open("https://revolut.me/n_slibi", "_blank", "noopener");
  window.location.href = `mailto:nour_slibi2@icloud.com?subject=${encodeURIComponent("Ny beställning från Akano")}&body=${encodeURIComponent(`Hej!\n\nJag vill beställa:\n${lines}\n\nTotalt: ${formatPrice(total)}\n\nJag betalar via Revolut.\n\nNamn och leveransadress:\n`)}`;
});
document.getElementById("newsletter-form").addEventListener("submit", (event) => {
  event.preventDefault();
  document.getElementById("form-message").textContent = "Tack! Håll utkik i inkorgen.";
  event.target.reset();
});

renderProducts();
renderCart();
