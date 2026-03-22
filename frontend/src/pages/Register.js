import { useState } from "react";
import axios from "axios";

function Register() {
  const [form, setForm] = useState({});

  const handleRegister = async () => {
    try {
      await axios.post("/api/register/", form);
      alert("Успешно!");
    } catch (e) {
      alert("Ошибка регистрации");
    }
  };

  return (
    <div>
      <h2>Регистрация</h2>

      <input placeholder="Логин" onChange={e => setForm({ ...form, username: e.target.value })} />
      <input placeholder="ФИО" onChange={e => setForm({ ...form, full_name: e.target.value })} />
      <input placeholder="Email" onChange={e => setForm({ ...form, email: e.target.value })} />
      <input type="password" placeholder="Пароль" onChange={e => setForm({ ...form, password: e.target.value })} />

      <button onClick={handleRegister}>Зарегистрироваться</button>
    </div>
  );
}

export default Register;