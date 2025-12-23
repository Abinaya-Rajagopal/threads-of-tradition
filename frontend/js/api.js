/**
 * API Helper - Threads of Tradition
 * Utility functions for making HTTP requests to the backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Make an API request
 * @param {string} endpoint - API endpoint (without base URL)
 * @param {object} options - Fetch options
 * @returns {Promise<object>} - JSON response
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Get token from localStorage
    const token = localStorage.getItem('token');
    
    // Set default headers
    const headers = {
        ...options.headers
    };
    
    // Add auth header if token exists
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Add content-type for JSON requests
    if (options.body && !(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(options.body);
    }
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * API methods for Artisan operations
 */
const ArtisanAPI = {
    register: (formData) => apiRequest('/artisan/register', {
        method: 'POST',
        body: formData
    }),
    
    login: (credentials) => apiRequest('/artisan/login', {
        method: 'POST',
        body: credentials
    }),
    
    getProfile: () => apiRequest('/artisan/profile'),
    
    updateProfile: (data) => apiRequest('/artisan/profile', {
        method: 'PUT',
        body: data
    }),
    
    getMyProducts: () => apiRequest('/artisan/products')
};

/**
 * API methods for Product operations
 */
const ProductAPI = {
    getMaterials: () => apiRequest('/products/materials'),
    
    generateCaption: (data) => apiRequest('/products/generate-caption', {
        method: 'POST',
        body: data
    }),
    
    recommendPrice: (data) => apiRequest('/products/recommend-price', {
        method: 'POST',
        body: data
    }),
    
    upload: (formData) => apiRequest('/products/upload', {
        method: 'POST',
        body: formData
    }),
    
    list: (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.material) params.append('material', filters.material);
        if (filters.min_price) params.append('min_price', filters.min_price);
        if (filters.max_price) params.append('max_price', filters.max_price);
        if (filters.verified_only) params.append('verified_only', 'true');
        
        const queryString = params.toString();
        return apiRequest(`/products/${queryString ? '?' + queryString : ''}`);
    },
    
    get: (id) => apiRequest(`/products/${id}`),
    
    delete: (id) => apiRequest(`/products/${id}`, {
        method: 'DELETE'
    })
};

/**
 * API methods for Admin operations
 */
const AdminAPI = {
    login: (credentials) => apiRequest('/admin/login', {
        method: 'POST',
        body: credentials
    }),
    
    listArtisans: (status = null) => {
        const params = status ? `?status=${status}` : '';
        return apiRequest(`/admin/artisans${params}`);
    },
    
    getArtisan: (id) => apiRequest(`/admin/artisans/${id}`),
    
    verifyArtisan: (id, action) => apiRequest(`/admin/artisans/${id}/verify`, {
        method: 'POST',
        body: { action }
    }),
    
    getStats: () => apiRequest('/admin/stats')
};

/**
 * Health check
 */
const checkHealth = () => apiRequest('/health');

// Export for use in other scripts
window.API = {
    base: API_BASE_URL,
    request: apiRequest,
    Artisan: ArtisanAPI,
    Product: ProductAPI,
    Admin: AdminAPI,
    checkHealth
};
