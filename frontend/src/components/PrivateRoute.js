// frontend/src/components/PrivateRoute.js

import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

const PrivateRoute = ({ children }) => {
    const { authTokens } = useContext(AuthContext);

    return authTokens ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
