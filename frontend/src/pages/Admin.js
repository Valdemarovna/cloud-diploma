import { useEffect, useState } from "react";
import axios from "axios";

function Admin() {
  const [users, setUsers] = useState([]);

  const loadUsers = async () => {
    const res = await axios.get("/api/users/", {
      withCredentials: true,
    });
    setUsers(res.data);
  };

  useEffect(() => {
    loadUsers();
  }, []);

  return (
    <div>
      <h2>Пользователи</h2>

      <ul>
        {users.map(u => (
          <li key={u.id}>
            {u.username} ({u.email})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Admin;