import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const [file, setFile] = useState(null);
  const [repoOwner, setRepoOwner] = useState("");
  const [repoName, setRepoName] = useState("");
  const [uploadOption, setUploadOption] = useState("repo"); // Default to "repo"
  const [loading, setLoading] = useState(false); // Loading state
  const navigate = useNavigate(); // Navigation hook

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Show loading bar

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

    const formData = new FormData();
    formData.append("uploadOption", uploadOption);
    if (uploadOption === "file") {
      formData.append("code_file", file);
    } else {
      formData.append("repo_owner", repoOwner);
      formData.append("repo_name", repoName);
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setLoading(false);
        navigate("/graph", { state: { graphUrl: data.visualization, kagOutput: data.kag_output } });
      } else {
        alert("Error generating graph");
        setLoading(false);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error during submission");
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Upload Code File or Enter Repository Details</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <label htmlFor="uploadOption">Select an option:</label>
        <select id="uploadOption" value={uploadOption} onChange={(e) => setUploadOption(e.target.value)}>
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
            <input type="text" placeholder="Enter Repo Owner" value={repoOwner} onChange={(e) => setRepoOwner(e.target.value)} />
            <br />
            <label htmlFor="repo_name">Repository Name:</label>
            <input type="text" placeholder="Enter Repo Name" value={repoName} onChange={(e) => setRepoName(e.target.value)} />
          </div>
        )}

        <button type="submit" style={{ marginTop: "20px" }}>Submit</button>
      </form>

      {loading && (
        <div style={{ width: "100%", backgroundColor: "#ddd", height: "5px", position: "relative" }}>
          <div style={{
            width: "100%",
            height: "5px",
            backgroundColor: "#00FFFF",
            position: "absolute",
            animation: "loadingAnimation 2s infinite",
          }}></div>
        </div>
      )}

      <style>
        {`
          @keyframes loadingAnimation {
            0% { width: 0%; }
            100% { width: 100%; }
          }
        `}
      </style>
    </div>
  );
}

export default Home;
