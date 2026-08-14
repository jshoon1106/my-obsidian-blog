## 역할
+ 통합 대시보드 (Index & Master MOC)

## 디렉토리 구조 및 지식망 (MOC)
전체 Vault의 물리적 폴더 구조를 명세하고, 모든 지식을 통합적으로 연결하는 최상위 지식망(Wiki) 허브

### **01_Projects** (단기 프로젝트 및 학업)

```dataview
LIST FROM "01_Projects"
WHERE file.folder = "01_Projects"
```
---
### **02_Areas** (주제별 영역 - 요약/정제된 지식 허브)

```dataview
LIST FROM "02_Areas"
WHERE file.folder = "02_Areas"
```
---
### **03_Resources** (독서 아카이브, 템플릿 등 외부 참고 자료 DB)

```dataview
LIST FROM "03_Resources"
WHERE file.folder = "03_Resources"
```
---
### **04_Archives** (가공되지 않은 원본 노트 / Raw Data)

```dataview
LIST FROM "04_Archives"
WHERE file.folder = "04_Archives"
```
  > [!summary]+ *04_Archives/subnotes*
>```dataview
>TABLE rows.file.link as Subnotes
>FROM "04_Archives/Subnotes"
>FLATTEN choice(length(file.inlinks) > 0, file.inlinks, list("참조 없음")) AS incoming
>GROUP BY incoming AS "분류"
>FLATTEN choice(key = "참조 없음", 3, choice(startswith(key.file.path,"04_Archives/Subnotes"), 2, 1)) AS sort_order
>SORT sort_order ASC, key ASC
>```

---
- **운영 규칙**: [[AGENTS]]
- **작업 이력**: [[log]]