import { useState } from "react";
import api from "../api/axios";

export default function RegisterPage() {
  const [form, setForm] = useState({});

  const submit = async () => {
    try {
      await api.post("/register/", form);
      alert("Registered!");
    } catch (e) {
      alert(JSON.stringify(e.response.data));
    }
  };

  return (
    <div className="container">
      <h2>Register</h2>
      <input placeholder="username" onChange={e => setForm({...form, username: e.target.value})} />
      <input placeholder="full_name" onChange={e => setForm({...form, full_name: e.target.value})} />
      <input placeholder="email" onChange={e => setForm({...form, email: e.target.value})} />
      <input type="password" placeholder="password" onChange={e => setForm({...form, password: e.target.value})} />
      <button onClick={submit}>Register</button>
    </div>
  );
}