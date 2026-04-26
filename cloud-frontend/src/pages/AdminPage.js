import { useEffect, useState } from "react";
import api from "../api/axios";
import "../index.css";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

export default function AdminPage() {
  const { isAdmin, isAuth } = useSelector(s => s.auth);
  const nav = useNavigate();

  const [users, setUsers] = useState([]);
  const [next, setNext] = useState(null);
  const [prev, setPrev] = useState(null);

  // 🔥 загрузка пользователей
  const load = async (url = "/users/") => {
    try {
      const res = await api.get(url);

      setUsers(res.data.results);
      setNext(res.data.next);
      setPrev(res.data.previous);

    } catch (e) {
      console.error("Failed to load users", e);
    }
  };

  useEffect(() => {
    if (isAuth && isAdmin) {
      load();
    }
  }, [isAuth, isAdmin]);

  if (!isAuth) {
    return <div>Please login</div>;
  }

  if (!isAdmin) {
    return <div>Access denied</div>;
  }

  const toggleAdmin = async (id) => {
    await api.patch(`/users/${id}/admin/`);
    load();
  };

  const deleteUser = async (id) => {
    if (!window.confirm("Delete user?")) return;

    await api.delete(`/users/${id}/`);
    load();
  };

  return (
    <div className="container">
      <h2>👑 Admin Panel</h2>

      {users.map(u => (
        <div key={u.id} className="card">
          <b>{u.username}</b> ({u.email})

          <div>Files: {u.file_count}</div>
          <div>Size: {(u.total_size / 1024 / 1024).toFixed(2)} MB</div>
          <div>Admin: {u.is_admin ? "Yes" : "No"}</div>

          <button onClick={() => toggleAdmin(u.id)}>
            Toggle Admin
          </button>

          <button onClick={() => deleteUser(u.id)}>
            Delete
          </button>

          <button onClick={() => nav(`/storage?user=${u.id}`)}>
            Open Storage
          </button>
        </div>
      ))}

      {/* пагинация */}
      <div style={{ marginTop: 20 }}>
        {prev && <button onClick={() => load(prev)}>⬅ Prev</button>}
        {next && <button onClick={() => load(next)}>Next ➡</button>}
      </div>
    </div>
  );
}