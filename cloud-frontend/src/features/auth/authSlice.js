import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../api/axios";

export const login = createAsyncThunk("auth/login", async (data) => {
  const res = await api.post("/login/", data);
  return res.data;
});

export const register = createAsyncThunk("auth/register", async (data) => {
  const res = await api.post("/register/", data);
  return res.data;
});

const authSlice = createSlice({
  name: "auth",
  initialState: {
    user: null,
    error: null,
    isAuth: false,
  },
  reducers: {
    logout(state) {
      return {
        user: null,
        isAuth: false,
        error: null,
      };
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.fulfilled, (state,action) => {
        state.isAuth = true;
        state.error = null;
        state.user = action.payload;
        state.isAdmin = true;
      })
      .addCase(login.rejected, (state) => {
        state.error = "Login failed";
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;