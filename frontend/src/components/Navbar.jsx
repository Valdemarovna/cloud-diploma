import { Link } from "react-router-dom";

export default function Navbar({ isAuth }) {
  return (
    <nav>
      {isAuth ? (
        <>
          <Link to="/storage">Storage</Link>
          <button>Logout</button>
        </>
      ) : (
        <>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </nav>
  );
}