import { useEffect, useState } from "react";
import api from "../api/axios";
import "../index.css";
import { useSelector } from "react-redux";
import { useSearchParams } from "react-router-dom";

export default function StoragePage() {
  const [searchParams] = useSearchParams();
  const { isAuth } = useSelector(s => s.auth);

  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");
  const [files, setFiles] = useState([]);
  const [links, setLinks] = useState({});
  const [next, setNext] = useState(null);
  const [prev, setPrev] = useState(null);
  const [ordering, setOrdering] = useState("");

  // берем user из URL (?user=ID)
  useEffect(() => {
    const userId = searchParams.get("user");
    if (userId) {
      setSelectedUser(userId);
    }
  }, [searchParams]);

  // загрузка пользователей (для админа)
  const loadUsers = async () => {
    try {
      const res = await api.get("/users/");
      setUsers(res.data.results || res.data); // поддержка пагинации
    } catch (e) {
      console.error("Failed to load users", e);
    }
  };

  const load = async (url = null) => {
    try {
      let requestUrl = url || "/files/?page=1";

      if (!url) {
        requestUrl = "/files/?page=1";

        if (selectedUser) {
          requestUrl += `&user_id=${selectedUser}`;
        }

        if (ordering) {
          requestUrl += `&ordering=${ordering}`;
        }
      }

      const res = await api.get(requestUrl);

      setFiles(res.data.results);
      setNext(res.data.next);
      setPrev(res.data.previous);

    } catch (e) {
      console.error("Failed to load files", e);
    }
  };

  useEffect(() => {
    if (!isAuth) {
      setFiles([]);
      return;
    }

    load();
    loadUsers();
  }, [isAuth, selectedUser, ordering]);

  // upload
  const upload = async (e) => {
    if (!e.target.files[0]) return;

    const formData = new FormData();
    formData.append("file", e.target.files[0]);

    try {
      await api.post("/upload/", formData);
      load();
    } catch (e) {
      alert("Upload failed");
    }
  };

  const deleteFile = async (id) => {
    if (!window.confirm("Delete file?")) return;

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

  // получение ссылки
  const getLink = async (id) => {
    try {
      const res = await api.get(`/files/${id}/link/`);

      setLinks(prev => ({
        ...prev,
        [id]: res.data.link
      }));

      // копирование (если доступно)
      if (navigator.clipboard) {
        navigator.clipboard.writeText(res.data.link);
      }

    } catch {
      alert("Failed to get link");
    }
  };

  return (
    <div className="container">
      <h2>📁 Storage</h2>

      {/* upload */}
      <input type="file" onChange={upload} />

      {/* фильтр по пользователю */}
      <select onChange={(e) => setSelectedUser(e.target.value)}>
        <option value="">All users</option>
        {users.map(u => (
          <option key={u.id} value={u.id}>
            {u.username}
          </option>
        ))}
      </select>

      {/* сортировка */}
      <select onChange={(e) => setOrdering(e.target.value)}>
        <option value="">Default</option>
        <option value="original_name">Name ↑</option>
        <option value="-original_name">Name ↓</option>
        <option value="-size">Size ↓</option>
        <option value="-uploaded_at">Newest</option>
      </select>

      {/* список файлов */}
      {files.map((f) => (
        <div key={f.id} className="card">
          <b>{f.name}</b>
          <div>Size: {(f.size / 1024).toFixed(2)} KB</div>
          <div>Owner: {f.owner}</div>
          <div>Comment: {f.comment || "—"}</div>

          <div style={{ marginTop: 10 }}>
            <button onClick={() => deleteFile(f.id)}>Delete</button>
            <button onClick={() => renameFile(f.id)}>Rename</button>
            <button onClick={() => updateComment(f.id)}>Comment</button>
            <button onClick={() => getLink(f.id)}>Get Link</button>

            {/* Универсальная ссылка */}
            <a href={`/download/${f.id}/`}>
              <button>Download</button>
            </a>
          </div>

          {/* ссылка */}
          {links[f.id] && (
            <div style={{ marginTop: 5 }}>
              Link: <a href={links[f.id]} target="_blank" rel="noreferrer">
                {links[f.id]}
              </a>
            </div>
          )}
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