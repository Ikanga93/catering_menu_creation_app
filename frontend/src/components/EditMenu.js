// src/components/EditMenu.js

import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { AuthContext } from '../contexts/AuthContext';
import { toast } from 'react-toastify';

const EditMenu = () => {
  const { id } = useParams(); // Get the menu ID from the URL
  const navigate = useNavigate();
  const { authTokens } = useContext(AuthContext);

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState(null);

  useEffect(() => {
    // Fetch the existing menu data to populate the form
    const fetchMenu = async () => {
      try {
        const response = await api.get(`/api/menus/${id}/`, {
          headers: {
            Authorization: `Bearer ${authTokens.access}`,
          },
        });
        setTitle(response.data.title);
        setDescription(response.data.description);
        // Assuming image is a URL; handle accordingly if it's different
      } catch (error) {
        console.error('Error fetching menu:', error);
        toast.error('Failed to fetch menu data.');
      }
    };

    fetchMenu();
  }, [id, authTokens]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    if (image) {
      formData.append('image', image);
    }

    try {
      const response = await api.put(`/api/menus/${id}/`, formData, {
        headers: {
          Authorization: `Bearer ${authTokens.access}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      toast.success('Menu updated successfully!');
      navigate('/menus'); // Redirect to the menus page
    } catch (error) {
      console.error('Error updating menu:', error);
      toast.error('Failed to update menu.');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Edit Menu</h2>
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
            rows="3"
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
            onChange={(e) => setImage(e.target.files[0])}
          />
        </div>
        <button type="submit" className="btn btn-primary">Update Menu</button>
      </form>
    </div>
  );
};

export default EditMenu;

/*
Explanation of the EditMenu Component:

Imports:

useParams: To extract the id parameter from the URL.
useNavigate: To programmatically navigate after successful updates.
AuthContext: To access authentication tokens.
toast: To display notifications.
State Variables:

title, description, image: To manage form data.
useEffect:

Fetches existing menu data using the id from the URL.
Populates the form fields with the fetched data.
handleSubmit:

Handles form submission.
Sends a PUT request to update the menu.
On success, navigates back to the /menus page.
*/