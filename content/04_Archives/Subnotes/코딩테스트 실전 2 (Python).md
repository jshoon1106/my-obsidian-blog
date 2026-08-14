# Python 코딩테스트 마스터 학습 노트



## 1. 커리큘럼 로드맵 개요

| 단계      | 학습 단계명                   | 핵심 학습 목표                                          |
| :------ | :----------------------- | :------------------------------------------------ |
| **1단계** | 기초 자료구조 & 기본 패턴          | Python 내장 자료구조 mastery, 그래프/트리 표현 및 인접 리스트 템플릿 암기 |
| **2단계** | 1순위 핵심 알고리즘 정복           | 구현/시뮬레이션, 완전탐색, DFS/BFS 활용 3대 핵심 패턴 습득            |
| **3단계** | Python 특화 패턴 변형 & 복잡도 설계 | `dict`/`set` 기반 방문 관리, 재귀 제한 설정, $N$ 기반 시간 복잡도 검증 |
| **4단계** | 2순위 고득점 알고리즘 확장          | DP(메모이제이션), `heapq` 활용 다익스트라 최단 경로 정복             |
| **5단계** | 실전 모의고사 & 30분 룰 풀이 루틴    | 80문제 기출 모의고사, 30분 룰 적용, 변형 문제 풀이 체화               |

---

## 2. 단계별 세부 학습 내용 & 예시 코드

### 1단계: 기초 자료구조 & 기본 패턴

#### 1.1 자료구조 매핑
##### (1) Stack / Grid (Python `list`)
- `append()` 및 `pop()`을 활용하여 $O(1)$ 스택 연산 수행.

```python

# ==========================================

# 1. Stack (스택) - LIFO (Last In, First Out)

# ==========================================

  

stack = []

  

# 데이터 삽입 (Push) - O(1)

stack.append(10)

stack.append(20)

stack.append(30)

  

# 데이터 꺼내기 (Pop) - O(1)

top_item = stack.pop()

  

print("Pop 된 요소:", top_item)

print("현재 스택 상태:", stack)

  

# [실행 결과]

# Pop 된 요소: 30

# 현재 스택 상태: [10, 20]

```

  

##### (2) Queue (`collections.deque`)

- Python 기본 `list`의 `pop(0)`은 $O(N)$이 소요되므로, $O(1)$ 연산을 보장하는 `collections.deque` 필수 사용.

  

```python

# ==========================================

# 2. Queue (큐) - FIFO (First In, First Out)

# ==========================================

from collections import deque

  

queue = deque()

  

# 데이터 삽입 (Enqueue) - O(1)

queue.append("A")

queue.append("B")

queue.append("C")

  

# 데이터 꺼내기 (Dequeue) - O(1)

front_item = queue.popleft()

  

print("Popleft 된 요소:", front_item)

print("현재 큐 상태:", list(queue))

  

# [실행 결과]

# Popleft 된 요소: A

# 현재 큐 상태: ['B', 'C']

```

  

##### (3) Hash Table (`dict` & `set`)

- Key-Value 탐색 및 중복 제거/존재 여부 확인을 $O(1)$ 시간에 수행.

  

```python

# ==========================================

# 3. Hash Table (해시 테이블) - O(1) 탐색

# ==========================================

  

# Dict (해시 맵) 활용

user_scores = {"alice": 95, "bob": 80}

user_scores["charlie"] = 90  # Key-Value 추가: O(1)

  

# Key 존재 여부 조회: O(1)

if "alice" in user_scores:

    print(f"Alice의 점수: {user_scores['alice']}")

  

# Set (해시 집합) 활용

visited_nodes = set()

visited_nodes.add(1)

visited_nodes.add(2)

  

# Element 존재 여부 조회: O(1)

if 2 in visited_nodes:

    print("노드 2는 방문 완료됨")

  

# [실행 결과]

# Alice의 점수: 95

# 노드 2는 방문 완료됨

```

  

#### 1.2 핵심 구현 패턴 (인접 리스트 변환 템플릿)

그래프 문제 입력을 인접 리스트(Adjacency List) 형태로 표현하는 기본 템플릿임.

  

