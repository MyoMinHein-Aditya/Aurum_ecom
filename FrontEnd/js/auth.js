/**
 * auth.js
 * Auth state management.
 */

window.auth = {
  init: () => {
    const token = localStorage.getItem('access_token');
    const authLinks = document.querySelectorAll('.auth-link');
    const guestLinks = document.querySelectorAll('.guest-link');
    
    if (token) {
      authLinks.forEach(el => el.style.display = 'inline-block');
      guestLinks.forEach(el => el.style.display = 'none');
    } else {
      authLinks.forEach(el => el.style.display = 'none');
      guestLinks.forEach(el => el.style.display = 'inline-block');
    }
  },
  
  logout: async () => {
    try {
      await window.api.logout();
    } catch(e) {}
    localStorage.removeItem('access_token');
    window.location.href = '/';
  }
};

document.addEventListener('DOMContentLoaded', () => {
  window.auth.init();
  
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      window.auth.logout();
    });
  }
});
