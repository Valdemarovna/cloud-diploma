import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../store/authSlice";
import axios from "axios";

function Navbar() {
  const dispatch = useDispatch();
  const isAuth = useSelector(state => state.auth.isAuthenticated);
  const user = useSelector(state => state.auth.user);

  const handleLogout = async () => {
    await axios.post("/api/logout/", {}, { withCredentials: true });

    dispatch(logout());
    localStorage.removeItem("user");
  };

  return (
    <nav>
      <Link to="/">Главная</Link>

      {isAuth ? (
        <>
          <Link to="/storage">Хранилище</Link>

          {user?.is_admin && <Link to="/admin">Админ</Link>}

          <button onClick={handleLogout}>Выход</button>
        </>
      ) : (
        <>
          <Link to="/login">Вход</Link>
          <Link to="/register">Регистрация</Link>
        </>
      )}
    </nav>
  );
}

export default Navbar;