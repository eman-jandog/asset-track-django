import { showSection } from './global.js';

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

document.addEventListener('DOMContentLoaded', () => {
    showSection('orders')
})