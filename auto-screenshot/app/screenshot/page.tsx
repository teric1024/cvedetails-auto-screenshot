'use client'
import { useState, useEffect } from "react";
import { FileInput, Label, Button, Spinner } from "flowbite-react";

export default function Screenshot() {
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [taskId, setTaskId] = useState(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      console.log("Uploading file to backend. " + process.env.BACKEND_DOMAIN_FROM_CLIENT);
      const response = await fetch(process.env.BACKEND_DOMAIN_FROM_CLIENT + "/screenshot", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const { task_id } = await response.json();
        console.log("Upload successful, task ID received: ", task_id);
        setTaskId(task_id);
      } else {
        console.error("Upload failed");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  useEffect(() => {
    const fetchZipFile = async () => {
      if (taskId) {
        try {
          console.log("Fetching ZIP file...");
          const zipResponse = await fetch(process.env.BACKEND_DOMAIN_FROM_CLIENT + `/download/${taskId}`, {
            method: "GET",
          });

          if (zipResponse.ok) {
            const contentType = zipResponse.headers.get("content-type");
            if (contentType && contentType.includes("application/zip")) {
              const blob = await zipResponse.blob();
              const url = window.URL.createObjectURL(blob);
              setDownloadUrl(url);
              console.log("ZIP file received and ready for download");

              // 自動下載 zip
              const link = document.createElement("a");
              link.href = url;
              link.download = `${process.env.NEXT_PUBLIC_ZIP_FILENAME}`;
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);

              clearInterval(interval);
            } else {
              console.error("Unexpected response content type");
            }
          } else {
            console.error("Failed to fetch ZIP file, retrying in 10 seconds...");
          }
        } catch (error) {
          console.error("Error fetching ZIP file:", error);
        }
      }
    };

    const interval = setInterval(() => {
      fetchZipFile();
    }, 10000);

    return () => clearInterval(interval);
  }, [taskId]);

  const handleFileChange = async (e) => {
    setTaskId(null);
    setDownloadUrl(null);
    setFile(e.target.files[0]);
  };

  return (
    <div>
      <p>Please upload a .txt file containing a list of packages (separate by new line).</p>
      <p>This server will screenshot the packages and download them as a zip file.</p>
      <form onSubmit={handleSubmit}>
        <div >
          <div className="mb-2 block">
            <Label htmlFor="file-upload" value="Upload file" />
          </div>
          <FileInput id="file-upload" onChange={handleFileChange} accept=".txt" />
        </div>
        <Button type="submit" className="mt-4">Upload</Button>
        {downloadUrl && (
          <div className="mt-4">
            <a href={downloadUrl} download={process.env.NEXT_PUBLIC_ZIP_FILENAME} className="text-blue-600 hover:underline">
              Download {process.env.NEXT_PUBLIC_ZIP_FILENAME}
            </a>
          </div>
        )}
        {(taskId && !downloadUrl) && (
          <div><Spinner aria-label="Default status example" />Taking screenshot... Please wait for a few seconds.</div>
        )}
      </form>
    </div>
  );
}
