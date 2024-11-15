// src/App.js

import React from 'react';
import { Routes, Route } from 'react-router-dom'; // No need to import BrowserRouter here
import Navbar from './components/Navbar';
import Home from './components/Home';
import Register from './components/Register';
import Login from './components/Login';
import MenuList from './components/MenuList';
import CreateMenu from './components/CreateMenu';
import EditMenu from './components/EditMenu';
import PrivateRoute from './components/PrivateRoute';
// Remove unnecessary imports
// import { AuthProvider } from './contexts/AuthContext'; // Not needed here
// import 'react-toastify/dist/ReactToastify.css';
// import { ToastContainer } from 'react-toastify';

const App = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/menus"
          element={
            <PrivateRoute>
              <MenuList />
            </PrivateRoute>
          }
        />
        <Route
          path="/create-menu"
          element={
            <PrivateRoute>
              <CreateMenu />
            </PrivateRoute>
          }
        />
        <Route
          path="/edit-menu/:id"
          element={
            <PrivateRoute>
              <EditMenu />
            </PrivateRoute>
          }
        />
        {/* Add other routes here */}
      </Routes>
      {/* Remove ToastContainer from App.js since it's already in index.js */}
    </>
  );
};

export default App;
