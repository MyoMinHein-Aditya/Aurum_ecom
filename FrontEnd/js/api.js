/**
 * api.js
 * Centralized fetch wrappers.
 */

const API_BASE = '/api/v1';

async function fetchAPI(endpoint, options = {}) {
  const token = localStorage.getItem('access_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...(options.headers || {})
  };

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });
    
    if (response.status === 401 && endpoint !== '/auth/login') {
      localStorage.removeItem('access_token');
      window.location.href = '/pages/login.html';
      return;
    }

    if (response.status === 204) {
      return null;
    }

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'An error occurred');
    }
    
    return data;
  } catch (error) {
    console.error(`API Error on ${endpoint}:`, error);
    throw error;
  }
}

window.api = {
  login: (credentials) => fetchAPI('/auth/login', { method: 'POST', body: JSON.stringify(credentials) }),
  register: (userData) => fetchAPI('/auth/register', { method: 'POST', body: JSON.stringify(userData) }),
  logout: () => fetchAPI('/auth/logout', { method: 'POST' }),
  getMe: () => fetchAPI('/auth/me'),
  
  getProducts: (search = '') => fetchAPI(`/products/?search=${search}&_t=${new Date().getTime()}`),
  getProduct: (id) => fetchAPI(`/products/${id}`),
  createProduct: (data) => fetchAPI('/products/', { method: 'POST', body: JSON.stringify(data) }),
  deleteProduct: (id) => fetchAPI(`/products/${id}`, { method: 'DELETE' }),
  
  getCart: () => fetchAPI('/cart/'),
  addToCart: (item) => fetchAPI('/cart/add', { method: 'POST', body: JSON.stringify(item) }),
  removeFromCart: (id) => fetchAPI(`/cart/remove/${id}`, { method: 'DELETE' }),
  clearCart: () => fetchAPI('/cart/clear', { method: 'POST' }),
  
  checkout: (data) => {
    if (!localStorage.getItem('access_token')) {
      const guestCart = JSON.parse(localStorage.getItem('guest_cart') || '[]');
      data.guest_cart_items = guestCart.map(i => ({ product_id: i.product.id, quantity: i.quantity }));
    }
    return fetchAPI('/orders/checkout', { method: 'POST', body: JSON.stringify(data) });
  },
  getOrders: () => fetchAPI('/orders/'),
  
  // Admin Endpoints
  getDashboard: () => fetchAPI('/admin/dashboard'),
  getAllOrdersAdmin: () => fetchAPI('/admin/orders'),
  updateOrderStatus: (id, status) => fetchAPI(`/admin/orders/${id}/status`, { method: 'PUT', body: JSON.stringify({ status }) }),
};
