import { showSection } from './global.js';

// Form submission handlers
// function handleStaffSubmission(event) {
//     event.preventDefault();
//     const formData = new FormData(event.target);
//     const staffData = Object.fromEntries(formData.entries());
    
//     // Generate employee ID if not provided
//     if (!staffData.employeeId) {
//         staffData.employeeId = 'EMP-' + Date.now().toString().slice(-6);
//     }
    
//     console.log('New staff member:', staffData);
//     alert(`Staff member ${staffData.firstName} ${staffData.lastName} added successfully!\nEmployee ID: ${staffData.employeeId}`);
//     closeModal('addStaffModal');
    
//     // In a real app, you would add this to the staff table
//     // For demo purposes, we'll just show success
// }

// function handleOrderSubmission(event) {
//     event.preventDefault();
//     const formData = new FormData(event.target);
//     const orderData = Object.fromEntries(formData.entries());
    
//     // Generate order ID
//     const orderId = 'ORD-' + new Date().getFullYear() + '-' + Date.now().toString().slice(-3);
    
//     // Get all order items
//     const itemNames = formData.getAll('itemName[]');
//     const itemQuantities = formData.getAll('itemQuantity[]');
//     const itemPrices = formData.getAll('itemPrice[]');
    
//     const items = itemNames.map((name, index) => ({
//         name,
//         quantity: itemQuantities[index],
//         price: itemPrices[index]
//     }));
    
//     const total = document.getElementById('orderTotal').textContent;
    
//     console.log('New order:', { orderId, ...orderData, items, total });
//     alert(`Order ${orderId} created successfully!\nTotal: ${total}\nItems: ${items.length}`);
//     closeModal('createOrderModal');
// }

// function handleAssetSubmission(event) {
//     event.preventDefault();
//     const formData = new FormData(event.target);
//     const assetData = Object.fromEntries(formData.entries());
    
//     // Generate asset ID if not provided
//     if (!assetData.assetId) {
//         assetData.assetId = 'AST-' + Date.now().toString().slice(-6);
//     }
    
//     console.log('New asset:', assetData);
//     alert(`Asset ${assetData.assetName} added successfully!\nAsset ID: ${assetData.assetId}\nValue: $${assetData.purchasePrice}`);
//     closeModal('addAssetModal');
// }

document.addEventListener('DOMContentLoaded', () => {
    showSection('staff')
})