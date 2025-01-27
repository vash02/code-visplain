import React, { useState, useEffect, useRef } from "react";
import Panzoom from "@panzoom/panzoom";

function App() {
  const [file, setFile] = useState(null);
  const [repoOwner, setRepoOwner] = useState("");
  const [repoName, setRepoName] = useState("");
  const [graphUrl, setGraphUrl] = useState(null);
  const [uploadOption, setUploadOption] = useState("repo");
  const panzoomContainerRef = useRef(null); // Reference for panzoom container

  // Handle file change
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Ensure both file or repo inputs are validated before submission
    if (uploadOption === "file" && !file) {
      alert("Please upload a file.");
      return;
    }

    if (uploadOption === "repo" && (!repoOwner || !repoName)) {
      alert("Please enter both repository owner and name.");
      return;
    }

    const formData = new FormData();

    // Append the upload option to the FormData
    formData.append("uploadOption", uploadOption);  // Append the uploadOption

    // Append file or repo details to FormData
    if (uploadOption === "file") {
      formData.append("code_file", file);
    } else {
      formData.append("repo_owner", repoOwner);
      formData.append("repo_name", repoName);
    }

    // Debugging: Log the FormData content
    console.log("FormData being sent:");
    formData.forEach((value, key) => console.log(key, value));

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      // Handle response from backend
      if (response.ok) {
        const data = await response.json();
        if (data.visualization) {
          // The backend returns the relative URL; prepend the Flask base URL
          setGraphUrl('http://127.0.0.1:5000' + data.visualization);
        }
      } else {
        alert("Error generating graph");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error during submission");
    }
  };

  // Initialize Panzoom when the graph URL is updated
  useEffect(() => {
    if (graphUrl && panzoomContainerRef.current) {
      const panzoomInstance = Panzoom(panzoomContainerRef.current, {
        maxScale: 5,
        minScale: 1,
        contain: "outside",
      });

      // Clean up Panzoom instance on component unmount
      return () => panzoomInstance.dispose();
    }
  }, [graphUrl]); // Only run when graphUrl is updated

  return (
    <div className="App" style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh" }}>
      <h1>Upload Code File or Enter Repository Details</h1>

      <form onSubmit={handleSubmit} style={{ textAlign: "center" }}>
        <label htmlFor="uploadOption">Select an option:</label>
        <select
          id="uploadOption"
          value={uploadOption}
          onChange={(e) => setUploadOption(e.target.value)}
          style={{ marginTop: "10px" }}
        >
          <option value="file">Upload File</option>
          <option value="repo">Enter Repo Details</option>
        </select>

        {/* File Upload Section */}
        {uploadOption === "file" && (
          <div id="fileUpload" style={{ marginTop: "20px" }}>
            <label htmlFor="code_file">Upload Code File:</label>
            <input
              type="file"
              accept=".py,.txt,.md"
              onChange={handleFileChange}
            />
          </div>
        )}

        {/* Repository Details Section */}
        {uploadOption === "repo" && (
          <div id="repoDetails" style={{ marginTop: "20px" }}>
            <label htmlFor="repo_owner">Repository Owner:</label>
            <input
              type="text"
              id="repo_owner"
              placeholder="Enter Repo Owner"
              value={repoOwner}
              onChange={(e) => setRepoOwner(e.target.value)}
            />
            <br />
            <label htmlFor="repo_name">Repository Name:</label>
            <input
              type="text"
              id="repo_name"
              placeholder="Enter Repo Name"
              value={repoName}
              onChange={(e) => setRepoName(e.target.value)}
            />
          </div>
        )}

        <button type="submit" style={{ marginTop: "20px" }}>
          Submit
        </button>
      </form>

      {/* Display Graph Image after generation */}
      {graphUrl && (
        <div
          id="graph-container"
          ref={panzoomContainerRef} // Assign the ref to the container
          style={{ marginTop: "30px", width: "80%", position: "relative" }}
        >
          <h2>Generated Graph</h2>
          <img
            src={graphUrl}
            alt="Generated Graph"
            className="graph-image"
            style={{
              width: "100%",
              maxWidth: "800px", // Ensure it's not too big
              margin: "0 auto", // Center the image
              border: "1px solid #ddd",
            }}
          />
          <button
            onClick={() => setGraphUrl(null)}
            id="close-button"
            style={{
              position: "absolute",
              top: "10px",
              right: "10px",
              fontSize: "20px",
              cursor: "pointer",
              background: "red",
              color: "white",
              border: "none",
              borderRadius: "50%",
            }}
          >
            ✖ Close
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
