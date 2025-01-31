import React, { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";

function GraphPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { graphUrl, kagOutput } = location.state || {};
  const graphContainerRef = useRef(null);

  useEffect(() => {
    if (graphContainerRef.current) {
      // Ensures the image fully fits the container without scrolling
      graphContainerRef.current.style.height = "80vh"; // Auto-scale height
    }
  }, [graphUrl]);

  return (
    <div
      style={{
        textAlign: "center",
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh", // Ensures the page is fully visible
        background: "#fff", // Set the background to white to remove black edges
      }}
    >
      <h1 style={{ marginBottom: "10px", fontSize: "24px" }}>Graph Visualization</h1>

      {graphUrl ? (
        <div
          ref={graphContainerRef}
          style={{
            width: "70%", // Reduce width slightly to fit within page
            height: "auto",
            maxHeight: "70vh", // Ensures it doesn't take too much space
            borderRadius: "10px",
            padding: "10px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            overflow: "hidden", // Prevent scrolling issues
          }}
        >
          <img
            src={`http://127.0.0.1:5000${graphUrl}`}
            alt="Generated Graph"
            style={{
              width: "100%",
              height: "auto",
              objectFit: "contain", // Maintains aspect ratio
              borderRadius: "8px",
              border: "none", // Remove borders
            }}
          />
        </div>
      ) : (
        <p>No graph available. Please go back and generate one.</p>
      )}

      {/* Back to Home button - Always visible below the graph */}
      <button
        onClick={() => navigate("/")}
        style={{
          marginTop: "20px",
          padding: "12px 24px",
          fontSize: "16px",
          background: "cyan",
          color: "#000",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        ⬅ Back to Home
      </button>

      {/* KAG Output Section */}
      {kagOutput && (
        <div
          style={{
            marginTop: "20px",
            padding: "15px",
            width: "70%",
            border: "1px solid #ddd",
            borderRadius: "10px",
            background: "#f9f9f9",
            textAlign: "left",
          }}
        >
          <h2 style={{ fontSize: "18px", marginBottom: "10px" }}>KAG Output (LLaMA Description)</h2>
          <p style={{ fontSize: "14px" }}>{kagOutput}</p>
        </div>
      )}
    </div>
  );
}

export default GraphPage;
