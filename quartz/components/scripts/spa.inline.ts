import micromorph from "micromorph"
import { FullSlug, RelativeURL, getFullSlug, normalizeRelativeURLs } from "../../util/path"
import { fetchCanonical } from "./util"

// adapted from `micromorph`
// https://github.com/natemoo-re/micromorph
const NODE_TYPE_ELEMENT = 1
let announcer = document.createElement("route-announcer")
const isElement = (target: EventTarget | null): target is Element =>
  (target as Node)?.nodeType === NODE_TYPE_ELEMENT
const isLocalUrl = (href: string) => {
  try {
    const url = new URL(href)
    if (window.location.origin === url.origin) {
      return true
    }
  } catch (e) {}
  return false
}

const isSamePage = (url: URL): boolean => {
  const sameOrigin = url.origin === window.location.origin
  const samePath = url.pathname === window.location.pathname
  return sameOrigin && samePath
}

const getOpts = ({ target }: Event): { url: URL; scroll?: boolean } | undefined => {
  if (!isElement(target)) return
  if (target.attributes.getNamedItem("target")?.value === "_blank") return
  const a = target.closest("a")
  if (!a) return
  if ("routerIgnore" in a.dataset) return
  const { href } = a
  if (!isLocalUrl(href)) return
  return { url: new URL(href), scroll: "routerNoscroll" in a.dataset ? false : undefined }
}

function notifyNav(url: FullSlug) {
  const event: CustomEventMap["nav"] = new CustomEvent("nav", { detail: { url } })
  document.dispatchEvent(event)
}

const cleanupFns: Set<(...args: any[]) => void> = new Set()
window.addCleanup = (fn) => cleanupFns.add(fn)

function startLoading() {
  document.querySelector(".navigation-progress")?.remove()
  const loadingBar = document.createElement("div")
  loadingBar.className = "navigation-progress"
  loadingBar.style.width = "0"
  document.body.prepend(loadingBar)

  setTimeout(() => {
    loadingBar.style.width = "80%"
  }, 100)
}

function stopLoading() {
  const loadingBar = document.querySelector(".navigation-progress")
  if (loadingBar) {
    loadingBar.remove()
  }
}

let isNavigating = false
let p: DOMParser
async function _navigate(url: URL, isBack: boolean = false) {
  isNavigating = true
  startLoading()
  p = p || new DOMParser()
  const contents = await fetchCanonical(url)
    .then((res) => {
      const contentType = res.headers.get("content-type")
      if (contentType?.startsWith("text/html")) {
        return res.text()
      } else {
        window.location.assign(url)
      }
    })
    .catch(() => {
      window.location.assign(url)
    })

  if (!contents) return

  // notify about to nav
  const event: CustomEventMap["prenav"] = new CustomEvent("prenav", { detail: {} })
  document.dispatchEvent(event)

  // cleanup old
  cleanupFns.forEach((fn) => fn())
  cleanupFns.clear()

  const html = p.parseFromString(contents, "text/html")
  normalizeRelativeURLs(html, url)

  let title = html.querySelector("title")?.textContent
  if (title) {
    document.title = title
  } else {
    const h1 = document.querySelector("h1")
    title = h1?.innerText ?? h1?.textContent ?? url.pathname
  }
  if (announcer.textContent !== title) {
    announcer.textContent = title
  }
  announcer.dataset.persist = ""
  html.body.appendChild(announcer)

  document.querySelector(".navigation-progress")?.remove()
  micromorph(document.body, html.body)

  // scroll into place and add history
  if (!isBack) {
    if (url.hash) {
      const el = document.getElementById(decodeURIComponent(url.hash.substring(1)))
      el?.scrollIntoView()
    } else {
      window.scrollTo({ top: 0 })
    }
  }

  // now, patch head, re-executing scripts
  const elementsToRemove = document.head.querySelectorAll(":not([data-persist])")
  elementsToRemove.forEach((el) => el.remove())
  const elementsToAdd = html.head.querySelectorAll(":not([data-persist])")
  elementsToAdd.forEach((el) => document.head.appendChild(el))

  // delay setting the url until now
  // at this point everything is loaded so changing the url should resolve to the correct addresses
  if (!isBack) {
    history.pushState({}, "", url)
  }

  notifyNav(getFullSlug(window))
  delete announcer.dataset.persist
}

async function navigate(url: URL, isBack: boolean = false) {
  if (isNavigating) return
  isNavigating = true
  try {
    await _navigate(url, isBack)
  } catch (e) {
    console.error(e)
    window.location.assign(url)
  } finally {
    stopLoading()
    isNavigating = false
  }
}

window.spaNavigate = navigate

