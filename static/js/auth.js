// Password Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            
            if (passwordInput) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    this.classList.add('active');
                } else {
                    passwordInput.type = 'password';
                    this.classList.remove('active');
                }
            }
        });
    });
    
    // Form validation feedback
    const form = document.querySelector('.auth-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = 'var(--error-color)';
                } else {
                    input.style.borderColor = 'var(--input-border)';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.style.borderColor = 'var(--error-color)';
                } else {
                    this.style.borderColor = 'var(--input-border)';
                }
            });
            
            input.addEventListener('input', function() {
                if (this.style.borderColor === 'var(--error-color)' && this.value.trim()) {
                    this.style.borderColor = 'var(--input-border)';
                }
            });
        });
    }
});
// Logo preview functionality
document.addEventListener('DOMContentLoaded', function() {
    const logoInput = document.getElementById('id_logo');
    const logoPreview = document.getElementById('logoPreview');
    
    if (logoInput && logoPreview) {
        // Make preview clickable
        logoPreview.addEventListener('click', function() {
            logoInput.click();
        });
        
        // Handle file selection
        logoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    logoPreview.innerHTML = `<img src="${e.target.result}" alt="Logo Preview">`;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});