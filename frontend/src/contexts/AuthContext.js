// src/contexts/AuthContext.js

import React, { createContext, useState, useEffect, useCallback } from 'react';
import api from '../services/api';
import { jwtDecode } from 'jwt-decode'; // Named import for v4.x
import { toast } from 'react-toastify';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
  );
  const [user, setUser] = useState(() =>
    localStorage.getItem('authTokens') ? jwtDecode(JSON.parse(localStorage.getItem('authTokens')).access) : null
  );

  const loginUser = async (username, password) => {
    try {
      const response = await api.post('/api/token/', { username, password });
      if (response.status === 200) {
        setAuthTokens(response.data);
        setUser(jwtDecode(response.data.access));
        localStorage.setItem('authTokens', JSON.stringify(response.data));
        toast.success('Logged in successfully!');
        return true;
      }
    } catch (error) {
      console.error('Login failed:', error);
      toast.error('Login failed. Please check your credentials.');
      return false;
    }
  };

  const registerUser = async (username, email, password, password2) => {
    try {
      const response = await api.post('/api/register/', { username, email, password, password2 });
      if (response.status === 201) {
        toast.success('Registration successful! Please log in.');
        return true;
      }
    } catch (error) {
      console.error('Registration failed:', error);
      if (error.response && error.response.data) {
        const errors = error.response.data;
        Object.keys(errors).forEach(key => {
          toast.error(`${key}: ${errors[key]}`);
        });
      } else {
        toast.error('Registration failed. Please try again.');
      }
      return false;
    }
  };

  const logoutUser = useCallback(() => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    toast.info('Logged out successfully.');
  }, []);


  // Function to refresh JWT token
  const refreshToken = useCallback(async () => {
    if (!authTokens?.refresh) return;
    try {
      const response = await api.post('/api/token/refresh/', { refresh: authTokens.refresh });
      setAuthTokens({
        access: response.data.access,
        refresh: authTokens.refresh,
      });
      setUser(jwtDecode(response.data.access));
      localStorage.setItem('authTokens', JSON.stringify({
        access: response.data.access,
        refresh: authTokens.refresh,
      }));
      toast.info('Session refreshed.');
    } catch (error) {
      console.error('Token refresh failed:', error);
      logoutUser();
    }
  }, [authTokens, logoutUser]);

  // Effect to periodically refresh token
  useEffect(() => {
    if (authTokens) {
      const interval = setInterval(() => {
        refreshToken();
      }, 4 * 60 * 1000); // Refresh token every 4 minutes
      return () => clearInterval(interval);
    }
  }, [authTokens, refreshToken]);

  return (
    <AuthContext.Provider value={{ user, authTokens, loginUser, registerUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
};
