document.addEventListener('DOMContentLoaded', function() {
    // Add page loading skeleton state briefly to smooth FOUC
    document.body.classList.add('is-loading');
    setTimeout(() => document.body.classList.remove('is-loading'), 350);

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

    // Copy button with success micro-interaction
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
                            const icon = this.querySelector('i');
                            const originalIcon = icon.className;
                            icon.className = 'fas fa-check';
                            this.setAttribute('title', 'Copied!');
                            setTimeout(() => {
                                icon.className = originalIcon;
                                this.setAttribute('title', 'Copy Key');
                            }, 1200);
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

    // Confirm delete with smooth card exit
    const confirmDelete = document.getElementById('confirmDelete');
    if (confirmDelete) {
        confirmDelete.addEventListener('click', function() {
            if (currentKeyId) {
                // optimistic UI: add exit animation
                const card = document.querySelector(`.api-key .delete-btn[data-key-id="${currentKeyId}"]`)?.closest('.api-key');
                if (card) {
                    card.classList.add('card-exit');
                }

                fetch(`/delete_key/${currentKeyId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        deleteModal.style.display = 'none';
                        // remove card after animation then reload to re-group
                        if (card) {
                            setTimeout(() => {
                                card.remove();
                                location.reload();
                            }, 220);
                        } else {
                            location.reload();
                        }
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

    // Keyboard shortcut: G to go to wallet
    window.addEventListener('keydown', function(e) {
        if ((e.key === 'g' || e.key === 'G') && !e.metaKey && !e.ctrlKey && !e.altKey) {
            const walletLink = document.querySelector('a[href*="/wallet"]');
            if (walletLink) {
                walletLink.click();
            }
        }
    });

    // Password strength indicator (register/login forms)
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        // Only add meter once
        if (!input.dataset.meterAttached) {
            const meter = document.createElement('div');
            meter.className = 'strength-meter';
            const bar = document.createElement('div');
            bar.className = 'bar';
            meter.appendChild(bar);
            input.insertAdjacentElement('afterend', meter);
            input.dataset.meterAttached = 'true';

            const evaluate = (value) => {
                let score = 0;
                if (value.length >= 8) score++;
                if (/[A-Z]/.test(value)) score++;
                if (/[0-9]/.test(value)) score++;
                if (/[^A-Za-z0-9]/.test(value)) score++;
                if (value.length >= 12) score++;
                if (score <= 2) {
                    meter.classList.remove('strength-medium','strength-strong');
                    meter.classList.add('strength-weak');
                } else if (score === 3 || score === 4) {
                    meter.classList.remove('strength-weak','strength-strong');
                    meter.classList.add('strength-medium');
                } else {
                    meter.classList.remove('strength-weak','strength-medium');
                    meter.classList.add('strength-strong');
                }
            };

            input.addEventListener('input', (e) => evaluate(e.target.value));
            evaluate(input.value || '');
        }
    });
});
