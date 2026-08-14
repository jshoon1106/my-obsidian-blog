### 1. 개요 및 학습 목표

#### 1.1 정의
- **개념**: 파이썬(Python 3) 표준 라이브러리와 유연한 자료구조를 활용하여 주어진 문제의 요구 조건에 맞는 알고리즘을 제한 시간 및 메모리 내에 구현하는 문제 해결 과정.
- **의의**: 기업 및 기관의 코딩테스트에서 파이썬은 풍부한 내장 함수와 간결한 문법 덕분에 개발 속도가 빠르고 코드 양이 적어 정해진 시간 내 문제를 정확히 풀이하기에 최적화됨.
- **실제 예시 및 원리**:
  - 시간 복잡도 기준: 파이썬은 1초당 약 $10^7 \sim 10^8$ 회 연산을 기준으로 판단.
  - $N \le 100,000$ 인 경우 $O(N \log N)$ 이하 알고리즘 설계 필요.

---

### 2. 입출력 및 기초 유틸리티

#### 2.1 빠른 입출력 (sys.stdin.readline)
- **정의**: 표준 입력(`input()`) 대신 파이썬 `sys` 모듈의 `stdin.readline()`을 사용하는 최적화 기법.
- **의의**: `input()` 함수는 반복 호출 시 개별 버퍼링 및 개행 문자 처리 비용으로 인해 입력 데이터가 클 때 시간 초과(TLE) 발생 원인이 됨.
- **실제 예시 및 원리**:
```python
import sys
input = sys.stdin.readline

# 1줄 문자열 입력 (개행 문자 제거)
data = input().rstrip()

# 1줄에 공백으로 구분된 여러 정수 입력
a, b, c = map(int, input().split())

# N줄의 정수 입력 받아 리스트 저장
n = int(input())
arr = [int(input()) for _ in range(n)]
```

#### 2.2 리스트 컴프리헨션 및 내장 유틸리티
- **정의**: 한 줄의 간결한 구문으로 리스트를 생성 및 가공하는 파이썬 고유 문법.
- **의의**: 반복문 속도를 향상시키고 2차원 격자/그래프 초기화 시 유용한 패턴 제공.
- **실제 예시 및 원리**:
```python
# 2차원 N x M 배열 0으로 초기화 (올바른 방법)
grid = [[0] * M for _ in range(N)]

# 짝수만 제곱하여 리스트 생성
evens_squared = [x**2 for x in range(10) if x % 2 == 0]

# zip & enumerate 활용
for idx, val in enumerate(['a', 'b', 'c']):
    print(idx, val)
```

---

### 3. 핵심 자료구조 (Data Structures)

#### 3.1 선형 구조 및 deque (스택 & 큐)
- **정의**: 데이터를 일렬로 저장하는 선형 구조로, 스택(LIFO)과 큐(FIFO) 형태 포함.
- **의의**: 파이썬 `list`는 큐로 사용 시 `pop(0)` 연산이 $O(N)$ 시간을 소모함. 이를 $O(1)$로 처리하기 위해 `collections.deque` 사용 필수.
- **실제 예시 및 원리**:
```python
from collections import deque

queue = deque([1, 2, 3])
queue.append(4)       # 우측 삽입 O(1)
queue.popleft()       # 좌측 추출 O(1) -> 큐 연산

stack = []
stack.append(1)       # Push O(1)
stack.pop()           # Pop O(1) -> 스택 연산
```

#### 3.2 해시 구조 (dict, set, Counter, defaultdict)
- **정의**: 키-값 쌍을 해시 테이블로 관리하여 $O(1)$ 시간 내 탐색 및 저장을 지원하는 구조. 
- **의의**: 중복 제거, 빈도수 집합, 탐색 연산 시 `in` 탐색을 $O(N)$에서 $O(1)$로 단축.
- **실제 예시 및 원리**:
```python
from collections import Counter, defaultdict

# 빈도수 계산
counts = Counter(['apple', 'banana', 'apple'])

# 기본값이 자동 생성되는 딕셔너리 (그래프 인접 리스트에 유용)
graph = defaultdict(list)
graph[1].append(2)  # 키 1이 없어도 자동 생성 후 append
```

