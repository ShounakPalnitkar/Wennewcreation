// Auth middleware to protect routes
document.addEventListener('DOMContentLoaded', function() {
    // Skip auth check for login page
    if (window.location.pathname === '/login.html') return;
    
    const authToken = localStorage.getItem('authToken');
    
    if (!authToken) {
        window.location.href = '/login.html';
        return;
    }
    
    // Verify token with server on each page load
    fetch('/api/verify', {
        headers: {
            'Authorization': `Bearer ${authToken}`
        }
    }).then(response => {
        if (!response.ok) {
            localStorage.removeItem('authToken');
            window.location.href = '/login.html';
        }
    }).catch(() => {
        localStorage.removeItem('authToken');
        window.location.href = '/login.html';
    });
});

// Logout functionality
function logout() {
    localStorage.removeItem('authToken');
    window.location.href = '/login.html';
}
