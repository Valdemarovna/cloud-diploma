import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../features/auth/authSlice";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { isAuth } = useSelector((s) => s.auth);
  const dispatch = useDispatch();

  const nav = useNavigate();

  const handleLogout = async () => {
    await api.post("/logout/");
    dispatch(logout());
    nav("/"); // 👈 редирект
  };

  return (
    <div style={{
      background: "#222",
      color: "white",
      padding: "10px 20px",
      display: "flex",
      justifyContent: "space-between"
    }}>
      <div>
        <Link to="/" style={{ color: "white", marginRight: 10 }}>Cloud</Link>
      </div>

      <div>
        {!isAuth && (
          <>
            <Link to="/login" style={{ color: "white", marginRight: 10 }}>Login</Link>
            <Link to="/register" style={{ color: "white" }}>Register</Link>
          </>
        )}

        {isAuth && (
          <>
            <Link to="/storage">Storage</Link>
            <Link to="/admin">Admin</Link>
            <button onClick={handleLogout}>Logout</button>
          </>
        )}
      </div>
    </div>
  );
}