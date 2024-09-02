import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import { Home, Translate, Spelling, Story } from "./Pages"
import Login from "./Pages/Login";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="login" element={<Login />} />
        <Route path="/" element={<Layout />}>
          <Route path="" element={<Home />} />
          <Route path="translate" element={<Translate />} />
          <Route path="spelling" element={<Spelling />} />
          <Route path="story" element={<Story />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}