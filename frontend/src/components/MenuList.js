// frontend/src/components/MenuList.js

import React, { useEffect, useState, useContext } from 'react';
import api from '../services/api';
import { AuthContext } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';

const MenuList = () => {
    const [menus, setMenus] = useState([]);
    const { authTokens } = useContext(AuthContext);

    useEffect(() => {
        const fetchMenus = async () => {
            try {
                const response = await api.get('/api/menus/', {
                    headers: {
                        Authorization: `Bearer ${authTokens.access}`,
                    },
                });
                setMenus(response.data);
            } catch (error) {
                console.error('Error fetching menus:', error);
            }
        };
        fetchMenus();
    }, [authTokens]);

    const deleteMenu = async (id) => {
        if (window.confirm('Are you sure you want to delete this menu?')) {
            try {
                await api.delete(`/api/menus/${id}/`, {
                    headers: {
                        Authorization: `Bearer ${authTokens.access}`,
                    },
                });
                setMenus(menus.filter(menu => menu.id !== id));
            } catch (error) {
                console.error('Error deleting menu:', error);
            }
        }
    };

    return (
        <div className="container mt-5">
            <h2>Your Menus</h2>
            <Link to="/create-menu" className="btn btn-primary mb-3">Add New Menu</Link>
            {menus.length > 0 ? (
                <div className="row">
                    {menus.map(menu => (
                        <div className="col-md-4" key={menu.id}>
                            <div className="card mb-4">
                                {menu.image && <img src={menu.image} className="card-img-top" alt={menu.title} />}
                                <div className="card-body">
                                    <h5 className="card-title">{menu.title}</h5>
                                    <p className="card-text">{menu.description}</p>
                                    <button className="btn btn-danger" onClick={() => deleteMenu(menu.id)}>Delete</button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <p>No menus available.</p>
            )}
        </div>
    );
};

export default MenuList;
