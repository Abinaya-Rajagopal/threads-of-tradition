/**
 * Authentication Helper - Threads of Tradition
 * Utility functions for managing authentication state
 */

const Auth = {
    /**
     * Store authentication data
     * @param {string} token - JWT token
     * @param {object} user - User data
     * @param {string} userType - 'artisan' or 'admin'
     */
    setAuth(token, user, userType) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('userType', userType);
    },

    /**
     * Get stored token
     * @returns {string|null}
     */
    getToken() {
        return localStorage.getItem('token');
    },

    /**
     * Get stored user data
     * @returns {object|null}
     */
    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    /**
     * Get user type
     * @returns {string|null}
     */
    getUserType() {
        return localStorage.getItem('userType');
    },

    /**
     * Check if user is authenticated
     * @returns {boolean}
     */
    isAuthenticated() {
        return !!this.getToken();
    },

    /**
     * Check if current user is an artisan
     * @returns {boolean}
     */
    isArtisan() {
        return this.getUserType() === 'artisan';
    },

    /**
     * Check if current user is an admin
     * @returns {boolean}
     */
    isAdmin() {
        return this.getUserType() === 'admin';
    },

    /**
     * Clear authentication data and logout
     */
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('userType');
    },

    /**
     * Require authentication - redirect if not authenticated
     * @param {string} redirectUrl - URL to redirect to if not authenticated
     */
    requireAuth(redirectUrl = '/frontend/artisan/login.html') {
        if (!this.isAuthenticated()) {
            window.location.href = redirectUrl;
            return false;
        }
        return true;
    },

    /**
     * Require artisan role
     */
    requireArtisan() {
        if (!this.isArtisan()) {
            window.location.href = '/frontend/artisan/login.html';
            return false;
        }
        return true;
    },

    /**
     * Require admin role
     */
    requireAdmin() {
        if (!this.isAdmin()) {
            window.location.href = '/frontend/admin/index.html';
            return false;
        }
        return true;
    }
};

// Export for use in other scripts
window.Auth = Auth;
