import { useEffect, useState } from "react";
import axios from "axios";

function Storage() {
  const [files, setFiles] = useState([]);
  const [file, setFile] = useState(null);

  const loadFiles = async () => {
    const res = await axios.get("/api/files/", { withCredentials: true });
    setFiles(res.data);
  };

  useEffect(() => {
    loadFiles();
  }, []);

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);

    await axios.post("/api/files/upload/", formData, {
      withCredentials: true,
    });

    loadFiles();
  };

  return (
    <div>
      <h2>Файлы</h2>

      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Загрузить</button>

      <ul>
        {files.map(f => (
          <li key={f.id}>
            {f.name} ({f.size})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Storage;