// frontend/src/components/Register.js

import React, { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import api from '../services/api'; // Add this line
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';


const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState(''); // New email state
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const navigate = useNavigate();
    const { registerUser } = useContext(AuthContext);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== password2) {
            alert('Passwords do not match');
            return;
        }
        if (!email) {
            toast.error("Email is required.");
            return;
        }
        // Optionally, add email format validation here

        try {
            const response = await api.post('/register/', { username, email, password, password2 });
            if (response.status === 201) {
                toast.success("Registration successful! Please log in.");
                navigate('/login');
            }
        } catch (error) {
            console.error(error);
            toast.error("Registration failed. Please try again.");
        }
    };

    return (
        <div className="container mt-5">
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                {/* Username Field */}
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                        type="text"
                        className="form-control"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>

                {/* Email Field */}
                <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                        type="email" // Ensures email format
                        className="form-control"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                 {/* Password Field */}
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                        type="password"
                        className="form-control"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                {/* Confirm Password Field */}
                <div className="mb-3">
                    <label htmlFor="password2" className="form-label">Confirm Password</label>
                    <input
                        type="password"
                        className="form-control"
                        id="password2"
                        value={password2}
                        onChange={(e) => setPassword2(e.target.value)}
                        required
                    />
                </div>
                
                <button type="submit" className="btn btn-primary">Register</button>
            </form>
        </div>
    );
};

export default Register;
