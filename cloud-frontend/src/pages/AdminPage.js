import { useEffect, useState } from "react";
import api from "../api/axios";
import "../index.css";
import { useNavigate } from "react-router-dom";

export default function AdminPage() {
  const [users, setUsers] = useState([]);

const nav = useNavigate();
const [loading, setLoading] = useState(true);

const load = async () => {
  try {
    const res = await api.get("/users/");
    setUsers(res.data);
  } catch (e) {
    nav("/storage");
  } finally {
    setLoading(false);
  }
};

  useEffect(() => {
    load();
  }, []);

  const remove = async (id) => {
    await api.delete(`/users/${id}/`);
    load();
  };

  const makeAdmin = async (id) => {
    await api.patch(`/users/${id}/make_admin/`);
    load();
  };

  const removeAdmin = async (id) => {
    await api.patch(`/users/${id}/remove_admin/`);
    load();
  };

  return (
    <div className="container">
      <h2>👑 Users</h2>

      {users.map(u => (
        <div key={u.id} style={{
          border: "1px solid #ddd",
          padding: 10,
          marginTop: 10,
          borderRadius: 8
        }}>
          <b>{u.username}</b> ({u.email})
          <div>Admin: {u.is_admin ? "Yes" : "No"}</div>

          <button onClick={() => remove(u.id)}>Delete</button>

          {u.is_admin ? (
            <button onClick={() => removeAdmin(u.id)}>
              Remove admin
            </button>
          ) : (
            <button onClick={() => makeAdmin(u.id)}>
              Make admin
            </button>
          )}
        </div>
      ))}
    </div>
  );
}