/**
 * cart_page.js
 */
async function renderCart() {
  const list = document.getElementById('cart-items-list');
  const totalEl = document.getElementById('cart-total');
  
  try {
    ui.showLoader();
    await cartState.fetch(); // Ensure state is fresh
    list.innerHTML = '';
    
    if (cartState.items.length === 0) {
      list.innerHTML = '<p>Your cart is empty. <a href="/pages/shop.html" style="color: var(--gold)">Continue shopping</a>.</p>';
      totalEl.textContent = '₹0.00';
      return;
    }
    
    let total = 0;
    cartState.items.forEach(item => {
      total += item.product.price * item.quantity;
      const row = document.createElement('div');
      row.className = 'cart-item-row';
      const imgUrl = item.product.image_url || 'https://via.placeholder.com/100?text=IMG';
      
      row.innerHTML = `
        <img src="${imgUrl}" alt="${item.product.name}">
        <div class="item-details">
          <h4>${item.product.name}</h4>
          <p style="color:var(--gold)">₹${item.product.price.toFixed(2)}</p>
          <p>Qty: ${item.quantity}</p>
        </div>
        <div class="item-actions">
          <button class="btn btn-outline" onclick="removeItem(${item.product.id})">Remove</button>
        </div>
      `;
      list.appendChild(row);
    });
    
    totalEl.textContent = `₹${total.toFixed(2)}`;
  } catch(e) {
    list.innerHTML = '<p>Error loading cart.</p>';
  } finally {
    ui.hideLoader();
  }
}

window.removeItem = async (productId) => {
  await cartState.remove(productId);
  renderCart();
};

document.addEventListener('DOMContentLoaded', () => {
  renderCart();
});
