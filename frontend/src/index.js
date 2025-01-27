import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import "./index.css";  // Optional: Global styles for the app

// Render the app to the root div in index.html
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);
