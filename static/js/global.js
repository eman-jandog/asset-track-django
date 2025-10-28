let toggleMode;

// Exported Functions
export function showSection(sectionName) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('bg-blue-50', 'text-blue-600', 'border-r-2', 'border-blue-600');
        item.classList.add('text-gray-600', 'hover:bg-gray-50', 'hover:text-gray-800');
    }) 

    const btn = document.querySelector(`[data-section=${sectionName}]`)
    btn.classList.remove('text-gray-600', 'hover:bg-gray-50', 'hover:text-gray-800');
    btn.classList.add('bg-blue-50', 'text-blue-600', 'border-r-2', 'border-blue-600');
}

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

    return !isCompact
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
function openModal(modalType, id=null) {
    let url;
    if (id) {
        url = `${modalType}/form/${id}/`;
    } else {
        url = `${modalType}/form/`;
    }

    htmx.ajax('GET', url, {
        'target': '#formModal',
    })

    document.getElementById('formModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById("formModal").classList.add('hidden');
    document.body.style.overflow = 'auto';
    // Reset form
    const form = document.querySelector(`#forModal form`);
    if (form) form.reset();
    // Reset order total if it's the order modal
    // if (modalType === 'createOrderModal') {
    //     updateOrderTotal();
    // }
}

document.addEventListener('DOMContentLoaded', () => {   
    // Sidebar actions
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
    document.getElementById('profileBtn').addEventListener('click', toggleUserMenu);
    document.getElementById('sidebarToggle').addEventListener('click', toggleSidebarMode);

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

    // Sidebar buttons navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            const section = item.dataset.section;
            let url = window.location.href
            let regEx = /\/[a-z]*\/$/i;
            url = url.replace(regEx, `/${section}/`)
            window.location.href = url       
        })
    })

    //  Initial Run

    // Modal close buttons
    // document.getElementById('closeStaffModal').addEventListener('click', () => closeModal('addStaffModal'));
    // document.getElementById('cancelStaffModal').addEventListener('click', () => closeModal('addStaffModal'));

    // document.getElementById('closeOrderModal').addEventListener('click', () => closeModal('createOrderModal'));
    // document.getElementById('cancelOrderModal').addEventListener('click', () => closeModal('createOrderModal'));

    // Form submissions
    // document.getElementById('addStaffForm').addEventListener('submit', handleStaffSubmission);
    // document.getElementById('createOrderForm').addEventListener('submit', handleOrderSubmission);
    // document.getElementById('addAssetForm').addEventListener('submit', handleAssetSubmission);

    // Order item management
    // document.getElementById('addOrderItem').addEventListener('click', addOrderItem);

    // Initial setup for order items
    // document.querySelectorAll('.remove-item').forEach(btn => {
    //     btn.addEventListener('click', function() {
    //         removeOrderItem(btn)
    //     });
    // });
            
    // Price calculation for order items
    // document.querySelectorAll('input[name="itemQuantity[]"], input[name="itemPrice[]"]').forEach(input => {
    //     input.addEventListener('input', updateOrderTotal);
    // });
})

