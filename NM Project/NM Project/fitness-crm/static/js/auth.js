// Authentication helpers

class AuthManager {
    static getUser() {
        const userStr = sessionStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }

    static setUser(user) {
        sessionStorage.setItem('user', JSON.stringify(user));
    }

    static logout() {
        sessionStorage.removeItem('user');
    }

    static isAuthenticated() {
        return this.getUser() !== null;
    }

    static requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '/';
        }
    }
}

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    AuthManager.requireAuth();
});
