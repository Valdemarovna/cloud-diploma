import { useEffect, useState } from "react";
import api from "../api/axios";
import "../index.css";
import { useSelector } from "react-redux";

export default function StoragePage() {
  const { isAuth } = useSelector(s => s.auth);
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");
  const [links, setLinks] = useState({});
  const loadUsers = async () => {
  try {
    const res = await api.get("/users/");
    setUsers(res.data);
  } catch {}
  };

  const [files, setFiles] = useState([]);

  const load = async () => {
    let url = "/files/";

    if (selectedUser) {
      url += `?user_id=${selectedUser}`;
    }

    const res = await api.get(url);
    setFiles(res.data);
  };

  useEffect(() => {
    if (!isAuth) {
      setFiles([]); // очистка
      return;
    };
    load();
    loadUsers(); // для админа
  }, [isAuth, selectedUser]);

  const upload = async (e) => {
    const formData = new FormData();
    formData.append("file", e.target.files[0]);

    await api.post("/upload/", formData);
    load();
  };

  const deleteFile = async (id) => {
    await api.delete(`/files/${id}/`);
    load();
  };

  const renameFile = async (id) => {
    const newName = prompt("New name:");
    if (!newName) return;
    await api.patch(`/files/${id}/rename/`, { name: newName });
    load();
  };

  const updateComment = async (id) => {
    const comment = prompt("Comment:");
    if (comment === null) return;
    await api.patch(`/files/${id}/comment/`, { comment });
    load();
  };

  const getLink = async (id) => {
    const res = await api.get(`/files/${id}/link/`);

    // сохраняем ссылку
    setLinks(prev => ({
      ...prev,
      [id]: res.data.link
    }));

    // копируем (можно оставить)
    navigator.clipboard.writeText(res.data.link);
    alert("Copied!");
  };

  return (
    <div className="container">
      <h2>📁 Your Storage</h2>

      <input type="file" onChange={upload} />

      <select onChange={(e) => setSelectedUser(e.target.value)}>
        <option value="">All users</option>
        {users.map(u => (
          <option key={u.id} value={u.id}>
            {u.username}
          </option>
        ))}
      </select>

      {files.map((f) => (
        <div key={f.id} style={{
          border: "1px solid #ddd",
          borderRadius: 8,
          padding: 10,
          marginTop: 10
        }}>
          <b>{f.name}</b>
          <div>Size: {f.size}</div>
          <div>Owner: {f.owner}</div>
          <div>Comment: {f.comment || "—"}</div>

          <div style={{ marginTop: 10 }}>
            <button onClick={() => deleteFile(f.id)}>Delete</button>
            <button onClick={() => renameFile(f.id)}>Rename</button>
            <button onClick={() => updateComment(f.id)}>Comment</button>
            <button onClick={() => getLink(f.id)}>Copy Link</button>

            <a href={`/download/${f.id}/`}>
              <button>Download</button>
            </a>
          </div>
        </div>
      ))}
    </div>
  );
}