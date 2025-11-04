import { jsxs, jsx } from "react/jsx-runtime";
import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { A as AuthTabs } from "./authTabs-9YWugUFB.js";
function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  async function handleLogin() {
    try {
      const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username,
          password
        })
      });
      if (!res.ok) throw new Error((await res.json()).detail || "Login failed");
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
  function forgotPassword() {
    alert("User is trying to reset their password");
  }
  return /* @__PURE__ */ jsxs("div", { className: "min-h-screen flex flex-col items-center justify-center bg-gray-100", children: [
    /* @__PURE__ */ jsx(AuthTabs, {}),
    /* @__PURE__ */ jsxs("div", { className: "flex flex-col gap-4 p-6 bg-white border border-black rounded w-80", children: [
      /* @__PURE__ */ jsx("img", { src: "/android-chrome-192x192.png", alt: "App Logo", className: "w-24 h-24 mx-auto rounded-full" }),
      /* @__PURE__ */ jsxs("div", { children: [
        /* @__PURE__ */ jsx("label", { htmlFor: "username", className: "pe-4 text-gray-900 font-semibold", children: "Username" }),
        /* @__PURE__ */ jsx("input", { id: "username", value: username, onChange: (e) => setUsername(e.target.value), className: "border rounded w-full px-2 py-1" })
      ] }),
      /* @__PURE__ */ jsxs("div", { children: [
        /* @__PURE__ */ jsx("label", { htmlFor: "password", className: "pe-4 text-gray-900 font-semibold", children: "Password" }),
        /* @__PURE__ */ jsx("input", { id: "password", type: "password", value: password, onChange: (e) => setPassword(e.target.value), className: "border rounded w-full px-2 py-1" })
      ] }),
      /* @__PURE__ */ jsx("button", { type: "button", className: "bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600", onClick: handleLogin, children: "Login" }),
      /* @__PURE__ */ jsx("button", { type: "button", className: "text-blue-600 underline hover:text-blue-800 bg-transparent border-none p-0 cursor-pointer", onClick: forgotPassword, children: "Forgot your password?" })
    ] })
  ] });
}
export {
  Login as component
};
