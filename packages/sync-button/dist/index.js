function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

var syncInlineScript = `
var s = () => {
  let setup = () => {
    for (let btn of document.getElementsByClassName("sync-trigger-btn")) {
      if (btn.dataset.bound) continue;
      btn.dataset.bound = "true";

      const showToast = (message, isError = false) => {
        document.querySelectorAll(".sync-toast").forEach((el) => el.remove());
        const toast = document.createElement("div");
        toast.className = "sync-toast " + (isError ? "error" : "");
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 4500);
      };

      btn.addEventListener("click", async (e) => {
        if (e.shiftKey) {
          if (confirm("저장된 GitHub Personal Access Token (PAT)을 재설정하시겠습니까?")) {
            localStorage.removeItem("QUARTZ_GITHUB_PAT");
            showToast("저장된 토큰이 삭제되었습니다.");
          }
          return;
        }

        let token = localStorage.getItem("QUARTZ_GITHUB_PAT");
        if (!token) {
          token = prompt(
            "동기화(배포) 실행에 필요한 GitHub Personal Access Token (PAT)을 입력해주세요:\\n(현재 브라우저에만 안전하게 저장됩니다)"
          );
          if (!token) return;
          token = token.trim();
          localStorage.setItem("QUARTZ_GITHUB_PAT", token);
        }

        btn.classList.add("syncing");
        showToast("🔄 Google Drive 동기화 및 빌드 요청 중...");

        try {
          const res = await fetch("https://api.github.com/repos/jshoon1106/my-obsidian-blog/dispatches", {
            method: "POST",
            headers: {
              Authorization: "Bearer " + token,
              Accept: "application/vnd.github+json",
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ event_type: "sync-blog" }),
          });

          btn.classList.remove("syncing");
          if (res.status === 204 || res.ok) {
            showToast("✅ 동기화 요청 완료! 약 1분 후 페이지를 새로고침하세요.");
          } else {
            const errData = await res.json().catch(() => ({}));
            showToast(
              "❌ 동기화 실패 (" + res.status + "): " + (errData.message || "토큰 권한 확인 필요 (Shift+클릭으로 토큰 재설정)"),
              true
            );
          }
        } catch (err) {
          btn.classList.remove("syncing");
          showToast("❌ 네트워크 오류: " + (err instanceof Error ? err.message : String(err)), true);
        }
      });
    }
  };
  setup();
};
document.addEventListener("nav", s);
document.addEventListener("render", s);
document.addEventListener("DOMContentLoaded", s);
`;

var syncStyles = `
.sync-trigger-btn {
  cursor: pointer;
  padding: 0;
  position: relative;
  background: none;
  border: none;
  width: 20px;
  height: 32px;
  margin: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--darkgray);
  transition: color 0.15s ease, transform 0.15s ease;
}
.sync-trigger-btn:hover {
  color: var(--secondary);
  transform: scale(1.1);
}
.sync-trigger-btn svg {
  width: 18px;
  height: 18px;
  fill: currentColor;
}
.sync-trigger-btn.syncing svg {
  animation: sync-spin 1s linear infinite;
}
@keyframes sync-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.sync-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: var(--light);
  color: var(--dark);
  border: 1px solid var(--lightgray);
  border-radius: 8px;
  padding: 12px 18px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
  font-size: 0.9rem;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: toast-in 0.25s ease-out;
  max-width: 360px;
}
.sync-toast.error {
  border-color: #ef4444;
  color: #b91c1c;
}
@keyframes toast-in {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
`;

var f2 = 0;
function u2(e2, t2, n2, o2, i2, u3) {
  t2 || (t2 = {});
  var a2, c2, p2 = t2;
  if ("ref" in p2) for (c2 in p2 = {}, t2) "ref" == c2 ? a2 = t2[c2] : p2[c2] = t2[c2];
  var l2 = { type: e2, props: p2, key: n2, ref: a2, __k: null, __: null, __b: 0, __e: null, __c: null, constructor: void 0, __v: --f2, __i: -1, __u: 0, __source: i2, __self: u3 };
  if ("function" == typeof e2 && (a2 = e2.defaultProps)) for (c2 in a2) void 0 === p2[c2] && (p2[c2] = a2[c2]);
  return l2;
}

var SyncButton = ({ displayClass }) => {
  return u2("button", {
    class: classNames(displayClass, "sync-trigger-btn"),
    "aria-label": "구글 드라이브 동기화",
    title: "구글 드라이브 동기화 (Shift+클릭시 토큰 재설정)",
    children: u2("svg", {
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      "stroke-width": "2",
      "stroke-linecap": "round",
      "stroke-linejoin": "round",
      children: [
        u2("path", { d: "M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3L21.5 8M22 12.5a10 10 0 0 1-18.8 4.2L2.5 16" })
      ]
    })
  });
};

SyncButton.beforeDOMLoaded = syncInlineScript;
SyncButton.css = syncStyles;
var SyncButton_default = (() => SyncButton);

export { SyncButton_default as SyncButton, SyncButton_default as default };