#### 3.3 우선순위 큐 (heapq)
- **정의**: 원소 중 최솟값(또는 최댓값)을 $O(\log N)$ 시간 내에 추출할 수 있는 완전 이진 트리 기반 구조.
- **의의**: 다익스트라 최단 경로 알고리즘, 그리디 문제에서 매 순간 최솟값/최댓값을 효율적으로 탐색할 때 사용.
- **실제 예시 및 원리**:
```python
import heapq

heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 5)

min_val = heapq.heappop(heap) # 1 반환 O(log N)

# 최대 힙 구현 방식 (음수 부호 전환)
max_heap = []
heapq.heappush(max_heap, -3)
max_val = -heapq.heappop(max_heap) # 3 반환
```

---

### 4. 핵심 알고리즘 (Algorithms)

#### 4.1 정렬 & 이진 탐색 (bisect)
- **정의**: 데이터를 특정 기준 순서대로 나열하거나, 정렬된 데이터에서 $O(\log N)$으로 위치를 탐색하는 방법.
- **의의**: 정렬 기반 문제 풀이 및 대용량 범위 내 탐색 시 필수 도구.
- **실제 예시 및 원리**:
```python
from bisect import bisect_left, bisect_right

arr = [1, 2, 4, 4, 4, 6, 8]

# 특정 값의 개수 구하기 O(log N)
def count_by_range(a, left_val, right_val):
    r_idx = bisect_right(a, right_val)
    l_idx = bisect_left(a, left_val)
    return r_idx - l_idx

# 4의 개수: 5 - 2 = 3
print(count_by_range(arr, 4, 4))
```

#### 4.2 완전 탐색 & 순열/조합 (itertools)
- **정의**: 모든 가능 조합을 탐색하는 방법 및 `itertools` 라이브러리를 통한 순열/조합 생성.
- **의의**: $N$이 작을 때 백트래킹(DFS) 코드를 직접 짜지 않고 라이브러리로 빠르게 구현 가능.
- **실제 예시 및 원리**:
```python
from itertools import permutations, combinations

items = ['A', 'B', 'C']
perms = list(permutations(items, 2))  # [('A','B'), ('A','C'), ...] -> 순열
combs = list(combinations(items, 2))  # [('A','B'), ('A','C'), ('B','C')] -> 조합
```

#### 4.3 그래프 탐색 (DFS & BFS)
- **정의**: 노드와 간선으로 이루어진 그래프 구조를 깊이 우선(DFS) 또는 너비 우선(BFS)으로 탐색하는 방법.
- **의의**: 최단 거리(BFS), 연결 요소 탐색, 미로 찾기 등 코딩테스트 출제 비중이 가장 높은 유형.
- **실제 예시 및 원리**:
```python
from collections import deque

# BFS (최단 거리 탐색)
def bfs(graph, start, visited):
    queue = deque([start])
    visited[start] = True
    while queue:
        v = queue.popleft()
        for i in graph[v]:
            if not visited[i]:
                queue.append(i)
                visited[i] = True

# DFS (재귀 깊이 탐색)
def dfs(graph, v, visited):
    visited[v] = True
    for i in graph[v]:
        if not visited[i]:
            dfs(graph, i, visited)
```

---

### 5. 실전 예외 처리 및 주의사항

#### 5.1 재귀 깊이 제어 (sys.setrecursionlimit)
- **정의**: 파이썬의 기본 재귀 깊이 한계(기본 1,000회)를 설정값을 통해 확장하는 방법.
- **의의**: 깊은 DFS 탐색 시 발생할 수 있는 `RecursionError` 방지.
- **실제 예시 및 원리**:
```python
import sys
sys.setrecursionlimit(10**6) # 재귀 한도를 100만으로 설정
```

#### 5.2 파이썬 주요 실수 패턴
- **2차원 배열 복사 에러**: `arr2 = arr1`은 얕은 복사이므로 `[row[:] for row in arr1]` 또는 `copy.deepcopy()` 사용.
- **시간 초과 원인**:
  - `list`의 `in` 연산 ($O(N)$ -> `set`으로 변환 필요)
  - `list.pop(0)` 또는 `list.insert(0, val)` ($O(N)$ -> `deque` 활용)
  - 큰 문자열 반복 덧붙이기 (`+=`) -> `''.join(list)` 활용
