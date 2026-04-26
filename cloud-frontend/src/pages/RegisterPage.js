import { useState } from "react";
import api from "../api/axios";

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: "",
    full_name: "",
    email: "",
    password: ""
  });

  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};

    const usernameRegex = /^[A-Za-z][A-Za-z0-9]{3,19}$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{6,}$/;

    if (!usernameRegex.test(form.username)) {
      newErrors.username = "Username must be 4-20 chars, start with letter";
    }

    if (!emailRegex.test(form.email)) {
      newErrors.email = "Invalid email format";
    }

    if (!passwordRegex.test(form.password)) {
      newErrors.password =
        "Password must contain 6+ chars, uppercase, number, special symbol";
    }

    if (!form.full_name) {
      newErrors.full_name = "Full name required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const submit = async () => {
    if (!validate()) return;

    try {
      await api.post("/register/", form);
      alert("Registered!");
    } catch (e) {
      alert("Registration failed");
    }
  };

  return (
    <div className="container">
      <h2>Register</h2>

      <input
        placeholder="Username"
        onChange={(e) => setForm({ ...form, username: e.target.value })}
      />
      {errors.username && <div style={{ color: "red" }}>{errors.username}</div>}

      <input
        placeholder="Full name"
        onChange={(e) => setForm({ ...form, full_name: e.target.value })}
      />
      {errors.full_name && <div style={{ color: "red" }}>{errors.full_name}</div>}

      <input
        placeholder="Email"
        onChange={(e) => setForm({ ...form, email: e.target.value })}
      />
      {errors.email && <div style={{ color: "red" }}>{errors.email}</div>}

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />
      {errors.password && <div style={{ color: "red" }}>{errors.password}</div>}

      <button onClick={submit}>Register</button>
    </div>
  );
}