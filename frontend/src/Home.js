import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const [file, setFile] = useState(null);
  const [repoOwner, setRepoOwner] = useState("");
  const [repoName, setRepoName] = useState("");
  const [uploadOption, setUploadOption] = useState("repo");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const navigate = useNavigate();

  // Simulate progress bar
  useEffect(() => {
    let interval;
    if (loading) {
      setProgress(0); // Reset progress
      interval = setInterval(() => {
        setProgress((prev) => (prev < 95 ? prev + 5 : prev)); // Max 95% until response
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [loading]);

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
        setProgress(100); // Complete progress bar

        if (graphType === "component") {
          navigate("/graph", { state: { graphUrl: data.visualization } });
        } else {
          navigate("/repo-summary", { state: { fileSummaries: data.file_summaries, pipelineDiagram: data.pipeline_diagram } });
        }
      } else {
        alert("Error processing request.");
        setLoading(false);
        setProgress(0);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error during submission");
      setLoading(false);
      setProgress(0);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "30px" }}>
      <h1>Upload Code File or Enter Repository Details</h1>

      <form style={{ marginBottom: "20px" }}>
        <label htmlFor="uploadOption">Select an option:</label>
        <select
          id="uploadOption"
          value={uploadOption}
          onChange={(e) => setUploadOption(e.target.value)}
          style={{ marginLeft: "10px", padding: "5px" }}
        >
          <option value="file">Upload File</option>
          <option value="repo">Enter Repo Details</option>
        </select>

        {uploadOption === "file" && (
          <div style={{ marginTop: "20px" }}>
            <label htmlFor="code_file">Upload Code File:</label>
            <input type="file" accept=".py,.txt,.md" onChange={handleFileChange} />
          </div>
        )}

        {uploadOption === "repo" && (
          <div style={{ marginTop: "20px" }}>
            <label htmlFor="repo_owner">Repository Owner:</label>
            <input
              type="text"
              placeholder="Enter Repo Owner"
              value={repoOwner}
              onChange={(e) => setRepoOwner(e.target.value)}
              style={{ marginLeft: "10px", padding: "5px" }}
            />
            <br />
            <label htmlFor="repo_name">Repository Name:</label>
            <input
              type="text"
              placeholder="Enter Repo Name"
              value={repoName}
              onChange={(e) => setRepoName(e.target.value)}
              style={{ marginLeft: "10px", padding: "5px" }}
            />
          </div>
        )}
      </form>

      {/* ✅ Buttons for Graph and Summary Generation */}
      {/*<button onClick={() => handleGenerateGraph("component")} style={buttonStyle}>Generate Component Graph</button>*/}
      <button onClick={() => handleGenerateGraph("summary")} style={{ ...buttonStyle, background: "lightblue" }}>Generate Summary</button>

      {/* ✅ Progress Bar */}
      {loading && (
        <div style={{ width: "100%", backgroundColor: "#ddd", height: "10px", marginTop: "20px", position: "relative" }}>
          <div style={{
            width: `${progress}%`,
            height: "100%",
            backgroundColor: "lightblue",
            transition: "width 1s ease-in-out",
          }}></div>
        </div>
      )}
    </div>
  );
}

// ✅ Styles
const buttonStyle = {
  margin: "10px",
  padding: "10px 20px",
  background: "grey",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer",
};

export default Home;
