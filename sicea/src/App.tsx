import React from 'react';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import { useAuth } from './hooks/AuthContext';
import FileUpload from "./components/FileUpload.tsx";

function App() {
  const { isAuthenticated, loading } = useAuth();

  console.log('Authentication Status:', isAuthenticated, 'Loading:', loading);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p>Cargando...</p>
        </div>
      </div>
    );
  }

  return isAuthenticated ? <FileUpload /> : <LoginPage />;
}

export default App;
