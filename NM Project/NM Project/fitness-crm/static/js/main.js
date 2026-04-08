// Global state
let updateInterval = null;
let charts = {};
const API_BASE = '/api';
let currentUser = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication first
    AuthManager.requireAuth();
    
    // Get current user
    currentUser = AuthManager.getUser();
    
    // Initialize UI with user info
    initializeUserProfile();
    initNavigation();
    initEventListeners();
    loadDashboard();
    startRealtimeUpdates();
});

// ==================== User Profile Management ====================

function initializeUserProfile() {
    if (currentUser) {
        document.getElementById('userDisplayName').textContent = currentUser.name;
        document.getElementById('userDisplayRole').textContent = currentUser.role;
    }
}

function toggleUserDropdown(e) {
    e.stopPropagation();
    const menu = document.getElementById('userDropdownMenu');
    menu.classList.toggle('active');
}

function closeUserDropdown() {
    document.getElementById('userDropdownMenu').classList.remove('active');
}

function viewProfile() {
    closeUserDropdown();
    console.log('User Profile:', currentUser);
    // You can implement a profile modal here
    alert(`Profile: ${currentUser.name} (${currentUser.role})\nEmail: ${currentUser.email}`);
}

function logout() {
    closeUserDropdown();
    if (confirm('Are you sure you want to logout?')) {
        AuthManager.logout();
        // Call logout API
        fetch(`${API_BASE}/auth/logout`, { method: 'POST' })
            .then(() => {
                window.location.href = '/';
            });
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.user-profile')) {
        closeUserDropdown();
    }
});

// Add click handler to user profile
document.addEventListener('DOMContentLoaded', () => {
    const userProfile = document.getElementById('userProfileDropdown');
    if (userProfile) {
        userProfile.addEventListener('click', toggleUserDropdown);
    }
});

// ==================== Navigation ====================

function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.dataset.section;
            switchSection(section);
        });
    });
}

function switchSection(section) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    
    // Show selected section
    const sectionId = `${section}-section`;
    const sectionElement = document.getElementById(sectionId);
    if (sectionElement) {
        sectionElement.classList.add('active');
    }
    
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.section === section) {
            link.classList.add('active');
        }
    });
    
    // Update page title
    const titles = {
        dashboard: 'Dashboard',
        members: 'Members Management',
        trainers: 'Trainers Management',
        classes: 'Classes & Schedules',
        payments: 'Payment Management',
        attendance: 'Attendance Records',
        analytics: 'Analytics & Reports'
    };
    document.getElementById('pageTitle').textContent = titles[section] || 'Dashboard';
    
    // Load section data
    if (section === 'members') loadMembers();
    else if (section === 'trainers') loadTrainers();
    else if (section === 'classes') loadClasses();
    else if (section === 'payments') loadPayments();
    else if (section === 'attendance') loadAttendance();
    else if (section === 'analytics') loadAnalytics();
}

// ==================== Event Listeners ====================

function initEventListeners() {
    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', () => {
        location.reload();
    });

    // Toggle sidebar
    document.getElementById('toggleSidebar').addEventListener('click', () => {
        document.querySelector('.sidebar').classList.toggle('collapsed');
        document.querySelector('.main-content').style.marginLeft = 
            document.querySelector('.sidebar').classList.contains('collapsed') ? '0' : '280px';
    });

    // Close sidebar on mobile when clicking nav link
    if (window.innerWidth <= 768) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                document.querySelector('.sidebar').classList.add('collapsed');
            });
        });
    }
}

// ==================== Dashboard ====================

async function loadDashboard() {
    try {
        const [analytics, payments, classes, members, trainers, attendance] = await Promise.all([
            fetch(`${API_BASE}/analytics`).then(r => r.json()),
            fetch(`${API_BASE}/payments/stats`).then(r => r.json()),
            fetch(`${API_BASE}/classes/stats`).then(r => r.json()),
            fetch(`${API_BASE}/members/stats`).then(r => r.json()),
            fetch(`${API_BASE}/trainers/stats`).then(r => r.json()),
            fetch(`${API_BASE}/attendance/stats`).then(r => r.json())
        ]);

        // Update KPI cards
        document.getElementById('totalRevenue').textContent = `$${analytics.total_revenue.toLocaleString()}`;
        document.getElementById('totalMembers').textContent = members.total_members;
        document.getElementById('activeSessions').textContent = analytics.active_classes;
        document.getElementById('avgOccupancy').textContent = analytics.avg_occupancy + '%';
        document.getElementById('memberRetention').textContent = analytics.member_retention_rate + '%';
        document.getElementById('availableTrainers').textContent = trainers.available;

        // Update trainer status
        document.getElementById('trainersAvailable').textContent = trainers.available;
        document.getElementById('trainersInSession').textContent = trainers.in_session;
        document.getElementById('trainersOnBreak').textContent = trainers.in_session;

        // Load charts
        loadCharts();

        // Load recent activity
        loadRecentActivity();

    } catch (error) {
        console.error('Error loading dashboard:', error);
        showNotification('Error loading dashboard data', 'error');
    }
}

