// Signup form enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Password strength indicator
    const password1 = document.getElementById('id_password1');
    if (password1) {
        password1.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            // You can add visual feedback here
        });
    }
    
    // Password match validation
    const password2 = document.getElementById('id_password2');
    if (password1 && password2) {
        password2.addEventListener('input', function() {
            if (this.value !== password1.value) {
                this.style.borderColor = 'var(--error-color)';
            } else {
                this.style.borderColor = 'var(--success-color)';
            }
        });
    }
});

function checkPasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]+/)) strength++;
    if (password.match(/[A-Z]+/)) strength++;
    if (password.match(/[0-9]+/)) strength++;
    if (password.match(/[$@#&!]+/)) strength++;
    
    return strength;
}