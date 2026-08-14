<u>**현재 폴더 : C:/users/user/git_projects**</u>

> [!note]+ mt
> ghp_YOUR_GITHUB_PERSONAL_ACCESS_TOKEN

---

- 원격 저장소 복제: `git clone (https://github.com/사용자명/저장소명.git)`

---

- 원격 저장소 연결 확인: `git remote -v` 
    1. 원격 저장소 연결
`git remote add origin (https://github.com/사용자명/저장소명.git)`
    2. 주소 재-설정
`git remote set-url origin (https://github.com/사용자명/저장소명.git)`

---

- 원격 저장소에서 불러오기: `git pull` = (`git fetch` + `git merge`)

---

- 로컬 폴더를 원격 저장소에 연결: `git init`

---

- 원격 저장소 버전이 내 저장소 버전보다 빠름
    - 내 작업 임시 저장
`git stash`
    - 내 저장소 + 원격 저장소 (서로 다른 영역의 경우)
`git pull`
