import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm"; // ✅ Fix: Ensure package is installed
import "github-markdown-css"; // ✅ Fix: Ensure package is installed

function RagResponsePage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { fileSummaries = {}, pipelineDiagram = "" } = location.state || {};

  return (
    <div style={pageStyle}>
      <h1 style={headerStyle}>📂 Repository Summary</h1>

      {/* ✅ Block Diagram */}
      {pipelineDiagram ? (
          <div style={diagramContainerStyle}>
              <h2 style={subHeaderStyle}>📊 Block Diagram</h2>
              <img
                  src={`http://127.0.0.1:5000${pipelineDiagram}`} // Ensure full path
                  alt="Block Diagram"
                  onError={(e) => {
                      console.error("Error loading block diagram:", e.target.src);
                      e.target.style.display = "none"; // Hide image if not found
                  }}
                  style={{
                      width: "100%",
                      maxWidth: "800px",
                      border: "2px solid black",
                      display: "block",
                      margin: "auto",
                  }}
              />
          </div>
      ) : (
          <p>No block diagram available.</p>
      )}

        {/* ✅ File Summaries */}
        {Object.keys(fileSummaries).length > 0 ? (
            <div style={summaryContainerStyle}>
                <h2 style={subHeaderStyle}>📜 File Summaries</h2>
                {Object.entries(fileSummaries).map(([file, content], index) => (
                    <div key={index} style={summaryStyle}>
                    <h3 style={{ color: "#007bff" }}>📌 {file}</h3>
              <ReactMarkdown className="markdown-body" remarkPlugins={[remarkGfm]}>
                {content}
              </ReactMarkdown>
            </div>
          ))}
        </div>
      ) : (
        <p>No summaries available.</p>
      )}

      <button onClick={() => navigate("/")} style={buttonStyle}>⬅ Back to Home</button>
    </div>
  );
}

/* ✅ Define missing styles */
const pageStyle = { textAlign: "center", padding: "20px", overflowY: "auto", maxHeight: "100vh" };
const headerStyle = { fontSize: "28px", marginBottom: "20px" };
const subHeaderStyle = { fontSize: "22px", marginBottom: "10px", fontWeight: "bold" };
const diagramContainerStyle = { marginBottom: "30px" };
const summaryContainerStyle = { textAlign: "left", maxWidth: "900px", margin: "auto", marginTop: "20px" };
const summaryStyle = { padding: "10px", border: "1px solid #ddd", borderRadius: "8px", background: "#f9f9f9", marginBottom: "15px" };
const buttonStyle = { marginTop: "20px", padding: "10px 20px", background: "cyan", border: "none", borderRadius: "8px", cursor: "pointer" };

export default RagResponsePage;
