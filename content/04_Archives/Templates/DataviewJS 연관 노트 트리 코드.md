### 계층적 연관 노트 트리

```dataviewjs
// 현재 노트(dv.current)를 최상위 루트로 설정
const rootPage = dv.current(); 
const visited = new Set();
const maxDepth = 3; // 최대 탐색 깊이 (3단계까지)

function generateTree(page, depth = 0) {
    if (!page || visited.has(page.file.path) || depth > maxDepth) return "";
    visited.add(page.file.path);

    const indent = "  ".repeat(depth);
    let result = `${indent}- ${page.file.link}\n`;

    // outlinks(현재 노트에 링크된 다른 위키링크들)를 탐색
    if (page.file.outlinks && page.file.outlinks.length > 0) {
        for (let link of page.file.outlinks) {
            // 시스템 가이드 및 공통 설정 노트는 트리 탐색에서 제외
            if (link.path.endsWith("AGENTS.md") || link.path.endsWith("log.md") || link.path.endsWith("index.md")) continue;

            const childPage = dv.page(link.path);
            if (childPage) {
                result += generateTree(childPage, depth + 1);
            }
        }
    }
    return result;
}

dv.paragraph(generateTree(rootPage));
```
