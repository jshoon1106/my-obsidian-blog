### 1. 개요 및 실전 문제 풀이 목표

#### 1.1 개요
- **목적**: 학부생 컴퓨터공학/소프트웨어 전공자 수준(백준 실버 I ~ 골드 IV, 프로그래머스 Lv 2~3)의 핵심 알고리즘 실전 문제 구현 능력 배양.
- **주요 영역**: 그래프 탐색(BFS/DFS), 탐욕법(Greedy), 이진 탐색(Parametric Search), 동적 계획법(DP), 우선순위 큐(Heap).

---

### 2. 학부생 핵심 실전 문제 5선 및 풀이

#### 2.1 [BFS] 2차원 미로 최단 경로
- **개념**: $N \times M$ 격자 미로에서 (1,1)에서 (N,M)까지의 최단 칸 수 구하기 (1: 이동 가능, 0: 벽).
- **해결 전략**: `collections.deque` 기반 너비 우선 탐색. 탐색 시 이전 칸 값 + 1 갱신으로 최단 거리 기록.
- **시간 복잡도**: $O(N \times M)$

```python
from collections import deque
import sys

def solve_maze(n, m, grid):
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    queue = deque([(0, 0)])
    
    while queue:
        x, y = queue.popleft()
        
        if x == n - 1 and y == m - 1:
            return grid[x][y]
            
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == 1:
                grid[nx][ny] = grid[x][y] + 1
                queue.append((nx, ny))
                
    return grid[n-1][m-1]
```

#### 2.2 [그리디 & 정렬] 회의실 배정
- **개념**: 1개의 회의실에 대해 $N$개의 회의 신청 $(S_i, E_i)$ 중 겹치지 않는 최대 회의 개수 구하기.
- **해결 전략**: 종료 시간($E_i$) 기준 오름차순 정렬 후 탐욕적 선택.
- **시간 복잡도**: $O(N \log N)$

```python
import sys

def max_meetings(meetings):
    meetings.sort(key=lambda x: (x[1], x[0]))
    
    count = 0
    end_time = 0
    
    for start, end in meetings:
        if start >= end_time:
            count += 1
            end_time = end
            
    return count
```

#### 2.3 [이진 탐색] 랜선 자르기 (Parametric Search)
- **개념**: $K$개의 랜선으로 같은 길이의 $N$개 이상 랜선을 만들 때 가능한 최대 랜선 길이 구하기.
- **해결 전략**: 탐색 범위 $[1, \max(\text{cables})]$ 설정 후 이진 탐색으로 조건 만족 최대 길이 산출.
- **시간 복잡도**: $O(K \log (\max(\text{cables})))$

```python
import sys

def max_cable_length(k, n, cables):
    start = 1
    end = max(cables)
    result = 0
    
    while start <= end:
        mid = (start + end) // 2
        count = sum(cable // mid for cable in cables)
        
        if count >= n:
            result = mid
            start = mid + 1
        else:
            end = mid - 1
            
    return result
```

#### 2.4 [동적 계획법] RGB거리 최소 비용
- **개념**: $N$개의 집을 빨강, 초록, 파랑으로 칠하는 비용이 주어질 때 이웃한 집 색이 겹치지 않는 최소 비용 구하기.
- **해결 전략**: `dp[i][color]` 상태 정의 후 이전 집의 타 색상 최솟값 가산 점화식 적용.
- **시간 복잡도**: $O(N)$

```python
import sys

def min_rgb_cost(n, costs):
    dp = [[0] * 3 for _ in range(n)]
    dp[0] = costs[0]
    
    for i in range(1, n):
        dp[i][0] = min(dp[i-1][1], dp[i-1][2]) + costs[i][0]
        dp[i][1] = min(dp[i-1][0], dp[i-1][2]) + costs[i][1]
        dp[i][2] = min(dp[i-1][0], dp[i-1][1]) + costs[i][2]
        
    return min(dp[n-1])
```

#### 2.5 [우선순위 큐] 절댓값 힙 구현
- **개념**: 정수 $X$ 삽입 및 절댓값이 가장 작은 값(동률 시 작은 원시 값) 출력/제거 처리.
- **해결 전략**: 파이썬 `heapq` 모듈 활용, 튜플 `(abs(x), x)` 형태로 최소 힙 구조 구성.
- **시간 복잡도**: 연산당 $O(\log N)$

```python
import heapq
import sys

def abs_heap_operations(operations):
    heap = []
    results = []
    
    for x in operations:
        if x != 0:
            heapq.heappush(heap, (abs(x), x))
        else:
            if heap:
                results.append(heapq.heappop(heap)[1])
            else:
                results.append(0)
                
    return results
```
