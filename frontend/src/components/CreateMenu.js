// frontend/src/components/CreateMenu.js

import React, { useState, useContext } from 'react';
import api from '../services/api';
import { AuthContext } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const CreateMenu = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [image, setImage] = useState(null);
    const { authTokens } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('title', title);
        formData.append('description', description);
        if (image) {
            formData.append('image', image);
        }

        try {
            const response = await api.post('/api/menus/', formData, {
                headers: {
                    Authorization: `Bearer ${authTokens.access}`,
                    'Content-Type': 'multipart/form-data',
                },
            });
            if (response.status === 201) {
                navigate('/menus');
            }
        } catch (error) {
            console.error('Error creating menu:', error);
            alert('Failed to create menu. Please try again.');
        }
    };

    return (
        <div className="container mt-5">
            <h2>Create New Menu</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="title" className="form-label">Title</label>
                    <input
                        type="text"
                        className="form-control"
                        id="title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="description" className="form-label">Description</label>
                    <textarea
                        className="form-control"
                        id="description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                    ></textarea>
                </div>
                <div className="mb-3">
                    <label htmlFor="image" className="form-label">Image</label>
                    <input
                        type="file"
                        className="form-control"
                        id="image"
                        accept="image/*"
                        onChange={(e) => setImage(e.target.files[0])}
                    />
                </div>
                <button type="submit" className="btn btn-primary">Create Menu</button>
            </form>
        </div>
    );
};

export default CreateMenu;
