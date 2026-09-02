// Enkel kundvagnslogik för statisk webbshop
const PRODUCTS = [
  { id: 1, title: 'Produkt 1', price: 99 },
  { id: 2, title: 'Produkt 2', price: 149 },
  { id: 3, title: 'Produkt 3 (digital)', price: 49 }
];

const cart = [];

function formatPrice(n){ return n + ' kr'; }

function findProduct(id){ return PRODUCTS.find(p => p.id === id); }

function addToCart(id){
  const item = cart.find(i => i.id === id);
  if(item) item.qty++;
  else cart.push({ id, qty: 1 });
  renderCart();
}

function removeFromCart(id){
  const idx = cart.findIndex(i => i.id === id);
  if(idx >= 0) cart.splice(idx,1);
  renderCart();
}

function clearCart(){ cart.length = 0; renderCart(); }

function cartTotal(){
  return cart.reduce((sum,i)=> sum + (findProduct(i.id).price * i.qty), 0);
}

function renderCart(){
  const itemsEl = document.getElementById('cart-items');
  const countEl = document.getElementById('cart-count');
  const totalEl = document.getElementById('cart-total');
  itemsEl.innerHTML = '';
  cart.forEach(i => {
    const p = findProduct(i.id);
    const li = document.createElement('li');
    li.innerHTML = `<span>${p.title} x ${i.qty}</span><span>${formatPrice(p.price * i.qty)}</span>`;
    li.addEventListener('click', ()=> removeFromCart(i.id));
    itemsEl.appendChild(li);
  });
  countEl.textContent = cart.reduce((s,i)=> s + i.qty, 0);
  totalEl.textContent = formatPrice(cartTotal());
}

function setup(){
  document.querySelectorAll('.add-to-cart').forEach(btn=>{
    btn.addEventListener('click', e=>{
      const id = Number(btn.dataset.id);
      addToCart(id);
    });
  });

  document.getElementById('cart-toggle').addEventListener('click', ()=>{
    document.getElementById('cart').classList.toggle('hidden');
  });

  document.getElementById('clear-cart').addEventListener('click', ()=>{
    clearCart();
  });

  document.getElementById('checkout-mail').addEventListener('click', ()=>{
    if(cart.length === 0){
      alert('Kundvagnen är tom. Lägg till en vara först.');
      return;
    }
    // Byt ut orders@example.com till din ordningsmottagande e-post
    const to = 'nour_slibi2@icloud.com';
    const subject = encodeURIComponent('Ny beställning från webbshop');
    let body = 'Hej,%0D%0A%0D%0AJag vill beställa följande:%0D%0A%0D%0A';
    cart.forEach(i => {
      const p = findProduct(i.id);
      body += `${p.title} x ${i.qty} — ${p.price} kr%0D%0A`;
    });
    body += `%0D%0ATotalt: ${cartTotal()} kr%0D%0A%0D%0AAdress (ange här):%0D%0ATelefon:%0D%0A%0D%0ATack!`;

    const mailto = `mailto:${to}?subject=${subject}&body=${body}`;
    window.location.href = mailto;
  });

  // Klickbara PayPal-länkar öppnas i ny flik (finns i HTML som platshållare)
  // Rensa kundvagnen initialt
  renderCart();
}

// Init när dokumentet är redo
if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup);
else setup();

// Tips: För riktig betalning, skapa en server-side endpoint som genererar Stripe Checkout sessions
// eller använd riktiga PayPal-länkar istället för platshållare. Byt också ut orders@example.com i checkout-mail till din egen e-postadress.