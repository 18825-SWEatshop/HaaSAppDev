import { jsx, jsxs, Fragment } from "react/jsx-runtime";
import { useState, useEffect } from "react";
import axios from "axios";
import { R as Route } from "./router-H1l_6Jad.js";
import "@tanstack/react-router";
import "@tanstack/react-router-devtools";
const API_URL = process.env.REACT_APP_API_URL;
const HardwareManagement = ({ label, projectId = "P1" }) => {
  const capacity = 100;
  const [availability, setAvailability] = useState(100);
  const [quantity, setQuantity] = useState("");
  const handleQuantityChange = (e) => {
    setQuantity(e.target.value);
  };
  const handleCheckout = async () => {
    const qty = Number(quantity) || 0;
    if (qty > 0 && qty <= availability) {
      try {
        await axios.post(`${API_URL}/checkout_hardware`, {
          projectId,
          qty
        });
        setAvailability(availability - qty);
      } catch (err) {
        console.error(err);
        alert("Checkout failed");
      }
    }
    setQuantity("");
  };
  const handleCheckin = async () => {
    const qty = Number(quantity) || 0;
    if (qty > 0 && availability + qty <= capacity) {
      try {
        await axios.post(`${API_URL}/checkin_hardware`, {
          projectId,
          qty
        });
        setAvailability(availability + qty);
      } catch (err) {
        console.error(err);
        alert("Check-in failed");
      }
    }
    setQuantity("");
  };
  return /* @__PURE__ */ jsx("div", { children: /* @__PURE__ */ jsxs("div", { style: { display: "flex", gap: "12px", alignItems: "center", marginTop: 4, marginBottom: 4 }, children: [
    /* @__PURE__ */ jsxs("div", { style: { minWidth: 160 }, children: [
      label,
      ": ",
      availability,
      "/",
      capacity
    ] }),
    /* @__PURE__ */ jsx("div", { children: /* @__PURE__ */ jsx(
      "input",
      {
        type: "number",
        id: "quantity",
        name: "quantity",
        placeholder: "Enter Quantity",
        min: "0",
        value: quantity,
        onChange: handleQuantityChange,
        style: { width: 100 }
      }
    ) }),
    /* @__PURE__ */ jsx("button", { onClick: handleCheckout, children: "Check-out" }),
    /* @__PURE__ */ jsx("button", { onClick: handleCheckin, children: "Check-in" })
  ] }) });
};
const __vite_import_meta_env__ = {};
function ProjectDetails() {
  const {
    projectId
  } = Route.useParams();
  const navigate = Route.useNavigate();
  const API = __vite_import_meta_env__?.VITE_API_URL ?? "http://127.0.0.1:8000";
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    async function fetchProjectDetails() {
      if (!token) {
        setError("Please log in first.");
        setLoading(false);
        return;
      }
      try {
        const res = await fetch(`${API}/projects/details`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            projectId
          })
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data?.detail || "Failed to fetch project details");
        setProject({
          ...data,
          projectId: data.projectID || data.projectId
        });
      } catch (err) {
        setError(err?.message ?? String(err));
      } finally {
        setLoading(false);
      }
    }
    fetchProjectDetails();
  }, [projectId, token, API]);
  let content;
  if (loading) {
    content = /* @__PURE__ */ jsx("div", { className: "text-gray-700 text-center", children: "Loading project details..." });
  } else if (error) {
    content = /* @__PURE__ */ jsx("div", { className: "text-red-600 text-center", children: error });
  } else if (project) {
    content = /* @__PURE__ */ jsxs(Fragment, { children: [
      /* @__PURE__ */ jsxs("div", { className: "flex flex-col gap-2", children: [
        /* @__PURE__ */ jsx("div", { className: "font-bold text-lg text-gray-900", children: project.name }),
        /* @__PURE__ */ jsxs("div", { className: "text-gray-700 text-sm", children: [
          "ID: ",
          project.projectId
        ] }),
        /* @__PURE__ */ jsxs("div", { className: "text-gray-700 text-sm", children: [
          "Description: ",
          project.description
        ] }),
        /* @__PURE__ */ jsxs("div", { className: "text-gray-700 text-sm", children: [
          "Owner: ",
          project.owner
        ] }),
        /* @__PURE__ */ jsxs("div", { className: "text-gray-700 text-sm", children: [
          "Authorized Users: ",
          project.authorizedUsers?.join(", ")
        ] })
      ] }),
      /* @__PURE__ */ jsxs("div", { className: "mt-6", children: [
        /* @__PURE__ */ jsx("h3", { className: "font-semibold text-gray-900 mb-2", children: "Hardware Management" }),
        /* @__PURE__ */ jsx(HardwareManagement, { label: "HWSet1", projectId: project.projectId }),
        /* @__PURE__ */ jsx(HardwareManagement, { label: "HWSet2", projectId: project.projectId })
      ] }),
      /* @__PURE__ */ jsx("button", { type: "button", className: "bg-gray-600 hover:bg-gray-700 text-white font-semibold px-4 py-2 rounded mt-6", onClick: () => navigate({
        to: "/projects"
      }), children: "Return to Projects" })
    ] });
  } else {
    content = null;
  }
  return /* @__PURE__ */ jsx("div", { className: "min-h-screen flex flex-col items-center justify-center bg-gray-100", children: /* @__PURE__ */ jsxs("div", { className: "flex flex-col gap-8 p-8 bg-white border border-black rounded w-[35rem] min-w-[20rem]", children: [
    /* @__PURE__ */ jsx("h2", { className: "text-2xl font-bold text-center mb-2 text-gray-900", children: "Project Details" }),
    content
  ] }) });
}
export {
  ProjectDetails as component
};
