import { useState } from "react";
import axios from "axios";
import { useDispatch } from "react-redux";
import { loginSuccess } from "../store/authSlice";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post(
        "/api/login/",
        { username, password },
        { withCredentials: true }
      );

      dispatch(loginSuccess(res.data.user));
      localStorage.setItem("user", JSON.stringify(res.data.user));

      navigate("/storage");
    } catch (e) {
      alert("Ошибка входа");
    }
  };

  return (
    <div>
      <h2>Вход</h2>
      <input placeholder="Логин" onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Пароль" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Войти</button>
    </div>
  );
}

export default Login;