```python

# ==========================================

# 그래프 인접 리스트 (Adjacency List) 템플릿

# ==========================================

  

# N: 노드 개수, M: 간선 개수

n, m = 5, 4

edges = [(1, 2), (1, 3), (2, 4), (3, 5)]

  

# 1-indexed 그래프 초기화 (0번 인덱스는 사용하지 않음)

graph = [[] for _ in range(n + 1)]

  

for u, v in edges:

    # 무방향(양방향) 간선인 경우 양쪽에 추가

    graph[u].append(v)

    graph[v].append(u)

  

# 연결 상태 출력

for node in range(1, n + 1):

    print(f"노드 {node}에 연결된 이웃: {graph[node]}")

  

# [실행 결과]

# 노드 1에 연결된 이웃: [2, 3]

# 노드 2에 연결된 이웃: [1, 4]

# 노드 3에 연결된 이웃: [1, 5]

# 노드 4에 연결된 이웃: [2]

# 노드 5에 연결된 이웃: [3]

```

  

---

  

### 2단계: 1순위 핵심 알고리즘 & 적용 연습

  

#### 2.1 시뮬레이션 & 구현 (2차원 그리드 이동)

2차원 배열 상에서 상하좌우 이동을 다루는 좌표 벡터 활용 패턴임.

  

```python

# ==========================================

# 2차원 그리드 4방향 이동 벡터 템플릿

# ==========================================

  

# 방향 벡터 정의 (상, 하, 좌, 우)

dx = [-1, 1, 0, 0]

dy = [0, 0, -1, 1]

  

# 현재 위치 및 격자 크기

x, y = 2, 2

grid_size = 5

  

print(f"현재 위치: ({x}, {y})")

  

# 4방향 탐색 수행

for i in range(4):

    nx = x + dx[i]

    ny = y + dy[i]

    # 격자 경계 유효성 검사 (Boundary Check)

    if 0 <= nx < grid_size and 0 <= ny < grid_size:

        print(f"방향 {i} 이동 -> 차기 위치: ({nx}, {ny})")

  

# [실행 결과]

# 현재 위치: (2, 2)

# 방향 0 이동 -> 차기 위치: (1, 2)

# 방향 1 이동 -> 차기 위치: (3, 2)

# 방향 2 이동 -> 차기 위치: (2, 1)

# 방향 3 이동 -> 차기 위치: (2, 3)

```

  

#### 2.2 완전 탐색 (Brute Force with `itertools`)

순열, 조합, 중복순열 등을 활용한 경우의 수 탐색 기법임.

  

```python

# ==========================================

# itertools를 활용한 완전 탐색 패턴

# ==========================================

from itertools import permutations, combinations, product

  

data = ['A', 'B', 'C']

  

# 1. 순열 (Permutations) - 순서 고려 O(N!)

perm_list = list(permutations(data, 2))

print("순열 (3개 중 2개 선택):", perm_list)

  

# 2. 조합 (Combinations) - 순서 미고려 O(2^N)

comb_list = list(combinations(data, 2))

print("조합 (3개 중 2개 선택):", comb_list)

  

# 3. 중복순열 (Product)

prod_list = list(product(data, repeat=2))

print("중복순열 (repeat=2):", prod_list)

  

# [실행 결과]

# 순열 (3개 중 2개 선택): [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

# 조합 (3개 중 2개 선택): [('A', 'B'), ('A', 'C'), ('B', 'C')]

# 중복순열 (repeat=2): [('A', 'A'), ('A', 'B'), ('A', 'C'), ...]

```

  

#### 2.3 DFS / BFS 탐색 구현

  

##### (1) DFS (깊이 우선 탐색) - 재귀 기반

```python

# ==========================================

# DFS (재귀 구현) 템플릿

# ==========================================

  

def dfs(graph, v, visited):

    # 현재 노드 방문 처리

    visited[v] = True

    print(v, end=' ')

    # 인접 노드 순회

    for neighbor in graph[v]:

        if not visited[neighbor]:

            dfs(graph, neighbor, visited)

  

# 그래프 및 방문 배열 정의

graph = [[], [2, 3], [1, 4], [1], [2]]

visited = [False] * 5

  

print("DFS 순회 경로:")

dfs(graph, 1, visited)

print()

  

# [실행 결과]

# DFS 순회 경로:

# 1 2 4 3

```

  

##### (2) BFS (너비 우선 탐색) - `deque` 기반

```python

# ==========================================

# BFS (큐 구현) 템플릿

# ==========================================

from collections import deque

  

def bfs(graph, start, visited):

    queue = deque([start])

    visited[start] = True

    while queue:

        v = queue.popleft()

        print(v, end=' ')

        # 인접 노드 탐색

        for neighbor in graph[v]:

            if not visited[neighbor]:

                visited[neighbor] = True

                queue.append(neighbor)

  

graph = [[], [2, 3], [1, 4], [1], [2]]

visited = [False] * 5

  

print("BFS 순회 경로:")

bfs(graph, 1, visited)

print()

  

# [실행 결과]

# BFS 순회 경로:

# 1 2 3 4

```

  

