## 개요

옵시디언 노트를 외부 암기 프로그램인 Anki 데스크톱과 연동하여 간격 반복(Spaced Repetition) 플래시카드로 자동 동기화하는 가이드

---

## 1. Anki 데스크톱 설치
1. Anki 공식 사이트([apps.ankiweb.net](https://apps.ankiweb.net/))에서 Windows용 최신 설치 프로그램 다운로드 후 설치
2. Anki 프로그램 실행 후 기본 프로필 구성 완료

---

## 2. 브릿지 애드온(AnkiConnect) 설정
옵시디언과 Anki 프로그램 간의 통신을 중개하는 애드온 설치 과정입니다.

1. Anki 상단 메뉴의 **도구(Tools) > 애드온(Add-ons)** 선택
2. **애드온 다운로드(Get Add-ons...)** 버튼 클릭
3. 코드 입력창에 아래 **AnkiConnect 고유 번호** 입력 후 확인
   * **코드 번호**: `2055492159`
4. 설치 완료 후 **Anki 데스크톱 재시작**
   * *주의*: 옵시디언에서 카드를 스캔 및 전송할 때 Anki 데스크톱 프로그램이 백그라운드에 항상 실행 중이어야 함

---

## 3. 옵시디언 플러그인 설정
1. 옵시디언 **설정 > 커뮤니티 플러그인** 이동
2. **Flashcards** 플러그인 검색 및 설치 후 활성화
3. Flashcards 설정 내 **Card parser** 옵션을 `Spaced Repetition` (질문::답변) 형식으로 지정

---

## 4. 동기화 테스트 및 실행
1. 임의의 마크다운 파일에 `#flashcards` 태그 삽입 후 아래 형식으로 플래시카드 작성
   ```markdown
   옵시디언 임베드 문법은 무엇인가?::![[노트명]]
   ```
2. 명령어 팔레트(`Ctrl + P`) 호출 후 `Flashcards: Easy Flashcards: Scan active file` 실행
3. Anki 데스크톱으로 전환하여 `Default` 또는 `#flashcards` 덱에 카드가 정상 추가되었는지 확인
