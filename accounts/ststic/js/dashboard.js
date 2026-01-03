// Dashboard Logo Loading
document.addEventListener('DOMContentLoaded', function() {
    // Load company logo from localStorage if it exists
    const savedLogo = localStorage.getItem('companyLogo');
    if (savedLogo) {
        updateDashboardLogo(savedLogo);
    }
});

function updateDashboardLogo(logoData) {
    const logoContainer = document.getElementById('dashboardLogo');
    const logoText = logoContainer.querySelector('.logo-text');
    
    if (logoContainer && logoText) {
        // Check if logo image already exists
        let logoImg = logoContainer.querySelector('.dashboard-logo-img');
        if (!logoImg) {
            logoImg = document.createElement('img');
            logoImg.className = 'dashboard-logo-img';
            logoImg.style.height = '40px';
            logoImg.style.width = 'auto';
            logoImg.style.borderRadius = '4px';
            logoContainer.insertBefore(logoImg, logoText);
        }
        logoImg.src = logoData;
        logoText.style.display = 'none';
    }
}