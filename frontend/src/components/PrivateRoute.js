import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

function PrivateRoute({ children }) {
  const isAuth = useSelector(state => state.auth.isAuthenticated);

  return isAuth ? children : <Navigate to="/login" />;
}

export default PrivateRoute;