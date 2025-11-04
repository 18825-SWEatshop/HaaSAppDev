import { jsx, jsxs } from "react/jsx-runtime";
import React, { useState } from "react";
function ProjectCard({ project }) {
  return /* @__PURE__ */ jsx("div", { className: "bg-white border border-gray-300 rounded-lg p-6 mb-4 w-full flex flex-col", children: /* @__PURE__ */ jsxs("div", { className: "flex flex-row items-center justify-between", children: [
    /* @__PURE__ */ jsxs("div", { children: [
      /* @__PURE__ */ jsx("div", { className: "font-bold text-lg text-gray-900", children: project.name }),
      /* @__PURE__ */ jsxs("div", { className: "text-gray-700 text-sm", children: [
        "ID: ",
        project.projectId
      ] }),
      /* @__PURE__ */ jsxs("div", { className: "text-gray-700 text-sm", children: [
        "Description: ",
        project.description
      ] })
    ] }),
    /* @__PURE__ */ jsx(
      "button",
      {
        type: "button",
        className: "bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded",
        onClick: () => window.location.href = `/projects/${project.projectId}`,
        children: "Details"
      }
    )
  ] }) });
}
const __vite_import_meta_env__ = {};
function ProjectsPage() {
  const API = __vite_import_meta_env__?.VITE_API_URL ?? "http://127.0.0.1:8000";
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const dummyProject = {
    projectId: "dummy123",
    name: "Dummy Project",
    description: "This is a dummy project for testing purposes.",
    owner: "testuser",
    authorizedUsers: ["testuser", "alice", "bob"]
  };
  const [projects, setProjects] = useState([dummyProject]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [projectName, setProjectName] = useState("");
  const [projectId, setProjectId] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [authorizedUsers, setAuthorizedUsers] = useState("");
  const [loginProjectId, setLoginProjectId] = useState("");
  React.useEffect(() => {
    async function fetchProjects() {
      if (!token) {
        alert("Please log in first.");
        setLoading(false);
        return;
      }
      try {
        const res = await fetch(`${API}/projects/user-projects`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          }
        });
        const data = await res.json().catch(() => []);
        if (!res.ok) throw new Error(data?.detail || "Failed to fetch projects");
        setProjects(data.projects || []);
      } catch (err) {
        setError(err?.message ?? String(err));
      } finally {
        setLoading(false);
      }
    }
    fetchProjects();
  }, [token, API]);
  async function handleCreateProject() {
    try {
      if (!token) {
        alert("Please log in first.");
        return;
      }
      const body = {
        projectId: projectId.trim(),
        name: projectName.trim(),
        description: projectDescription.trim(),
        authorizedUsers: authorizedUsers.split(",").map((s) => s.trim()).filter(Boolean)
      };
      const res = await fetch(`${API}/projects/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.detail || "Create failed");
      alert(`Project created: ${data.projectId}`);
      setProjectName("");
      setProjectId("");
      setProjectDescription("");
      setAuthorizedUsers("");
      setLoading(true);
      setError(null);
      React.startTransition(() => {
        setProjects((prev) => [...prev, data]);
      });
    } catch (err) {
      alert(err?.message ?? String(err));
    }
  }
  async function handleLoginProject() {
    try {
      if (!token) {
        alert("Please log in first.");
        return;
      }
      const res = await fetch(`${API}/projects/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          projectId: loginProjectId.trim()
        })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.detail || "Login failed");
      localStorage.setItem("projectId", data.projectId);
      alert(`Logged into project: ${data.name}`);
      setLoginProjectId("");
      setLoading(true);
      setError(null);
      React.startTransition(() => {
        setProjects((prev) => {
          if (!prev.some((p) => p.projectId === data.projectId)) {
            return [...prev, data];
          }
          return prev;
        });
      });
    } catch (err) {
      alert(err?.message ?? String(err));
    }
  }
  let projectListContent;
  if (loading) {
    projectListContent = /* @__PURE__ */ jsx("div", { className: "text-gray-700 text-center", children: "Loading projects..." });
  } else if (error) {
    projectListContent = /* @__PURE__ */ jsx("div", { className: "text-red-600 text-center", children: error });
  } else if (projects.length === 0) {
    projectListContent = /* @__PURE__ */ jsx("div", { className: "text-gray-700 text-center", children: "No projects found." });
  } else {
    projectListContent = /* @__PURE__ */ jsx("div", { className: "flex flex-col gap-4", children: projects.map((project) => /* @__PURE__ */ jsx(ProjectCard, { project }, project.projectId)) });
  }
  return /* @__PURE__ */ jsx("div", { className: "min-h-screen flex flex-col items-center justify-center bg-gray-100", children: /* @__PURE__ */ jsxs("div", { className: "flex flex-row gap-8", children: [
    /* @__PURE__ */ jsxs("div", { className: "flex flex-col gap-8 p-8 bg-white border border-black rounded w-[35rem] min-w-[20rem]", children: [
      /* @__PURE__ */ jsx("h2", { className: "text-2xl font-bold text-center mb-2 text-gray-900", children: "Project List" }),
      projectListContent
    ] }),
    /* @__PURE__ */ jsxs("div", { className: "flex flex-col gap-8 p-8 bg-white border border-black rounded w-96", children: [
      /* @__PURE__ */ jsx("h1", { className: "text-2xl font-bold text-center mb-2 text-gray-900", children: "Project Management" }),
      /* @__PURE__ */ jsxs("div", { className: "flex flex-col gap-2", children: [
        /* @__PURE__ */ jsx("label", { htmlFor: "projectName", className: "font-semibold text-gray-900", children: "Create a new project" }),
        /* @__PURE__ */ jsx("input", { id: "projectName", value: projectName, onChange: (e) => setProjectName(e.target.value), className: "border rounded w-full px-2 py-1", placeholder: "Project Name" }),
        /* @__PURE__ */ jsx("input", { id: "projectId", value: projectId, onChange: (e) => setProjectId(e.target.value), className: "border rounded w-full px-2 py-1", placeholder: "Project ID (unique)" }),
        /* @__PURE__ */ jsx("input", { id: "projectDescription", value: projectDescription, onChange: (e) => setProjectDescription(e.target.value), className: "border rounded w-full px-2 py-1", placeholder: "Project Description" }),
        /* @__PURE__ */ jsx("input", { id: "authorizedUsers", value: authorizedUsers, onChange: (e) => setAuthorizedUsers(e.target.value), className: "border rounded w-full px-2 py-1", placeholder: "Authorized Users (comma-separated)" }),
        /* @__PURE__ */ jsx("button", { type: "button", className: "bg-green-600 hover:bg-green-700 text-white font-semibold px-4 py-2 rounded mt-2", onClick: handleCreateProject, disabled: !projectName.trim() || !projectId.trim(), children: "Create Project" })
      ] }),
      /* @__PURE__ */ jsxs("div", { className: "flex flex-col gap-2", children: [
        /* @__PURE__ */ jsx("label", { htmlFor: "loginProjectId", className: "font-semibold text-gray-900", children: "Login to existing project" }),
        /* @__PURE__ */ jsx("input", { id: "loginProjectId", value: loginProjectId, onChange: (e) => setLoginProjectId(e.target.value), className: "border rounded w-full px-2 py-1", placeholder: "Project ID" }),
        /* @__PURE__ */ jsx("button", { type: "button", className: "bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded mt-2", onClick: handleLoginProject, disabled: !loginProjectId.trim(), children: "Login to Project" })
      ] })
    ] })
  ] }) });
}
export {
  ProjectsPage as component
};
