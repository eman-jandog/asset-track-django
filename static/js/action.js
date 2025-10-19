// Technical Functions

function handleLogout() {
    // localStorage.removeItem('userEmail');
    // localStorage.removeItem('isLoggedIn');
    
    // Show auth container and hide dashboard
    document.getElementById('dashboardContainer').classList.add('hidden');
    // document.getElementById('authContainer').classList.remove('hidden');
    
    // Reset forms
    document.getElementById('loginFormElement').reset();
    document.getElementById('registerFormElement').reset();
    showLoginForm();
}

function toggleSidebarMode() {
    const sidebar = document.getElementById('sidebar'); 
    const mainContent = document.getElementById('mainContent');

    const isCompact = !sidebar.classList.contains('w-64');

    if (isCompact) {
        // Switch to compact sidebar
        sidebar.classList.remove('w-16');
        sidebar.classList.add('w-64');
        mainContent.classList.remove('lg:ml-16');
        mainContent.classList.add('lg:ml-64');      
    } else {
        // Switch to full sidebar
        sidebar.classList.remove('w-64');
        sidebar.classList.add('w-16');
        mainContent.classList.remove('lg:ml-64');
        mainContent.classList.add('lg:ml-16');  
    }
}

function showSection(sectionName) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('bg-blue-50', 'text-blue-600', 'border-r-2', 'border-blue-600');
        item.classList.add('text-gray-600', 'hover:bg-gray-50', 'hover:text-gray-800');
    }) 

    const btn = document.querySelector(`[data-section=${sectionName}]`)
    btn.classList.remove('text-gray-600', 'hover:bg-gray-50', 'hover:text-gray-800');
    btn.classList.add('bg-blue-50', 'text-blue-600', 'border-r-2', 'border-blue-600');

    // htmx.ajax("GET", `/${sectionName}/`, '#mainSection')
    document.querySelectorAll('.section-content').forEach(section => {
        section.classList.add('hidden')
    })

    const section = document.querySelector(`#${sectionName}Section`)
    section.classList.remove('hidden')
    
}

function toggleUserMenu() {
    const sidebar = document.getElementById('sidebar'); 
    const userMenu = document.getElementById('userMenu');

    const isCompact = sidebar.classList.contains('w-16');

    if (isCompact) {
        userMenu.classList.remove('lg:left-66');
        userMenu.classList.add('lg:left-18')
    }
    else {
        userMenu.classList.remove('lg:left-18')
        userMenu.classList.add('lg:left-66');
    }

    userMenu.classList.toggle('hidden');
}

// Modal functions
function openModal(modalId) {
    console.log('clicked')
    document.getElementById(modalId).classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
    document.body.style.overflow = 'auto';
    // Reset form
    const form = document.querySelector(`#${modalId} form`);
    if (form) form.reset();
    // Reset order total if it's the order modal
    if (modalId === 'createOrderModal') {
        updateOrderTotal();
    }
}

// Order item management
function addOrderItem() {
    const container = document.getElementById('orderItemsContainer');
    const newItem = document.createElement('div');
    newItem.className = 'order-item grid grid-cols-1 md:grid-cols-5 gap-4 p-4 bg-gray-50 rounded-lg';
    newItem.innerHTML = `
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Item Name *</label>
            <input type="text" name="itemName[]" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all text-sm" placeholder="Product name">
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select name="itemCategory[]" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all text-sm">
                <option value="">Select</option>
                <option value="Laptop">Laptop</option>
                <option value="Monitor">Monitor</option>
                <option value="Mobile">Mobile</option>
                <option value="Printer">Printer</option>
                <option value="Accessory">Accessory</option>
                <option value="Furniture">Furniture</option>
            </select>
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Quantity *</label>
            <input type="number" name="itemQuantity[]" required min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all text-sm" placeholder="1">
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Unit Price *</label>
            <input type="number" name="itemPrice[]" required min="0" step="0.01" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all text-sm" placeholder="0.00">
        </div>
        <div class="flex items-end">
            <button type="button" class="remove-item w-full bg-red-100 text-red-700 px-3 py-2 rounded-lg hover:bg-red-200 transition-colors text-sm">Remove</button>
        </div>
    `;
    container.appendChild(newItem);
    
    // Add event listeners to new item
    const removeBtn = newItem.querySelector('.remove-item');
    removeBtn.addEventListener('click', function() {
        removeOrderItem(removeBtn)
    });
    
    const priceInputs = newItem.querySelectorAll('input[name="itemQuantity[]"], input[name="itemPrice[]"]');
    priceInputs.forEach(input => {
        input.addEventListener('input', updateOrderTotal);
    });
}

function updateOrderTotal() {
    const items = document.querySelectorAll('.order-item');
    let total = 0;
    
    items.forEach(item => {
        const quantity = parseFloat(item.querySelector('input[name="itemQuantity[]"]').value) || 0;
        const price = parseFloat(item.querySelector('input[name="itemPrice[]"]').value) || 0;
        total += quantity * price;
    });
    
    document.getElementById('orderTotal').textContent = `$${total.toFixed(2)}`;
}

