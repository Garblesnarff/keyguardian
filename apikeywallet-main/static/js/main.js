document.addEventListener('DOMContentLoaded', function() {
    // Toggle visibility button
    const toggleButtons = document.querySelectorAll('.toggle-visibility-btn');
    toggleButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const keyId = this.getAttribute('data-key-id');
            const keyElement = this.closest('.api-key');
            const maskedKey = keyElement.querySelector('.masked-key');
            
            if (maskedKey.textContent.includes('•')) {
                // Get the actual key
                fetch(`/get_key/${keyId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.key) {
                        maskedKey.textContent = data.key;
                        this.querySelector('i').classList.remove('fa-eye');
                        this.querySelector('i').classList.add('fa-eye-slash');
                    }
                })
                .catch(error => console.error('Error:', error));
            } else {
                maskedKey.textContent = '••••••••••••••••';
                this.querySelector('i').classList.remove('fa-eye-slash');
                this.querySelector('i').classList.add('fa-eye');
            }
        });
    });

    // Copy button
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const keyId = this.getAttribute('data-key-id');
            
            fetch(`/copy_key/${keyId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.key) {
                    navigator.clipboard.writeText(data.key)
                        .then(() => {
                            const originalIcon = this.querySelector('i').className;
                            this.querySelector('i').className = 'fas fa-check';
                            setTimeout(() => {
                                this.querySelector('i').className = originalIcon;
                            }, 1000);
                        });
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Edit button
    const editButtons = document.querySelectorAll('.edit-btn');
    const editModal = document.getElementById('editModal');
    
    editButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const keyId = this.getAttribute('data-key-id');
            const keyElement = this.closest('.api-key');
            const keyName = keyElement.querySelector('h4').textContent;
            
            document.getElementById('editKeyId').value = keyId;
            document.getElementById('editKeyName').value = keyName;
            editModal.style.display = 'flex';
        });
    });

    // Edit form handling
    const editKeyForm = document.getElementById('editKeyForm');
    if (editKeyForm) {
        editKeyForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const keyId = document.getElementById('editKeyId').value;
            const newKeyName = document.getElementById('editKeyName').value;
            
            fetch(`/edit_key/${keyId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key_name: newKeyName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Cancel edit
    const cancelEdit = document.getElementById('cancelEdit');
    if (cancelEdit) {
        cancelEdit.addEventListener('click', function() {
            editModal.style.display = 'none';
        });
    }

    // Delete button
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const deleteModal = document.getElementById('deleteModal');
    let currentKeyId = null;
    
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            currentKeyId = this.getAttribute('data-key-id');
            deleteModal.style.display = 'flex';
        });
    });

    // Confirm delete
    const confirmDelete = document.getElementById('confirmDelete');
    if (confirmDelete) {
        confirmDelete.addEventListener('click', function() {
            if (currentKeyId) {
                fetch(`/delete_key/${currentKeyId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        deleteModal.style.display = 'none';
                        location.reload();
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    }

    // Cancel delete
    const cancelDelete = document.getElementById('cancelDelete');
    if (cancelDelete) {
        cancelDelete.addEventListener('click', function() {
            deleteModal.style.display = 'none';
            currentKeyId = null;
        });
    }

    // Category select change
    const categorySelects = document.querySelectorAll('.category-select');
    categorySelects.forEach(select => {
        select.addEventListener('change', function() {
            const keyId = this.getAttribute('data-key-id');
            const categoryId = parseInt(this.value);
            
            fetch(`/update_key_category/${keyId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ category_id: categoryId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Modal background click to close
    window.addEventListener('click', function(event) {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
            currentKeyId = null;
        }
    });
});
