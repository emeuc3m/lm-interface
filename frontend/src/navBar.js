import React from "react";
import { Link } from "react-router-dom";

import './styles/navBar.css'


function NavBar() {
  return (
    <nav
      id="sidebarMenu"
      className="collapse d-lg-block sidebar collapse"
    >
      <div className="logo">
        <Link to="/" style={{color: "#ffffff", fontSize: "2rem"}}>LM Interface</Link>
      </div>
      <div className="list-group list-group-flush mx-3 mt-4">
        <Link to="/translate"className="list-group-item py-2 ripple side-elems"
          aria-current="true">
          Translate
        </Link>
        <Link to="/spelling"className="list-group-item py-2 ripple side-elems"
          aria-current="true">
          Fix spelling
        </Link>
        <Link to="/story"className="list-group-item py-2 ripple side-elems"
          aria-current="true">
          Create a story
        </Link>
      </div>
    </nav>

  )
}


export default NavBar;