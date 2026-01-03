// Add to static/js/navigation.js or in base.html
document.addEventListener('DOMContentLoaded', function() {
    // Get current path
    const currentPath = window.location.pathname;
    
    // Get all nav items
    const navItems = document.querySelectorAll('.dashboard-nav .nav-item');
    
    // Remove active class from all items
    navItems.forEach(item => {
        item.classList.remove('active');
        
        // Check if current path matches the nav item
        const href = item.getAttribute('href');
        if (currentPath.startsWith(href) && href !== '#') {
            item.classList.add('active');
        }
    });
});