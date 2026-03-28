import { useState } from "react";
import { useDispatch } from "react-redux";
import { login } from "../features/auth/authSlice";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [form, setForm] = useState({});
  const dispatch = useDispatch();
  const nav = useNavigate();

  const submit = async () => {
    const res = await dispatch(login(form));

    if (!res.error) {
      nav("/storage");
    }
  };

  return (
    <div className="container">
      <h2>Login</h2>
      <input placeholder="username" onChange={e => setForm({...form, username: e.target.value})} />
      <input type="password" placeholder="password" onChange={e => setForm({...form, password: e.target.value})} />
      <button onClick={submit}>Login</button>
    </div>
  );
}