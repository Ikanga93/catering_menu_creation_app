// frontend/src/services/api.js

import axios from 'axios';

const api = axios.create({
    baseURL: '/api, http://127.0.0.1:8000', // Ensure this matches your backend URL
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add the Authorization header
api.interceptors.request.use(
    (config) => {
        const authTokens = localStorage.getItem('authTokens')
            ? JSON.parse(localStorage.getItem('authTokens'))
            : null;
        if (authTokens && authTokens.access) {
            config.headers.Authorization = `Bearer ${authTokens.access}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const refreshToken = JSON.parse(localStorage.getItem('authTokens'))?.refresh;
            if (refreshToken) {
                try {
                    const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', { refresh: refreshToken });
                    localStorage.setItem('authTokens', JSON.stringify({
                        access: response.data.access,
                        refresh: refreshToken,
                    }));
                    api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
                    originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    // Refresh token failed, logout the user
                    localStorage.removeItem('authTokens');
                    window.location.href = '/login';
                    return Promise.reject(refreshError);
                }
            } else {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;
