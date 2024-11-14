
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Register from './components/Register';
import Login from './components/Login';
import MenuList from './components/MenuList';
import CreateMenu from './components/CreateMenu';
import EditMenu from './components/EditMenu';
import PrivateRoute from './components/PrivateRoute';
import { AuthProvider } from './contexts/AuthContext'; // Import AuthProvider
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';


const App = () => {
  return (
    <AuthProvider> {/* Wrap with AuthProvider */}
      <Router>
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
          <ToastContainer /> {/* Add ToastContainer for notifications */}
      </Router>
    </AuthProvider>
  );
};

export default App;
