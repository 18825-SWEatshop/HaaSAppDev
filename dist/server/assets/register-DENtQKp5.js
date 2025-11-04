import { jsxs, jsx } from "react/jsx-runtime";
import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { A as AuthTabs } from "./authTabs-9YWugUFB.js";
function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const navigate = useNavigate();
  async function handleRegister() {
    try {
      const res = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: name,
          password: pw
        })
      });
      if (!res.ok) throw new Error((await res.json()).detail || "Register failed");
      const {
        token
      } = await res.json();
      localStorage.setItem("token", token);
      navigate({
        to: "/projects"
      });
    } catch (e) {
      alert(e.message);
    }
  }
  return /* @__PURE__ */ jsxs("div", { className: "min-h-screen flex flex-col items-center justify-center bg-gray-100", children: [
    /* @__PURE__ */ jsx(AuthTabs, {}),
    /* @__PURE__ */ jsxs("div", { className: "flex flex-col gap-4 p-6 bg-white border border-black rounded w-80", children: [
      /* @__PURE__ */ jsx("img", { src: "/android-chrome-192x192.png", alt: "App Logo", className: "w-24 h-24 mx-auto rounded-full" }),
      /* @__PURE__ */ jsxs("div", { children: [
        /* @__PURE__ */ jsx("label", { htmlFor: "name", className: "pe-4 text-gray-900 font-semibold", children: "Username" }),
        /* @__PURE__ */ jsx("input", { id: "name", value: name, onChange: (e) => setName(e.target.value), className: "border rounded w-full px-2 py-1" })
      ] }),
      /* @__PURE__ */ jsxs("div", { children: [
        /* @__PURE__ */ jsx("label", { htmlFor: "pw", className: "pe-4 text-gray-900 font-semibold", children: "Password" }),
        /* @__PURE__ */ jsx("input", { id: "pw", type: "password", value: pw, onChange: (e) => setPw(e.target.value), className: "border rounded w-full px-2 py-1" })
      ] }),
      /* @__PURE__ */ jsx("p", { className: "text-sm text-gray-600", children: "Your personal data will be used to support your experience throughout this website, to manage access to your account, and for other purposes described in our privacy policy." }),
      /* @__PURE__ */ jsx("button", { type: "button", className: "bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded", onClick: handleRegister, children: "REGISTER" })
    ] })
  ] });
}
export {
  Register as component
};
