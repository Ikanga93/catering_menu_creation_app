
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Register from './components/Register';
import Login from './components/Login';
import MenuList from './components/MenuList';
import CreateMenu from './components/CreateMenu';
import PrivateRoute from './components/PrivateRoute';

const App = () => {
  return (
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
              {/* Add other routes here */}
          </Routes>
      </Router>
  );
};

export default App;
