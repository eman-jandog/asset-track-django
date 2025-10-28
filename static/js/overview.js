import { showSection } from './global.js';

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
    initializeDashboard();
    showSection('overview')
})