// frontend/src/contexts/AuthContext.js

import React, { createContext, useState, useEffect } from 'react';
import api from '../services/api';
import { jwtDecode } from 'jwt-decode';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
    );
    const [user, setUser] = useState(() =>
        localStorage.getItem('authTokens') ? jwt_decode(JSON.parse(localStorage.getItem('authTokens')).access) : null
    );

    const loginUser = async (username, password) => {
        try {
            const response = await api.post('/api/token/', { username, password });
            if (response.status === 200) {
                setAuthTokens(response.data);
                setUser(jwt_decode(response.data.access));
                localStorage.setItem('authTokens', JSON.stringify(response.data));
                return true;
            }
        } catch (error) {
            console.error('Login failed:', error);
            return false;
        }
    };

    const registerUser = async (username, password, password2) => {
        try {
            const response = await api.post('/api/register/', { username, password, password2 });
            if (response.status === 201) {
                return true;
            }
        } catch (error) {
            console.error('Registration failed:', error);
            return false;
        }
    };

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
    };

    const refreshToken = async () => {
        if (!authTokens) return;
        try {
            const response = await api.post('/api/token/refresh/', { refresh: authTokens.refresh });
            if (response.status === 200) {
                setAuthTokens(response.data);
                setUser(jwt_decode(response.data.access));
                localStorage.setItem('authTokens', JSON.stringify(response.data));
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
            logoutUser();
        }
    };

    useEffect(() => {
        if (authTokens) {
            const interval = setInterval(() => {
                refreshToken();
            }, 4 * 60 * 1000); // Refresh token every 4 minutes
            return () => clearInterval(interval);
        }
    }, [authTokens]);

    return (
        <AuthContext.Provider value={{ user, authTokens, loginUser, registerUser, logoutUser }}>
            {children}
        </AuthContext.Provider>
    );
};

/*
Explanation:

State Management:
authTokens: Stores the JWT access and refresh tokens.
user: Stores the decoded user information from the JWT.
Functions:
loginUser: Handles user login by obtaining JWT tokens.
registerUser: Handles user registration.
logoutUser: Clears authentication tokens and user state.
refreshToken: Refreshes the access token using the refresh token.
Effect Hook:
Sets up an interval to refresh the token periodically.
Provider:
Provides authentication state and functions to the entire application.
*/