#### 2.4 DFS/BFS 3대 핵심 활용 유형

  

##### (유형 1) 네트워크 / 컴포넌트 개수 세기

```python

# ==========================================

# 활용 유형 1: 연결 요소(Connected Components) 개수 카운팅

# ==========================================

  

def count_components(n, graph):

    visited = [False] * (n + 1)

    component_count = 0

    def dfs(node):

        visited[node] = True

        for next_node in graph[node]:

            if not visited[next_node]:

                dfs(next_node)

  

    for i in range(1, n + 1):

        if not visited[i]:

            dfs(i)

            component_count += 1

    return component_count

  

# 노드 4개: Component 1 (1-2), Component 2 (3-4)

graph = [[], [2], [1], [4], [3]]

print("연결 요소 총 개수:", count_components(4, graph))

  

# [실행 결과]

# 연결 요소 총 개수: 2

```

  

##### (유형 2) 연결된 요소 크기 측정

```python

# ==========================================

# 활용 유형 2: 특정 시작 노드에 연결된 요소 크기 측정

# ==========================================

from collections import deque

  

def get_component_size(graph, start_node, visited):

    queue = deque([start_node])

    visited[start_node] = True

    size = 1

    while queue:

        curr = queue.popleft()

        for next_node in graph[curr]:

            if not visited[next_node]:

                visited[next_node] = True

                queue.append(next_node)

                size += 1

    return size

  

graph = [[], [2, 3], [1], [1], []]

visited = [False] * 5

print("1번 노드와 연결된 영역 크기:", get_component_size(graph, 1, visited))

  

# [실행 결과]

# 1번 노드와 연결된 영역 크기: 3

```

  

##### (유형 3) 두 요소 간 연결 여부 / 최단 거리 (BFS)

```python

# ==========================================

# 활용 유형 3: BFS 기반 최단 거리 계산

# ==========================================

from collections import deque

  

def shortest_path(n, graph, start_node):

    # 거리 테이블 (-1로 미방문 상태 표현)

    distance = [-1] * (n + 1)

    queue = deque([start_node])

    distance[start_node] = 0

    while queue:

        curr = queue.popleft()

        for next_node in graph[curr]:

            if distance[next_node] == -1:  # 첫 방문 시 최단 거리 확정

                distance[next_node] = distance[curr] + 1

                queue.append(next_node)

    return distance

  

graph = [[], [2, 3], [1, 4], [1, 4], [2, 3]]

print("1번 노드로부터 각 노드별 최단 거리:", shortest_path(4, graph, 1))

  

# [실행 결과]

# 1번 노드로부터 각 노드별 최단 거리: [-1, 0, 1, 1, 2]

```

  

---

  

### 3단계: Python 특화 패턴 변형 & 시간 복잡도 설계

  

#### 3.1 Python 특화 고려사항

  

##### (1) 재귀 깊이 제한 해제

DFS 재귀 사용 시 기본 깊이 제한(1,000회) 초과를 방지하기 위해 필수 설정함.

  

```python

import sys

  

# 재귀 깊이 제한을 10^6으로 설정 (기본값 1,000)

sys.setrecursionlimit(10**6)

```

  

##### (2) 자료구조 변형 (`dict` 기반 인접 리스트 & `set` visited)

노드 이름이 문자열이거나 값이 매우 큰 대형 숫자일 경우 활용함.

  

```python

# ==========================================

# 문자열 노드 대응 dict & set 패턴

# ==========================================

from collections import defaultdict

  

# 문자열 키 인접 리스트

graph = defaultdict(list)

edges = [("Seoul", "Busan"), ("Seoul", "Incheon"), ("Busan", "Daegu")]

  

for u, v in edges:

    graph[u].append(v)

    graph[v].append(u)

  

# set 기반 방문 체크

visited = set()

  

def dfs_str(node):

    visited.add(node)

    print(f"방문 노드: {node}")

    for neighbor in graph[node]:

        if neighbor not in visited:

            dfs_str(neighbor)

  

dfs_str("Seoul")

  

# [실행 결과]

# 방문 노드: Seoul

# 방문 노드: Busan

# 방문 노드: Daegu

# 방문 노드: Incheon

```

  

##### (3) 전역 변수 관리 (`global` 및 `.clear()`)

다중 테스트 케이스 실행 시 상태 초기화 패턴임.

  

