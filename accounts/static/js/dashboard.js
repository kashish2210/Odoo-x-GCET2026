// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Profile Dropdown Toggle
    const profileDropdownBtn = document.getElementById('profileDropdownBtn');
    const profileDropdownMenu = document.getElementById('profileDropdownMenu');
    
    if (profileDropdownBtn && profileDropdownMenu) {
        profileDropdownBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            profileDropdownMenu.classList.toggle('show');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!profileDropdownBtn.contains(e.target) && !profileDropdownMenu.contains(e.target)) {
                profileDropdownMenu.classList.remove('show');
            }
        });
    }
    
    // Search Functionality
    const searchInput = document.getElementById('searchInput');
    const employeeCards = document.querySelectorAll('.employee-card');
    
    if (searchInput && employeeCards.length > 0) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            employeeCards.forEach(card => {
                const employeeName = card.querySelector('.employee-info h3').textContent.toLowerCase();
                const employeeRole = card.querySelector('.employee-role').textContent.toLowerCase();
                const employeeDept = card.querySelector('.employee-dept').textContent.toLowerCase();
                
                if (employeeName.includes(searchTerm) || 
                    employeeRole.includes(searchTerm) || 
                    employeeDept.includes(searchTerm)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Employee Card Click (redirect to employee profile)
    if (employeeCards.length > 0) {
        employeeCards.forEach(card => {
            card.addEventListener('click', function() {
                const employeeId = this.getAttribute('data-employee-id');
                if (employeeId) {
                    // Redirect to employee profile page
                    window.location.href = `/employee/${employeeId}/profile/`;
                }
            });
        });
    }
    
    // Add Employee Button
    const addEmployeeBtn = document.getElementById('addEmployeeBtn');
    if (addEmployeeBtn) {
        addEmployeeBtn.addEventListener('click', function() {
            // Redirect to add employee page
            window.location.href = '/employee/add/';
            // Or show a modal
            // showAddEmployeeModal();
        });
    }
    
    // Settings Button
    const settingsBtn = document.getElementById('settingsBtn');
    if (settingsBtn) {
        settingsBtn.addEventListener('click', function() {
            // Redirect to settings page
            window.location.href = '/settings/';
            // Or show settings modal
        });
    }
    
    // Real-time clock update (optional)
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
        
        const clockElements = document.querySelectorAll('.attendance-time small');
        // This is just for demonstration - you'd actually get this from server
    }
    
    // Update clock every minute (if needed)
    // setInterval(updateClock, 60000);
    
    // Animation on page load
    const cards = document.querySelectorAll('.employee-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });
});