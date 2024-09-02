import React from "react";
import {Outlet} from "react-router-dom";
import NavBar from "./navBar";
import "./App.css"

const Layout = () => {
  return (
    <div style={{ display: "flex" }}>
      <NavBar />
      <div className="content">
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;