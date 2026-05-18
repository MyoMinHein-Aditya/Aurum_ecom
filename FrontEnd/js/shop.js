/**
 * shop.js
 */
let debounceTimer;

async function loadProducts(search = '') {
  try {
    const products = await api.getProducts(search);
    const grid = document.getElementById('product-grid');
    grid.innerHTML = '';
    
    if (products.length === 0) {
      grid.innerHTML = '<p>No products found.</p>';
      return;
    }
    
    products.forEach(p => {
      const card = document.createElement('div');
      card.className = 'product-card';
      // Use placeholder if no image
      const imgUrl = p.image_url || 'https://via.placeholder.com/260x250?text=Aurum';
      card.innerHTML = `
        <img src="${imgUrl}" alt="${p.name}">
        <div class="card-body">
          <h3 class="card-title">${p.name}</h3>
          <p class="card-price">₹${p.price.toFixed(2)}</p>
          <div style="display:flex; gap:0.5rem">
            <button class="btn btn-primary" onclick="cartState.add(${p.id})">Add to Cart</button>
            <button class="btn btn-outline" onclick="openQuickView(${p.id})">View</button>
          </div>
        </div>
      `;
      grid.appendChild(card);
    });
  } catch (err) {
    ui.showToast('Failed to load products', 'error');
  }
}

async function openQuickView(id) {
  try {
    ui.showLoader();
    const p = await api.getProduct(id);
    const modal = document.getElementById('quick-view-modal');
    const body = document.getElementById('modal-body');
    const imgUrl = p.image_url || 'https://via.placeholder.com/260x250?text=Aurum';
    body.innerHTML = `
      <div style="display:flex; gap: 2rem;">
        <img src="${imgUrl}" style="width:50%; border-radius:8px;" alt="${p.name}">
        <div>
          <h2>${p.name}</h2>
          <p style="color:var(--gold); font-size:1.25rem;">₹${p.price.toFixed(2)}</p>
          <p style="margin: 1rem 0">${p.description}</p>
          <button class="btn btn-primary" onclick="cartState.add(${p.id}); document.getElementById('quick-view-modal').classList.remove('active')">Add to Cart</button>
          <a href="/pages/product.html?id=${p.id}" style="margin-left:1rem; text-decoration:underline;">Full Details</a>
        </div>
      </div>
    `;
    modal.classList.add('active');
  } catch(e) {
    ui.showToast('Failed to load product', 'error');
  } finally {
    ui.hideLoader();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const q = urlParams.get('q') || '';
  
  const searchInput = document.getElementById('search-input');
  if (searchInput && q) {
    searchInput.value = q;
  }
  
  loadProducts(q);
  
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        loadProducts(e.target.value);
      }, 300);
    });
  }
  
  document.getElementById('close-modal').addEventListener('click', () => {
    document.getElementById('quick-view-modal').classList.remove('active');
  });
});