function removeOrderItem(btn) {
    const items = document.querySelectorAll('.order-item');
    if (items.length > 1) {
        btn.closest('.order-item').remove();
        updateOrderTotal();
    } else {
        alert('At least one item is required for an order.');
    }
}

// Form submission handlers
function handleStaffSubmission(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const staffData = Object.fromEntries(formData.entries());
    
    // Generate employee ID if not provided
    if (!staffData.employeeId) {
        staffData.employeeId = 'EMP-' + Date.now().toString().slice(-6);
    }
    
    console.log('New staff member:', staffData);
    alert(`Staff member ${staffData.firstName} ${staffData.lastName} added successfully!\nEmployee ID: ${staffData.employeeId}`);
    closeModal('addStaffModal');
    
    // In a real app, you would add this to the staff table
    // For demo purposes, we'll just show success
}

function handleOrderSubmission(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const orderData = Object.fromEntries(formData.entries());
    
    // Generate order ID
    const orderId = 'ORD-' + new Date().getFullYear() + '-' + Date.now().toString().slice(-3);
    
    // Get all order items
    const itemNames = formData.getAll('itemName[]');
    const itemQuantities = formData.getAll('itemQuantity[]');
    const itemPrices = formData.getAll('itemPrice[]');
    
    const items = itemNames.map((name, index) => ({
        name,
        quantity: itemQuantities[index],
        price: itemPrices[index]
    }));
    
    const total = document.getElementById('orderTotal').textContent;
    
    console.log('New order:', { orderId, ...orderData, items, total });
    alert(`Order ${orderId} created successfully!\nTotal: ${total}\nItems: ${items.length}`);
    closeModal('createOrderModal');
}

function handleAssetSubmission(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const assetData = Object.fromEntries(formData.entries());
    
    // Generate asset ID if not provided
    if (!assetData.assetId) {
        assetData.assetId = 'AST-' + Date.now().toString().slice(-6);
    }
    
    console.log('New asset:', assetData);
    alert(`Asset ${assetData.assetName} added successfully!\nAsset ID: ${assetData.assetId}\nValue: $${assetData.purchasePrice}`);
    closeModal('addAssetModal');
}

// Initializing
function initializeCharts() {
    // Asset Distribution Chart
    const assetCtx = document.getElementById('assetChart').getContext('2d');
    new Chart(assetCtx, {
        type: 'doughnut',
        data: {
            labels: ['Laptops', 'Monitors', 'Mobile Devices', 'Printers', 'Accessories'],
            datasets: [{
                data: [35, 25, 20, 12, 8],
                backgroundColor: [
                    '#3B82F6',
                    '#10B981',
                    '#F59E0B',
                    '#EF4444',
                    '#8B5CF6'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });

    // Monthly Orders Chart
    const ordersCtx = document.getElementById('ordersChart').getContext('2d');
    new Chart(ordersCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Orders',
                data: [12, 19, 15, 25, 22, 30],
                borderColor: '#3B82F6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function initializeDashboard() {
    // populateStaffTable();
    // populateOrdersTable();
    // populateAssetsGrid();
    // loadUserProfile();
    
    // Initialize charts after a short delay to ensure DOM is ready
    setTimeout(initializeCharts, 100);
}

document.addEventListener('DOMContentLoaded', () => {
    // Sidebar actions
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
    document.getElementById('profileBtn').addEventListener('click', toggleUserMenu);
    document.getElementById('sidebarToggle').addEventListener('click', toggleSidebarMode);

    // Modal close buttons
    document.getElementById('closeStaffModal').addEventListener('click', () => closeModal('addStaffModal'));
    document.getElementById('cancelStaffModal').addEventListener('click', () => closeModal('addStaffModal'));

    document.getElementById('closeOrderModal').addEventListener('click', () => closeModal('createOrderModal'));
    document.getElementById('cancelOrderModal').addEventListener('click', () => closeModal('createOrderModal'));

    // Form submissions
    document.getElementById('addStaffForm').addEventListener('submit', handleStaffSubmission);
    document.getElementById('createOrderForm').addEventListener('submit', handleOrderSubmission);
    // document.getElementById('addAssetForm').addEventListener('submit', handleAssetSubmission);

    // Order item management
    document.getElementById('addOrderItem').addEventListener('click', addOrderItem);

    // Initial setup for order items
    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', function() {
            removeOrderItem(btn)
        });
    });
            
    // Price calculation for order items
    document.querySelectorAll('input[name="itemQuantity[]"], input[name="itemPrice[]"]').forEach(input => {
        input.addEventListener('input', updateOrderTotal);
    });

    // Sidebar buttons navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            const section = item.dataset.section;
            showSection(section);
        })
    })

    // Autoclose for userMenu
    document.addEventListener('click', function(event) {
        const userMenu = document.getElementById('userMenu');
        
        if (!userMenu.classList.contains('hidden')) {
            const userButton = event.target.closest('button');  
            
            if (!userButton || userButton.getAttribute('id') != 'profileBtn') {
                userMenu.classList.add('hidden');
            }
        }
    });

    //  Initial Run
    toggleSidebarMode();
    initializeDashboard();
})