```python

# ==========================================

# 다중 테스트케이스 상태 초기화 패턴

# ==========================================

  

visited = set()

result_count = 0

  

def solve_testcase(tc_id):

    global result_count

    # 1. 이전 상태 완전 초기화

    visited.clear()

    result_count = 0

    # 2. 로직 수행

    visited.add(1)

    result_count += tc_id * 10

    print(f"Testcase {tc_id} 결과: {result_count}")

  

solve_testcase(1)

solve_testcase(2)

  

# [실행 결과]

# Testcase 1 결과: 10

# Testcase 2 결과: 20

```

  

#### 3.2 입력값 $N$ 기반 시간 복잡도 선택 규칙

  

- Python 1초당 연산 가능 횟수: 약 $2 \times 10^7 \sim 5 \times 10^7$회

  

| 입력 크기 ($N$) | 허용 시간 복잡도 | 추천 알고리즘 / 자료구조 |

| :--- | :--- | :--- |

| $N \le 10 \sim 12$ | $O(N!)$, $O(2^N)$ | 순열, 조합, 완전탐색 (Brute Force) |

| $N \le 500$ | $O(N^3)$ | 플로이드-워셜, 3중 반복문 |

| $N \le 2,000 \sim 5,000$ | $O(N^2)$ | 2중 반복문, 이차원 DP |

| $N \le 100,000 \sim 200,000$ | $O(N \log N)$ | 정렬(`sort()`), 우선순위 큐(`heapq`), 이진 탐색 |

| $N \le 1,000,000 \sim 10,000,000$ | $O(N)$, $O(\log N)$ | 해시(`dict`/`Counter`), 투 포인터, 누적 합 |

  

---

  

### 4단계: 2순위 고득점 알고리즘 확장

  

#### 4.1 동적 계획법 (DP - Dynamic Programming)

  

##### (1) 1D DP 메모이제이션 / 타뷸레이션 (피보나치 예시)

```python

# ==========================================

# 1D DP (Bottom-up Tabulation)

# ==========================================

  

n = 10

dp = [0] * (n + 1)

  

# 초기 기본 상태 정의

dp[1] = 1

  

# 점화식 적용: dp[i] = dp[i-1] + dp[i-2]

for i in range(2, n + 1):

    dp[i] = dp[i - 1] + dp[i - 2]

  

print("피보나치 10번째 값:", dp[10])

  

# [실행 결과]

# 피보나치 10번째 값: 55

```

  

##### (2) 2D DP 테이블 초기화 & 점화식 적용

```python

# ==========================================

# 2D DP 테이블 초기화 및 격자 경로 탐색

# ==========================================

  

rows, cols = 3, 4

dp_2d = [[0] * cols for _ in range(rows)]

  

# 격자 이동 경우의 수 (상단/좌측 경계 초기화)

for r in range(rows):

    for c in range(cols):

        if r == 0 or c == 0:

            dp_2d[r][c] = 1

        else:

            dp_2d[r][c] = dp_2d[r - 1][c] + dp_2d[r][c - 1]

  

print(" (2, 3) 도달 가능 경로 수:", dp_2d[2][3])

  

# [실행 결과]

# (2, 3) 도달 가능 경로 수: 10

```

  

#### 4.2 다익스트라 (Dijkstra) 최단 경로

`heapq` 우선순위 큐를 활용한 단일 출발 최단 경로 알고리즘임.

  

```python

# ==========================================

# 다익스트라 (Dijkstra) 최단 경로 템플릿

# ==========================================

import heapq

  

def dijkstra(start, n, graph):

    INF = float('inf')

    distances = [INF] * (n + 1)

    distances[start] = 0

    # 우선순위 큐 (거리, 노드 번호)

    pq = [(0, start)]

    while pq:

        current_dist, current_node = heapq.heappop(pq)

        # 이미 처리된 더 짧은 경로가 존재하는 경우 스킵

        if current_dist > distances[current_node]:

            continue

        for neighbor, weight in graph[current_node]:

            distance = current_dist + weight

            # 더 짧은 경로 발견 시 최단 거리 갱신

            if distance < distances[neighbor]:

                distances[neighbor] = distance

                heapq.heappush(pq, (distance, neighbor))

    return distances

  

# 그래프 설정 (노드 4개)

n = 4

graph = [[] for _ in range(n + 1)]

graph[1].append((2, 2))

graph[1].append((3, 5))

graph[2].append((3, 1))

graph[2].append((4, 4))

graph[3].append((4, 1))

  

print("1번 노드 출발 최단 거리 배열:", dijkstra(1, n, graph))

  

# [실행 결과]

# 1번 노드 출발 최단 거리 배열: [inf, 0, 2, 3, 4]

```

  

---

  

### 5단계: 실전 훈련 & 문제 풀이 루틴

  

