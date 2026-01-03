// Profile page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Tab switching functionality
    const tabs = document.querySelectorAll('.tab');
    const tabPanels = document.querySelectorAll('.tab-panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and panels
            tabs.forEach(t => t.classList.remove('active'));
            tabPanels.forEach(panel => panel.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding panel
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
    
    // Avatar upload functionality (if needed)
    const editAvatarBtn = document.querySelector('.btn-edit-avatar');
    if (editAvatarBtn) {
        editAvatarBtn.addEventListener('click', function() {
            // You can implement avatar upload logic here
            console.log('Edit avatar clicked');
            // For now, just show an alert
            alert('Avatar upload functionality will be implemented');
        });
    }
    
    // Edit profile button
    const editProfileBtn = document.querySelector('.btn-edit-profile');
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', function() {
            console.log('Edit profile clicked');
            // Redirect to edit profile page or show modal
            // window.location.href = '/profile/edit/';
        });
    }
    
    // Save current active tab in sessionStorage
    const activeTab = sessionStorage.getItem('activeProfileTab');
    if (activeTab) {
        const tab = document.querySelector(`[data-tab="${activeTab}"]`);
        if (tab) {
            tab.click();
        }
    }
    
    // Store active tab when changed
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            sessionStorage.setItem('activeProfileTab', targetTab);
        });
    });
});
// Tab switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab');
    const tabPanels = document.querySelectorAll('.tab-panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.dataset.tab;
            
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            
            // Remove active class from all panels
            tabPanels.forEach(panel => panel.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Add active class to corresponding panel
            const targetPanel = document.getElementById(targetTab);
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
        });
    });
});