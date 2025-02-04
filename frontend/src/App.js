import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./Home";
import GraphPage from "./GraphPage";
import RagResponsePage from "./RagResponsePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/graph" element={<GraphPage />} />
        <Route path="/repo-summary" element={<RagResponsePage />} />
      </Routes>
    </Router>
  );
}

export default App;
