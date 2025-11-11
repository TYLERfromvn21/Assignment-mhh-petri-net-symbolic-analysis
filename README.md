# Assignment-mhh-petri-net-symbolic-analysis
CO2011 – Symbolic &amp; Algebraic Reasoning in Petri Nets – HCMUT- Bài tập lớn mô hình hóa- nhóm 3 thiên lý ơi

**HCMUT – Semester 1 (2025-2026)**  
**Nhóm: 3 thiên lý ơi**
Phân chia Petri nets 1-safe:
1. Parse PNML → internal model: Quốc Duy
2. Explicit reachability (BFS)             1 người
3. Symbolic reachability (BDD)             1 người + Quốc Duy
4. Deadlock detection (ILP + BDD)          1 người
5. Optimization over reachable markings    1 người

### Task 1 – Parser PNML
- **PNML (Petri Net Markup Language)** là **chuẩn XML quốc tế (ISO/IEC 15909-2)** để lưu Petri Net.  
- **File `.pnml`** chứa: `<place>`, `<transition>`, `<arc>`, `<initialMarking>`.  
- **Parser (`src/parser.py`)** làm gì?  
  1. Đọc file `.pnml` → kiểm tra **hợp lệ theo chuẩn** (dùng `lxml`).  
  2. Kiểm tra **1-safe**: không place nào có >1 token.  
  3. Trả về **Python dict**:  
     ```python
     net = {
         'places': {'p1': {'initial': 1}, ...},
         'transitions': {'t1': {}},
         'arcs': [('p1', 't1', 1), ...],
         'graph': NetworkX DiGraph,
         'initial_marking': {'p1': 1, 'p2': 0}
     }
## Cài đặt thư viện python
- pip install -r requirements.txt (hoặc lệnh khác)
- Đọc assignment PDF ("mm-251-assignment.pdf")
- Input chung: Net từ parse_pnml(file) (dict: places, transitions, arcs, initial_marking).

## Task 2 – Explicit computation of reachable markings (branch feature/task2)
- Nhiệm vụ chính: Implement BFS or DFS để enumerate reachable markings từ initial. 
- Output: List markings. Compare time/memory với Task 3.

File code cần tải: 
- src/task2_explicit_bfs.py (export hàm compute_reachable(net)).
- Examples PNML từ pnml.org (ví dụ philosophers.pnml – có deadlock: https://www.pnml.org/version-2009/examples/philo.pnml).


Input: Net từ parser task 1 (initial_marking).

Output: List dict markings (e.g., {'p1':0, 'p2':1}), total count, time/memory (dùng timeit, sys.getsizeof).

gợi ý : 
- BFS queue hoặc DFS với set visited. Check enabled transitions (tokens đủ arcs input).

Reference:
- PETRI_NETWORKS PDF remaining pages (reachability graph)
- Web: https://en.wikipedia.org/wiki/Petri_net (reachability).

Chú ý: 
- State space explosion – dùng small models (≤10 places). Assume 1-safe (marking 0/1).
- Run trên simple.pnml (2 markings), philosophers (deadlock states). Compare manual.

## Task 3 – Symbolic computation of reachable markings using BDD (branch feature/task3)

Nhiệm vụ chính: 
- Encode markings bằng BDD (places as variables, 0/1 tokens). Iterative fixed-point để build reachable set.
- Output: BDD, count markings, compare time/memory với Task 2.

File code cần tải:
- src/task3_symbolic_bdd.py (export hàm symbolic_reachable(net)).
- Examples PNML từ pnml.org (ví dụ philosophers.pnml – có deadlock: https://www.pnml.org/version-2009/examples/philo.pnml).

Input: Net từ parser.

Output: BDD object, total count (bdd.count()), time/memory.

Gợi ý: 
- Map places to variables. Initial BDD. Iterate image computation (pre/post sets).

References 
- Web: https://github.com/tulip-control/dd (dd docs), 
- https://en.wikipedia.org/wiki/Binary_decision_diagram. 
- References [2] Bryant BDD.

Chú ý: 
- Variable ordering quan trọng (bonus). Small models để tránh explosion.
- Compare count với Task 2. Use BDD dump để visualize.

## Task 4 – Deadlock detection using ILP and BDD (branch feature/task4)

Nhiệm vụ chính: 
- Kết hợp ILP với BDD từ Task 3 để find reachable dead marking (no enabled transition). 
- Output: Một deadlock marking hoặc "none", running time.

File code: 
- src/task4_deadlock_ilp.py (export hàm detect_deadlock(net, bdd_reach)).
- PuLP (requirements.txt).
- Examples PNML từ pnml.org (ví dụ philosophers.pnml – có deadlock: https://www.pnml.org/version-2009/examples/philo.pnml).

Input: Net, BDD reachable từ Task 3.

Output: Dict marking (dead & reachable) hoặc "none", time.

Gợi ý: 
- Formulate ILP: variables marking (0/1), constraints reachable (from BDD), no-enabled (tokens < arc weights cho all transitions). Solve minimize 1 (find one).

References  
- PETRI_NETWORKS PDF (deadlock section).
- Web: https://coin-or.github.io/pulp/ (PuLP docs).
- References [15] Murata, [17] Pastor.

Chú ý: 
- Deadlock = dead + reachable. Small models. Report time trên examples.
- Run trên philosophers (nên có deadlock), simple.pnml (no deadlock) trên github ở trên. Compare manual.

## Task 5 – Optimization over reachable markings (branch feature/task5)

Nhiệm vụ chính: 
- Given c (weights places), maximize c^T M over M reachable (từ BDD Task 3).
- Output: Optimal marking hoặc "none", running time. (20% điểm)

File code: 
- src/task5_optimize.py (export hàm optimize_reachable(net, bdd_reach, c)).
- PuLP từ requirement.txt. 
- Examples PNML từ pnml.org (ví dụ philosophers.pnml – có deadlock: https://www.pnml.org/version-2009/examples/philo.pnml).
- Tạo c random (e.g., [1,2,...] cho places).

Input: Net, BDD reachable, vector c.

Output: Dict optimal M hoặc "none", time.

Gợi ý: 
- ILP: variables M (0/1), objective max c^T M, constraints reachable (BDD to ILP), marking valid.

Web:
- PuLP docs. References [7] Graver ILP, [11] Kautz optimization.

Chú ý: 
- Linear objective, integer weights. Small models. Nếu unbounded, report none.
- Run trên simple.pnml với c=[1,1] (max tokens p2=1). Manual calc.

Tài liệu tham khảo
- Assignment PDF: mm-251-assignment.pdf (full tasks, references [1]-[22]).
- PETRI_NETWORKS-Version-0.2.pdf: Theory Petri nets.
- Matcovschi_Pastravanu_PNT_PNSB.pdf: MATLAB toolbox cho simulate/verify
