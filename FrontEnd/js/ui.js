/**
 * ui.js
 * Toast messages, loaders, and DOM helpers.
 */

window.ui = {
  showToast: (message, type = 'info') => {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    setTimeout(() => {
      toast.classList.add('fade-out');
      toast.addEventListener('animationend', () => {
        toast.remove();
      });
    }, 3000);
  },
  
  showLoader: () => {
    let loader = document.getElementById('global-loader');
    if (!loader) {
      loader = document.createElement('div');
      loader.id = 'global-loader';
      loader.className = 'loader-overlay';
      loader.innerHTML = '<div class="spinner"></div>';
      document.body.appendChild(loader);
    }
    loader.classList.remove('hidden');
  },
  
  hideLoader: () => {
    const loader = document.getElementById('global-loader');
    if (loader) {
      loader.classList.add('hidden');
    }
  }
};
