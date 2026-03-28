import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AdminPage from "./pages/AdminPage";
import StoragePage from "./pages/StoragePage";
import Navbar from "./components/Navbar";
import api from "./api/axios";
import { useEffect } from "react";

function App() {
    useEffect(() => {
    api.get("/login/"); // или любой GET
  }, []);
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/storage" element={<StoragePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;