import axios from "axios";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie) {
    const cookies = document.cookie.split(";");
    for (let c of cookies) {
      c = c.trim();
      if (c.startsWith(name + "=")) {
        cookieValue = c.substring(name.length + 1);
      }
    }
  }
  return cookieValue;
}

const api = axios.create({
  baseURL: "",
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const csrfToken = getCookie("csrftoken");
  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }
  return config;
});

export default api;