import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const [file, setFile] = useState(null);
  const [repoOwner, setRepoOwner] = useState("");
  const [repoName, setRepoName] = useState("");
  const [uploadOption, setUploadOption] = useState("repo");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleGenerateGraph = async (graphType) => {
    setLoading(true);

    if (uploadOption === "file" && !file) {
      alert("Please upload a file.");
      setLoading(false);
      return;
    }

    if (uploadOption === "repo" && (!repoOwner || !repoName)) {
      alert("Please enter both repository owner and name.");
      setLoading(false);
      return;
    }

    let requestData;
    let apiEndpoint;

    if (graphType === "component") {
      apiEndpoint = "http://127.0.0.1:5000/upload";
      requestData = new FormData();
      requestData.append("uploadOption", uploadOption);
      if (uploadOption === "file") {
        requestData.append("code_file", file);
      } else {
        requestData.append("repo_owner", repoOwner);
        requestData.append("repo_name", repoName);
      }
    } else if (graphType === "summary") {
      apiEndpoint = "http://127.0.0.1:5000/generate_repo_summary";
      requestData = JSON.stringify({
        repo_owner: repoOwner,
        repo_name: repoName,
      });
    }

    try {
      const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: graphType === "summary" ? { "Content-Type": "application/json" } : undefined,
        body: requestData,
      });

      if (response.ok) {
        const data = await response.json();
        setLoading(false);

        if (graphType === "component") {
          navigate("/graph", { state: { graphUrl: data.visualization } });
        } else {
          navigate("/repo-summary", { state: { fileSummaries: data.file_summaries, pipelineDiagram: data.pipeline_diagram } });
        }
      } else {
        alert("Error processing request.");
        setLoading(false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error during submission");
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Title */}
      <h1 style={styles.title}>Code Visplain</h1>
      <p style={styles.subtitle}>Understand and visualize your AI code structure</p>

      {/* Upload Form */}
      <div style={styles.formContainer}>
        <label htmlFor="uploadOption" style={styles.label}>Select an option:</label>
        <select
          id="uploadOption"
          value={uploadOption}
          onChange={(e) => setUploadOption(e.target.value)}
          style={styles.input}
        >
          <option value="file">Upload File</option>
          <option value="repo">Enter Repo Details</option>
        </select>

        {/* File Upload Section */}
        {uploadOption === "file" && (
          <div style={styles.uploadContainer}>
            <label htmlFor="code_file" style={styles.label}>Upload Code File:</label>
            <input type="file" accept=".py,.txt,.md" onChange={handleFileChange} style={styles.input} />
          </div>
        )}

        {/* Repository Input Fields */}
        {uploadOption === "repo" && (
          <div style={styles.inputContainer}>
            <label htmlFor="repo_owner" style={styles.label}>Repository Owner:</label>
            <input
              type="text"
              placeholder="Enter Repo Owner"
              value={repoOwner}
              onChange={(e) => setRepoOwner(e.target.value)}
              style={styles.input}
            />
            <label htmlFor="repo_name" style={styles.label}>Repository Name:</label>
            <input
              type="text"
              placeholder="Enter Repo Name"
              value={repoName}
              onChange={(e) => setRepoName(e.target.value)}
              style={styles.input}
            />
          </div>
        )}

        {/* Buttons */}
        <button onClick={() => handleGenerateGraph("summary")} style={styles.button}>Generate Summary</button>
      </div>

      {/* Loading Animation */}
      {loading && <p style={styles.loadingText}>Processing request... Please wait</p>}
    </div>
  );
}

/* ✅ Styles Object for Dark Theme */
const styles = {
  container: {
    textAlign: "center",
    padding: "40px",
    backgroundColor: "#121212",  // Dark Background
    color: "white",
    minHeight: "100vh",
  },
  title: {
    fontSize: "3rem",
    fontWeight: "bold",
    marginBottom: "10px",
    color: "#00d4ff", // Cyan Title
  },
  subtitle: {
    fontSize: "1.2rem",
    marginBottom: "30px",
    color: "#bbb",
  },
  formContainer: {
    backgroundColor: "#1e1e1e",
    padding: "30px",
    borderRadius: "12px",
    boxShadow: "0px 4px 10px rgba(255, 255, 255, 0.1)",
    display: "inline-block",
    minWidth: "400px",
  },
  inputContainer: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    marginTop: "20px",
  },
  uploadContainer: {
    marginTop: "20px",
  },
  label: {
    fontSize: "1rem",
    fontWeight: "bold",
    color: "#ddd",
    display: "block",
    marginBottom: "8px",
  },
  input: {
    padding: "10px",
    fontSize: "1rem",
    borderRadius: "5px",
    border: "1px solid #555",
    backgroundColor: "#222",
    color: "white",
    width: "100%",
  },
  button: {
    marginTop: "20px",
    padding: "12px 24px",
    fontSize: "1rem",
    background: "#00d4ff",
    color: "#000",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontWeight: "bold",
    transition: "all 0.3s ease",
  },
  buttonHover: {
    background: "#00a3cc",
  },
  loadingText: {
    marginTop: "20px",
    fontSize: "1.2rem",
    color: "#ffcc00",
  }
};

export default Home;
