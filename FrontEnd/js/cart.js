/**
 * cart.js
 * Cart state and helper functions.
 */

window.cartState = {
  items: [],
  
  fetch: async () => {
    if (localStorage.getItem('access_token')) {
      try {
        const data = await window.api.getCart();
        window.cartState.items = data.items;
      } catch (e) {
        console.error(e);
      }
    } else {
      const stored = localStorage.getItem('guest_cart');
      if (stored) {
        window.cartState.items = JSON.parse(stored);
      }
    }
    window.cartState.updateBadge();
  },
  
  add: async (productId, quantity = 1) => {
    try {
      window.ui.showLoader();
      const product = await window.api.getProduct(productId);
      
      if (localStorage.getItem('access_token')) {
        await window.api.addToCart({ product_id: productId, quantity });
      } else {
        const existing = window.cartState.items.find(i => i.product.id === productId);
        if (existing) {
          existing.quantity += quantity;
        } else {
          window.cartState.items.push({ id: Date.now(), product, quantity });
        }
        localStorage.setItem('guest_cart', JSON.stringify(window.cartState.items));
      }
      await window.cartState.fetch();
      window.ui.showToast('Added to cart');
    } catch (e) {
      window.ui.showToast(e.message, 'error');
    } finally {
      window.ui.hideLoader();
    }
  },

  remove: async (productId) => {
    try {
      window.ui.showLoader();
      if (localStorage.getItem('access_token')) {
        await window.api.removeFromCart(productId);
      } else {
        window.cartState.items = window.cartState.items.filter(i => i.product.id !== productId);
        localStorage.setItem('guest_cart', JSON.stringify(window.cartState.items));
      }
      await window.cartState.fetch();
      window.ui.showToast('Removed from cart');
    } catch (e) {
      window.ui.showToast(e.message, 'error');
    } finally {
      window.ui.hideLoader();
    }
  },

  clear: async () => {
      if (localStorage.getItem('access_token')) {
        await window.api.clearCart();
      } else {
        window.cartState.items = [];
        localStorage.removeItem('guest_cart');
      }
      window.cartState.updateBadge();
  },
  
  updateBadge: () => {
    const badge = document.getElementById('cart-count');
    if (badge) {
      const count = window.cartState.items.reduce((sum, item) => sum + item.quantity, 0);
      badge.textContent = count;
      badge.style.display = count > 0 ? 'inline-block' : 'none';
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  window.cartState.fetch();
});
