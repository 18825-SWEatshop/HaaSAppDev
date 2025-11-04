import { jsxs, jsx } from "react/jsx-runtime";
import { useRouterState, Link } from "@tanstack/react-router";
function AuthTabs() {
  const { location } = useRouterState();
  const isLogin = location.pathname === "/login";
  const base = "text-3xl font-semibold transition-colors";
  const active = "text-gray-900";
  const inactive = "text-gray-400 hover:text-gray-600";
  return /* @__PURE__ */ jsxs("div", { className: "w-80 mx-auto mb-4 grid grid-cols-[1fr_auto_1fr] items-center text-center", children: [
    /* @__PURE__ */ jsx("div", { className: "text-right pr-2 justify-self-start", children: /* @__PURE__ */ jsx(
      Link,
      {
        to: "/login",
        className: `${base} ${isLogin ? active : inactive}`,
        children: "Login"
      }
    ) }),
    /* @__PURE__ */ jsx("span", { className: "inline-flex items-center justify-center\n                        w-7 h-7 rounded-full border text-[10px] text-gray-500 mx-2", children: "OR" }),
    /* @__PURE__ */ jsx("div", { className: "text-left pl-2 justify-self-end", children: /* @__PURE__ */ jsx(
      Link,
      {
        to: "/register",
        className: `${base} ${!isLogin ? active : inactive}`,
        children: "Register"
      }
    ) })
  ] });
}
export {
  AuthTabs as A
};