async function loadCharts() {
    try {
        const revenueData = await fetch(`${API_BASE}/revenue/by-plan`).then(r => r.json());
        
        // Revenue chart
        const revenueCtx = document.getElementById('revenueChart');
        if (revenueCtx && !charts.revenue) {
            charts.revenue = new Chart(revenueCtx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(revenueData),
                    datasets: [{
                        data: Object.values(revenueData),
                        backgroundColor: [
                            '#6366f1',
                            '#ec4899',
                            '#3b82f6'
                        ],
                        borderColor: '#1e293b',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            labels: { color: '#f1f5f9' }
                        }
                    }
                }
            });
        } else if (charts.revenue) {
            charts.revenue.data.datasets[0].data = Object.values(revenueData);
            charts.revenue.update();
        }
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

async function loadRecentActivity() {
    try {
        const payments = await fetch(`${API_BASE}/payments?limit=5`).then(r => r.json());
        const attendance = await fetch(`${API_BASE}/attendance?limit=5`).then(r => r.json());
        
        const activities = [
            ...payments.map(p => ({
                type: 'payment',
                text: `${p.member_name} made a payment of $${p.amount}`,
                time: p.payment_date,
                icon: '💳'
            })),
            ...attendance.map(a => ({
                type: 'checkin',
                text: `${a.member_name} checked in for ${a.class_name}`,
                time: a.check_in_time,
                icon: '✅'
            }))
        ].sort((a, b) => new Date(b.time) - new Date(a.time)).slice(0, 10);

        let html = '';
        activities.forEach(activity => {
            const timeago = getTimeAgo(activity.time);
            const iconClass = activity.type === 'payment' ? 'payment' : 'checkin';
            html += `
                <div class="activity-item">
                    <div class="activity-icon ${iconClass}">${activity.icon}</div>
                    <div class="activity-content">
                        <div class="activity-text">${activity.text}</div>
                        <div class="activity-time">${timeago}</div>
                    </div>
                </div>
            `;
        });

        document.getElementById('activityFeed').innerHTML = html || '<p class="empty-state">No recent activity</p>';
    } catch (error) {
        console.error('Error loading recent activity:', error);
    }
}

// ==================== Members ====================

