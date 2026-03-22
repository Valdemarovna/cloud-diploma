import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./authSlice";
import axios from "axios";

axios.defaults.withCredentials = true;
export const store = configureStore({
  reducer: {
    auth: authReducer,
  },
});