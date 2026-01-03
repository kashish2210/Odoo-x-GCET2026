// Profile Tab Functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            document.getElementById(tabName + '-tab').classList.add('active');
        });
    });
    
    // Profile photo upload
    const editPhotoBtn = document.querySelector('.edit-photo-btn');
    if (editPhotoBtn) {
        editPhotoBtn.addEventListener('click', function() {
            // Create file input dynamically
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';
            
            fileInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(event) {
                        const profilePhoto = document.querySelector('.profile-photo');
                        profilePhoto.style.backgroundImage = `url(${event.target.result})`;
                        profilePhoto.style.backgroundSize = 'cover';
                        profilePhoto.style.backgroundPosition = 'center';
                        profilePhoto.querySelector('svg').style.display = 'none';
                    };
                    reader.readAsDataURL(file);
                }
            });
            
            fileInput.click();
        });
    }
});