#### 5.1 30분 룰 (30-Minute Rule)

- 문제 독해 및 접근 방법 고민 시간을 **30분**으로 제한.

- 30분 내 핵심 아이디어 미도출 시 즉시 해설/정답 코드 확인.

- 해설의 접근 방식 체화 후 **보지 않고 직접 재구현**.

  

#### 5.2 입출력 속도 최적화 (`sys.stdin.readline`)

대량의 입력을 빠르게 처리하기 위한 패턴임.

  

```python

# ==========================================

# sys.stdin.readline 빠른 입출력 템플릿

# ==========================================

import sys

  

# 빠른 입력 재정의

input = sys.stdin.readline

  

# 1. 한 줄 문자열 입력받기 (개행 문자는 .strip()으로 제거)

# line = input().strip()

  

# 2. 공백 구분 정수 입력

# a, b, c = map(int, input().split())

  

# 3. 2차원 리스트 입력

# n = int(input())

# grid = [list(map(int, input().split())) for _ in range(n)]

```

  

#### 5.3 1문 다변형 훈련

- 문제 해결 후 다른 방식 적용 재풀이:

  - 재귀 DFS $\rightarrow$ 반복문 BFS

  - 배열 `visited` $\rightarrow$ `dict` / `set` 변형

  - 인덱스 탐색 $\rightarrow$ 클래스 / 데이터 클래스 활용

  

---

  

## 3. Python 필수 내장 모듈 요약표 & 활용 코드

  

| 모듈명 | 주요 클래스 / 함수 | 주요 용도 |

| :--- | :--- | :--- |

| `collections` | `deque`, `defaultdict`, `Counter` | BFS 큐 구현, 기본값 딕셔너리(인접 리스트), 빈도수 카운트 |

| `heapq` | `heappush()`, `heappop()`, `heapify()` | 다익스트라 알고리즘, 우선순위 큐 구현 (최소 힙) |

| `itertools` | `permutations`, `combinations`, `product` | 완전탐색(순열, 조합, 중복순열) 경우의 수 생성 |

| `sys` | `stdin.readline`, `setrecursionlimit` | 빠른 입출력 처리, 재귀 깊이 한도 증가 |

  

### 모듈별 예시 코드

  

#### (1) `collections`

```python

# ==========================================

# collections 모듈 활용 예시

# ==========================================

from collections import deque, defaultdict, Counter

  

# 1. deque (양방향 큐)

dq = deque([1, 2, 3])

dq.appendleft(0)

dq.pop()

print("deque 결과:", list(dq))

  

# 2. defaultdict (기본값 제공 딕셔너리)

adj = defaultdict(list)

adj[1].append(2)

print("defaultdict 결과:", dict(adj))

  

# 3. Counter (빈도수 측정)

counts = Counter(["apple", "banana", "apple", "orange", "banana", "apple"])

print("Counter 결과:", counts)

print("가장 흔한 요소 1개:", counts.most_common(1))

  

# [실행 결과]

# deque 결과: [0, 1, 2]

# defaultdict 결과: {1: [2]}

# Counter 결과: Counter({'apple': 3, 'banana': 2, 'orange': 1})

# 가장 흔한 요소 1개: [('apple', 3)]

```

  

#### (2) `heapq`

```python

# ==========================================

# heapq 모듈 활용 예시 (최소 힙)

# ==========================================

import heapq

  

heap = []

heapq.heappush(heap, 5)

heapq.heappush(heap, 1)

heapq.heappush(heap, 3)

  

print("Heap Pop (최소값 추출):", heapq.heappop(heap))

  

# 리스트를 힙 구조로 즉시 변환 (O(N))

arr = [4, 1, 7, 3, 8, 5]

heapq.heapify(arr)

print("Heapify 변환 결과:", arr)

  

# [실행 결과]

# Heap Pop (최소값 추출): 1

# Heapify 변환 결과: [1, 3, 5, 4, 8, 7]

```

  

#### (3) `itertools`

```python

# ==========================================

# itertools 모듈 활용 예시

# ==========================================

from itertools import permutations, combinations, product

  

arr = [1, 2, 3]

  

print("순열:", list(permutations(arr, 2)))

print("조합:", list(combinations(arr, 2)))

print("중복순열:", list(product(arr, repeat=2)))

```

  

#### (4) `sys`

```python

# ==========================================

# sys 모듈 활용 예시

# ==========================================

import sys

  

# 재귀 깊이 제한 확장

sys.setrecursionlimit(10**6)

  

# 빠른 입력 설정

input = sys.stdin.readline

```

  
**