function createRouter() {
  if (typeof window !== "undefined") {
    window.addEventListener("click", async (event) => {
      const { url } = getOpts(event) ?? {}
      // dont hijack behaviour, just let browser act normally
      if (!url || event.ctrlKey || event.metaKey) return
      event.preventDefault()

      if (isSamePage(url) && url.hash) {
        const el = document.getElementById(decodeURIComponent(url.hash.substring(1)))
        el?.scrollIntoView()
        history.pushState({}, "", url)
        return
      }

      navigate(url, false)
    })

    window.addEventListener("popstate", (event) => {
      const { url } = getOpts(event) ?? {}
      if (window.location.hash && window.location.pathname === url?.pathname) return
      navigate(new URL(window.location.toString()), true)
      return
    })
  }

  return new (class Router {
    go(pathname: RelativeURL) {
      const url = new URL(pathname, window.location.toString())
      return navigate(url, false)
    }

    back() {
      return window.history.back()
    }

    forward() {
      return window.history.forward()
    }
  })()
}

createRouter()
notifyNav(getFullSlug(window))

if (!customElements.get("route-announcer")) {
  const attrs = {
    "aria-live": "assertive",
    "aria-atomic": "true",
    style:
      "position: absolute; left: 0; top: 0; clip: rect(0 0 0 0); clip-path: inset(50%); overflow: hidden; white-space: nowrap; width: 1px; height: 1px",
  }

  customElements.define(
    "route-announcer",
    class RouteAnnouncer extends HTMLElement {
      constructor() {
        super()
      }
      connectedCallback() {
        for (const [key, value] of Object.entries(attrs)) {
          this.setAttribute(key, value)
        }
      }
    },
  )
}

function initSyncButton() {
  if (document.querySelector(".sync-trigger-btn")) return

  const darkmodeBtn = document.querySelector(".darkmode")
  const readermodeBtn = document.querySelector(".readermode")
  const flexContainer =
    document.querySelector(".left .flex-component") ||
    darkmodeBtn?.closest(".flex-component") ||
    darkmodeBtn?.parentElement?.parentElement ||
    document.querySelector(".toolbar") ||
    document.querySelector("header")

  if (!flexContainer) return

  const wrapper = document.createElement("div")
  wrapper.style.cssText =
    "flex-grow: 0; flex-shrink: 1; flex-basis: auto; order: 0; align-self: center; justify-self: center;"

  const btn = document.createElement("button")
  btn.className = "sync-trigger-btn"
  btn.setAttribute("aria-label", "구글 드라이브 동기화 (Google Drive Sync)")
  btn.setAttribute("title", "구글 드라이브 동기화 (Google Drive Sync - Shift+클릭시 토큰 재설정)")
  btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3L21.5 8M22 12.5a10 10 0 0 1-18.8 4.2L2.5 16"/>
  </svg>`

  const showToast = (message: string, isError = false) => {
    document.querySelectorAll(".sync-toast").forEach((el) => el.remove())
    const toast = document.createElement("div")
    toast.className = `sync-toast ${isError ? "error" : ""}`
    toast.textContent = message
    document.body.appendChild(toast)
    setTimeout(() => toast.remove(), 4500)
  }

  btn.addEventListener("click", async (e) => {
    if (e.shiftKey) {
      if (confirm("저장된 GitHub Personal Access Token (PAT)을 재설정하시겠습니까?")) {
        localStorage.removeItem("QUARTZ_GITHUB_PAT")
        showToast("저장된 토큰이 삭제되었습니다.")
      }
      return
    }

    let token = localStorage.getItem("QUARTZ_GITHUB_PAT")
    if (!token) {
      token = prompt(
        "동기화(배포) 실행에 필요한 GitHub Personal Access Token (PAT)을 입력해주세요:\n(현재 브라우저에만 안전하게 저장됩니다)",
      )
      if (!token) return
      token = token.trim()
      localStorage.setItem("QUARTZ_GITHUB_PAT", token)
    }

    btn.classList.add("syncing")
    showToast("🔄 Google Drive 동기화 및 빌드 요청 중...")

    try {
      const res = await fetch("https://api.github.com/repos/jshoon1106/my-obsidian-blog/dispatches", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/vnd.github+json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ event_type: "sync-blog" }),
      })

      btn.classList.remove("syncing")
      if (res.status === 204 || res.ok) {
        showToast("✅ 동기화 요청 완료! 약 1분 후 페이지를 새로고침하세요.")
      } else {
        const errData = (await res.json().catch(() => ({}))) as { message?: string }
        showToast(
          `❌ 동기화 실패 (${res.status}): ${errData.message || "토큰 권한 확인 필요 (Shift+클릭으로 토큰 재설정)"}`,
          true,
        )
      }
    } catch (err) {
      btn.classList.remove("syncing")
      showToast(`❌ 네트워크 오류: ${err instanceof Error ? err.message : String(err)}`, true)
    }
  })

  wrapper.appendChild(btn)
  flexContainer.appendChild(wrapper)
}

document.addEventListener("nav", initSyncButton)
document.addEventListener("DOMContentLoaded", initSyncButton)
if (document.readyState === "complete" || document.readyState === "interactive") {
  initSyncButton()
}