async function loadMembers() {
    try {
        const [members, stats] = await Promise.all([
            fetch(`${API_BASE}/members`).then(r => r.json()),
            fetch(`${API_BASE}/members/stats`).then(r => r.json())
        ]);

        // Update stats
        document.getElementById('stat-total-members').textContent = stats.total_members;
        document.getElementById('stat-active-members').textContent = stats.active_members;
        document.getElementById('stat-pending-renewals').textContent = stats.pending_renewals;
        document.getElementById('stat-new-members').textContent = stats.new_this_month;

        // Populate table
        const tbody = document.querySelector('#membersTable tbody');
        tbody.innerHTML = members.map(m => `
            <tr>
                <td><strong>${m.name}</strong></td>
                <td>${m.email}</td>
                <td>${m.membership_plan}</td>
                <td><span class="status-badge ${m.status.toLowerCase()}">${m.status}</span></td>
                <td>${m.join_date}</td>
                <td>${m.renewal_date || '-'}</td>
                <td>${m.total_classes}</td>
                <td><button class="action-btn"><i class="fas fa-edit"></i></button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading members:', error);
        showNotification('Error loading members', 'error');
    }
}

// ==================== Trainers ====================

async function loadTrainers() {
    try {
        const [trainers, stats] = await Promise.all([
            fetch(`${API_BASE}/trainers`).then(r => r.json()),
            fetch(`${API_BASE}/trainers/stats`).then(r => r.json())
        ]);

        // Update stats
        document.getElementById('stat-total-trainers').textContent = stats.total_trainers;
        document.getElementById('stat-trainers-available').textContent = stats.available;
        document.getElementById('stat-trainers-in-session').textContent = stats.in_session;
        document.getElementById('stat-avg-rating').textContent = stats.avg_rating + '★';

        // Populate table
        const tbody = document.querySelector('#trainersTable tbody');
        tbody.innerHTML = trainers.map(t => `
            <tr>
                <td><strong>${t.name}</strong></td>
                <td>${t.specialization}</td>
                <td>${t.experience_years} years</td>
                <td>${t.rating}★</td>
                <td><span class="status-badge ${t.status.toLowerCase().replace(' ', '-')}">${t.status}</span></td>
                <td>${t.availability}</td>
                <td><button class="action-btn"><i class="fas fa-edit"></i></button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading trainers:', error);
        showNotification('Error loading trainers', 'error');
    }
}

// ==================== Classes ====================

async function loadClasses() {
    try {
        const [classes, stats] = await Promise.all([
            fetch(`${API_BASE}/classes`).then(r => r.json()),
            fetch(`${API_BASE}/classes/stats`).then(r => r.json())
        ]);

        // Update stats
        document.getElementById('stat-total-classes').textContent = stats.total_classes;
        document.getElementById('stat-scheduled-classes').textContent = stats.scheduled;
        document.getElementById('stat-in-progress-classes').textContent = stats.in_progress;
        document.getElementById('stat-class-occupancy').textContent = stats.avg_occupancy + '%';

        // Populate table
        const tbody = document.querySelector('#classesTable tbody');
        tbody.innerHTML = classes.map(c => `
            <tr>
                <td><strong>${c.name}</strong></td>
                <td>${c.type}</td>
                <td>${c.trainer_name}</td>
                <td>${c.schedule_time}</td>
                <td>${c.current_enrollment}/${c.max_capacity}</td>
                <td><div class="occupancy-bar" style="width: ${c.utilization}%">${c.utilization}%</div></td>
                <td><span class="status-badge ${c.status.toLowerCase().replace(' ', '-')}">${c.status}</span></td>
                <td><button class="action-btn"><i class="fas fa-edit"></i></button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading classes:', error);
        showNotification('Error loading classes', 'error');
    }
}

// ==================== Payments ====================

async function loadPayments() {
    try {
        const [payments, stats] = await Promise.all([
            fetch(`${API_BASE}/payments`).then(r => r.json()),
            fetch(`${API_BASE}/payments/stats`).then(r => r.json())
        ]);

        // Update stats
        document.getElementById('stat-total-transactions').textContent = stats.total_transactions;
        document.getElementById('stat-completed-payments').textContent = stats.completed;
        document.getElementById('stat-payment-revenue').textContent = `$${stats.total_revenue.toLocaleString()}`;
        document.getElementById('stat-avg-transaction').textContent = `$${stats.avg_transaction.toLocaleString()}`;

        // Populate table
        const tbody = document.querySelector('#paymentsTable tbody');
        tbody.innerHTML = payments.map(p => `
            <tr>
                <td>${p.member_name}</td>
                <td>$${p.amount.toLocaleString()}</td>
                <td>${p.payment_date}</td>
                <td>${p.payment_type}</td>
                <td><span class="status-badge ${p.status.toLowerCase()}">${p.status}</span></td>
                <td><button class="action-btn"><i class="fas fa-eye"></i></button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading payments:', error);
        showNotification('Error loading payments', 'error');
    }
}

// ==================== Attendance ====================

async function loadAttendance() {
    try {
        const [attendance, stats] = await Promise.all([
            fetch(`${API_BASE}/attendance`).then(r => r.json()),
            fetch(`${API_BASE}/attendance/stats`).then(r => r.json())
        ]);

        // Update stats
        document.getElementById('stat-today-checkins').textContent = stats.today_checkins;
        document.getElementById('stat-week-checkins').textContent = stats.this_week_checkins;
        document.getElementById('stat-total-attendance').textContent = stats.total_records;
        document.getElementById('stat-avg-daily').textContent = stats.avg_daily_attendance;

        // Populate table
        const tbody = document.querySelector('#attendanceTable tbody');
        tbody.innerHTML = attendance.map(a => `
            <tr>
                <td>${a.member_name}</td>
                <td>${a.class_name}</td>
                <td>${a.check_in_time}</td>
                <td>60 min</td>
                <td><button class="action-btn"><i class="fas fa-trash"></i></button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading attendance:', error);
        showNotification('Error loading attendance', 'error');
    }
}

// ==================== Analytics ====================

async function loadAnalytics() {
    try {
        const topTrainers = await fetch(`${API_BASE}/trainers/top-rated`).then(r => r.json());
        
        // Top trainers list
        let html = '';
        topTrainers.forEach((trainer, index) => {
            html += `
                <div class="trainer-card">
                    <div>
                        <div class="trainer-name">#${index + 1} ${trainer.name}</div>
                        <small class="text-muted">${trainer.specialization}</small>
                    </div>
                    <div class="trainer-rating">${trainer.rating}★</div>
                </div>
            `;
        });
        document.getElementById('topTrainersList').innerHTML = html;

        // Initialize sample charts
        initAnalyticsCharts();
    } catch (error) {
        console.error('Error loading analytics:', error);
        showNotification('Error loading analytics', 'error');
    }
}

function initAnalyticsCharts() {
    // Member Growth Chart
    const growthCtx = document.getElementById('memberGrowthChart');
    if (growthCtx && !charts.growth) {
        charts.growth = new Chart(growthCtx, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [{
                    label: 'New Members',
                    data: [12, 19, 15, 25],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { labels: { color: '#f1f5f9' } }
                },
                scales: {
                    y: { ticks: { color: '#f1f5f9' } },
                    x: { ticks: { color: '#f1f5f9' } }
                }
            }
        });
    }

    // Class Type Distribution
    const typeCtx = document.getElementById('classTypeChart');
    if (typeCtx && !charts.type) {
        charts.type = new Chart(typeCtx, {
            type: 'pie',
            data: {
                labels: ['Yoga', 'Cardio', 'Strength', 'Pilates', 'CrossFit'],
                datasets: [{
                    data: [15, 22, 18, 12, 10],
                    backgroundColor: ['#6366f1', '#ec4899', '#3b82f6', '#10b981', '#f59e0b']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { labels: { color: '#f1f5f9' } }
                }
            }
        });
    }

    // Payment Trends
    const paymentCtx = document.getElementById('paymentTrendsChart');
    if (paymentCtx && !charts.payment) {
        charts.payment = new Chart(paymentCtx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Daily Revenue',
                    data: [850, 920, 780, 1050, 990, 1200, 950],
                    backgroundColor: '#10b981'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { labels: { color: '#f1f5f9' } }
                },
                scales: {
                    y: { ticks: { color: '#f1f5f9' } },
                    x: { ticks: { color: '#f1f5f9' } }
                }
            }
        });
    }
}

// ==================== Real-time Updates ====================

function startRealtimeUpdates() {
    updateRealtimeData();
    updateInterval = setInterval(updateRealtimeData, 5000); // Update every 5 seconds
}

async function updateRealtimeData() {
    try {
        const data = await fetch(`${API_BASE}/realtime-data`).then(r => r.json());
        
        // You can use this data to update specific UI elements in real-time
        // without full page refresh
        console.log('Real-time data:', data);
        
        // Update notification badge if there are changes
        const notificationBadge = document.getElementById('notificationBadge');
        if (data.recent_payments > 0) {
            notificationBadge.textContent = parseInt(notificationBadge.textContent) + 1;
        }
    } catch (error) {
        console.error('Error updating real-time data:', error);
    }
}

// ==================== Utility Functions ====================

function getTimeAgo(date) {
    const now = new Date();
    const then = new Date(date);
    const diff = Math.floor((now - then) / 1000);

    if (diff < 60) return 'just now';
    if (diff < 3600) return Math.floor(diff / 60) + ' minutes ago';
    if (diff < 86400) return Math.floor(diff / 3600) + ' hours ago';
    if (diff < 604800) return Math.floor(diff / 86400) + ' days ago';
    return Math.floor(diff / 604800) + ' weeks ago';
}

function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // You can implement a toast notification here
    // For now, we'll just use console
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Stop updates when user closes the page
window.addEventListener('beforeunload', () => {
    if (updateInterval) clearInterval(updateInterval);
});
