# Day 14 — Exercises

## AI Evaluation & Benchmarking · Lab Worksheet

**Thời gian làm bài:** 09:15–12:00

**Domain:** Northstar University Student Services

Điền trực tiếp câu trả lời vào file này. Golden dataset 20 QA được viết một lần
duy nhất trong `golden_dataset.json`, không chép lại toàn bộ vào Markdown.

---

Từ 09:15–09:30, cài môi trường và chạy baseline tests theo `guide_lab.md`.

---

## Part 1 — Warm-up (09:30–09:45)

### Exercise 1.1 — RAGAS Metric Thresholds

Theo bài giảng:

- 0.8–1.0: Good — monitor, maintain.
- 0.6–0.8: Needs work — analyze failures, iterate.
- Dưới 0.6: Significant issues — investigate.

Với từng metric, xác định khi nào score thấp có thể chấp nhận và khi nào là
critical.

| Metric | Trường hợp điểm thấp có thể chấp nhận | Trường hợp điểm thấp nghiêm trọng | Hành động cần thực hiện |
|---|---|---|---|
| Faithfulness | Điểm 0.6-0.8 có thể chấp nhận với câu trả lời thăm dò hoặc khi ngữ cảnh chuẩn chưa đầy đủ, nếu các claim rủi ro cao được kiểm tra. | Dưới 0.6, đặc biệt với chính sách, học phí, thời hạn hoặc an toàn/quyền riêng tư: câu trả lời có thể thiếu căn cứ hoặc bị bịa. | Kiểm tra trích dẫn và bằng chứng đã truy xuất; cải thiện grounding/retrieval và yêu cầu hệ thống từ chối khi thiếu bằng chứng. |
| Answer Relevance | Điểm 0.6-0.8 có thể chấp nhận với câu hỏi rộng hoặc mơ hồ nếu câu trả lời có hướng làm rõ hữu ích. | Dưới 0.6 nghĩa là câu trả lời không đáp ứng ý định của sinh viên, nhất là với yêu cầu hành chính khẩn cấp. | Kiểm tra nhận diện ý định và prompt/routing; bổ sung câu hỏi đại diện, yêu cầu trả lời trực tiếp hoặc hỏi lại để làm rõ. |
| Context Recall | Điểm 0.6-0.8 có thể chấp nhận với tra cứu đơn giản chỉ cần một chunk hoặc khi bằng chứng bị thiếu không mang tính thiết yếu. | Dưới 0.6 khi thiếu quy tắc đủ điều kiện, ngoại lệ, ngày tháng hoặc các bước bắt buộc. | Cải thiện mở rộng truy vấn, lập chỉ mục, chia chunk và lọc metadata; kiểm thử câu hỏi nhiều tài liệu và trường hợp biên. |
| Context Precision | Điểm 0.6-0.8 có thể chấp nhận khi các chunk thừa không gây hại và ưu tiên độ trễ/chi phí. | Dưới 0.6 khi chunk chính sách không liên quan hoặc mâu thuẫn chiếm các vị trí đầu và có thể làm sai phần sinh câu trả lời. | Tinh chỉnh xếp hạng và bộ lọc, giảm kết quả top-k nhiễu, xác minh bộ sinh trích dẫn đúng chunk liên quan. |
| Completeness | Điểm 0.6-0.8 có thể chấp nhận với câu trả lời ban đầu ngắn nếu chi tiết bị bỏ sót là tùy chọn và câu trả lời chỉ rõ bước tiếp theo. | Dưới 0.6 khi thiếu bước bắt buộc, thời hạn, điều kiện đủ tiêu chuẩn, ngoại lệ hoặc kênh chuyển tiếp. | Đối chiếu với các ý bắt buộc; cải thiện retrieval và template trả lời có cấu trúc, sau đó human review các case có tác động cao. |

### Exercise 1.2 — Bias trong LLM-as-a-Judge

Ba bias thường gặp:

- Position bias: judge ưu tiên answer xuất hiện trước.
- Verbosity bias: judge ưu tiên answer dài hơn.
- Self-preference: judge ưu tiên output giống chính model đó.

**Câu 1: Thiết kế experiment phát hiện position bias với ít nhất hai conditions.**

> Dùng cùng một tập câu hỏi và các cặp câu trả lời đã được người đánh giá kiểm tra là tương đương về chất lượng. Ở điều kiện A, đặt câu trả lời A trước B; ở điều kiện B, đảo thứ tự. Xáo trộn câu hỏi và chạy nhiều lần nếu bộ đánh giá có tính ngẫu nhiên. So sánh điểm/lựa chọn giữa hai điều kiện: nếu câu trả lời đặt trước thường thắng hoặc điểm thay đổi đáng kể dù nội dung không đổi, đó là position bias. Có thể thêm điều kiện C với thứ tự ngẫu nhiên để kiểm chứng.

**Câu 2: Làm thế nào giảm verbosity bias bằng rubric design?**

> Rubric phải chấm theo các tiêu chí độc lập và chất lượng thông tin, không theo độ dài. Nêu rõ các sự kiện/bước bắt buộc, độ đúng, grounding và mức độ trực tiếp; quy định rằng câu trả lời ngắn nhưng đủ ý được điểm tối đa, còn phần lan man hoặc lặp lại không được cộng điểm. Tách completeness khỏi văn phong và yêu cầu bộ đánh giá giải thích điểm bằng bằng chứng cụ thể.

**Câu 3: Tại sao cần calibrate LLM judge với human labels?**

> Nhãn của con người là mốc chuẩn để đo độ đồng thuận, phát hiện bộ đánh giá quá dễ/quá khắt khe và kiểm tra việc chấm có đúng tiêu chí lĩnh vực hay không. Calibration giúp hiệu chỉnh rubric/prompt, chọn ngưỡng, phát hiện drift và tránh biến bias ổn định của model thành quality gate tự động. Các case bất đồng hoặc rủi ro cao cần được người đánh giá xem xét.

### Exercise 1.3 — Evaluation trong CI/CD

**Câu 1: Chọn threshold để block deployment.**

| Metric | Ngưỡng | Lý do |
|---|---:|---|
| Faithfulness | 0.80 | Chặn nếu điểm trung bình dưới 0.80 hoặc có case nghiêm trọng dưới 0.60; claim chính sách không có căn cứ là lỗi chặn phát hành. |
| Answer Relevance | 0.75 | Chặn nếu điểm trung bình dưới 0.75 hoặc nhóm ý định quan trọng dưới 0.60; câu trả lời phải đáp ứng hoặc làm rõ ý định. |
| Completeness | 0.75 | Chặn nếu điểm trung bình dưới 0.75 hoặc bỏ sót bước/thời hạn bắt buộc trong các case cần thiết. |

**Câu 2: Khi nào dùng offline evaluation, online evaluation và human review?**

> Đánh giá offline dùng trước mỗi lần phát hành và sau khi đổi model, prompt, retriever hoặc chunking, với golden dataset để kiểm thử hồi quy. Đánh giá online dùng sau khi triển khai trên lưu lượng thật để theo dõi drift, độ trễ, chi phí và phản hồi. Người đánh giá xem xét thủ công để tạo/hiệu chỉnh nhãn, kiểm tra các case rủi ro cao hoặc case có bất đồng giữa bộ đánh giá và kiểm tra theo luật, đồng thời đánh giá truy vấn mới/đối kháng. Kết quả online và human review nên được đưa ngược vào dataset và bộ kiểm thử hồi quy.

---

## Part 2 — Core Coding (09:45–10:40)

Hoàn thiện các TODO bắt buộc trong `template.py`.

### Task 1 — Data Models

- `QAPair`: question, expected answer, gold context, metadata và retrieved contexts.
- `EvalResult`: answer-side scores, optional retrieval scores, pass/failure fields.
- `overall_score()`: trung bình Faithfulness, Relevance và Completeness.

### Task 2 — RAGASEvaluator

Answer-side:

- `evaluate_faithfulness(answer, context)`
- `evaluate_relevance(answer, question)`
- `evaluate_completeness(answer, expected)`

Retrieval-side:

- `evaluate_context_recall(contexts, expected)`
- `evaluate_context_precision(contexts, expected)`

Full pipeline:

- `run_full_eval(..., contexts=None)` luôn tính ba answer metrics.
- Nếu có `contexts`, tính và lưu thêm Context Recall và Context Precision.
- Retrieval scores không làm thay đổi `overall_score()` và pass rule gốc.

### Task 3 — LLMJudge

- `score_response(question, answer, rubric)`
- `detect_bias(scores_batch)`

### Task 4 — BenchmarkRunner

- `run(qa_pairs, agent_fn, evaluator)`
- `generate_report(results)`
- `run_regression(new_results, baseline_results)`
- `identify_failures(results, threshold)`

`BenchmarkRunner.run()` phải truyền `pair.retrieved_contexts` vào
`run_full_eval()`. Report phải có average của hai retrieval metrics.

### Task 5 — FailureAnalyzer

- `categorize_failures(failures)`
- `find_root_cause(failure)`
- `generate_improvement_suggestions(failures)`
- `generate_improvement_log(failures, suggestions)`

Kiểm tra:

```bash
pytest tests/ -v
```

`rerank_by_overlap()` là TODO bonus của Exercise 3.5. Test tương ứng được skip
nếu bạn chưa làm bonus.

---

## Part 3 — Golden Dataset & Real Benchmark (10:40–11:35)

### Exercise 3.1 — Build the Golden Dataset

Thiết kế và validate dataset theo Mục 5–6 trong `guide_lab.md`. Nội dung 20 QA
được điền trực tiếp trong `golden_dataset.json`; phần dưới chỉ ghi lại kết quả
và quyết định thiết kế, không chép lại toàn bộ QA.

**Kết quả dataset**

| Hạng mục | Kết quả |
|---|---|
| Tổng số records | ____ / 20 |
| Easy | ____ / 5 |
| Medium | ____ / 7 |
| Hard | ____ / 5 |
| Adversarial | ____ / 3 |
| Source documents được sử dụng | ____ / 10 |
| Validator status | PASS / FAIL |

**Ba case đại diện cho quyết định thiết kế**

| ID | Difficulty | Source document(s) | Vì sao case phù hợp với difficulty/attack type? |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

**Điểm khó nhất khi xây dựng expected answer hoặc evidence là gì?**

> *Câu trả lời:*

**Xác nhận:**

- [ ] Mọi claim trong expected answer đều có evidence hỗ trợ.
- [ ] Không có questions trùng ý và không dùng kiến thức ngoài corpus.
- [ ] `python validate_golden_dataset.py` báo `PASS`.

### Exercise 3.2 — Benchmark Run

Chạy:

```bash
python domain_assistant.py
python evaluate_answers.py
```

Copy bảng terminal vào đây hoặc điền từ `artifacts/benchmark_results.json`.

| ID | Question (short) | Ctx Recall | Ctx Precision | Faithfulness | Relevance | Completeness | Overall | Passed? | Failure Type |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| E01 | | | | | | | | | |
| E02 | | | | | | | | | |
| E03 | | | | | | | | | |
| E04 | | | | | | | | | |
| E05 | | | | | | | | | |
| M01 | | | | | | | | | |
| M02 | | | | | | | | | |
| M03 | | | | | | | | | |
| M04 | | | | | | | | | |
| M05 | | | | | | | | | |
| M06 | | | | | | | | | |
| M07 | | | | | | | | | |
| H01 | | | | | | | | | |
| H02 | | | | | | | | | |
| H03 | | | | | | | | | |
| H04 | | | | | | | | | |
| H05 | | | | | | | | | |
| A01 | | | | | | | | | |
| A02 | | | | | | | | | |
| A03 | | | | | | | | | |

**Aggregate Report**

- Overall pass rate: ____%
- Avg Context Recall: ____
- Avg Context Precision: ____
- Avg Faithfulness: ____
- Avg Relevance: ____
- Avg Completeness: ____
- Failure type distribution: ____

**Ba cases có Overall Score thấp nhất**

1. ID: ____ | Score: ____ | Failure type: ____
2. ID: ____ | Score: ____ | Failure type: ____
3. ID: ____ | Score: ____ | Failure type: ____

**Nhận xét ngắn:** Metric nào yếu nhất? Kết quả gợi ý vấn đề nằm ở retrieval
hay generation?

> *Câu trả lời:*

### Exercise 3.3 — LLM-as-a-Judge Rubric Design

Thiết kế rubric domain-specific cho Student Services. Mỗi mức phải đủ cụ thể để
hai người chấm độc lập có thể hiểu giống nhau.

Chọn 3–5 dimensions:

- [ ] Correctness
- [ ] Completeness
- [ ] Relevance
- [ ] Evidence/citation
- [ ] Actionability
- [ ] Safety/privacy
- [ ] Tone/clarity
- [ ] Dimension khác: __________

| Score | Tiêu chí domain-specific | Ví dụ response |
|---:|---|---|
| 5 | | |
| 4 | | |
| 3 | | |
| 2 | | |
| 1 | | |

**Ba edge cases khó chấm**

| Edge Case | Tại sao khó chấm? | Rubric xử lý thế nào? |
|---|---|---|
| | | |
| | | |
| | | |

**Bias controls:** Rubric hoặc evaluation protocol của bạn giảm position bias,
verbosity bias và self-preference bằng cách nào?

> *Câu trả lời:*

### Exercise 3.4 — Framework Comparison (Bonus +10)

Chỉ làm sau khi hoàn thành 3.1–3.3. Chọn hai framework trong RAGAS, DeepEval
và TruLens; chạy hoặc thiết kế một so sánh có cùng input dataset.

| Tiêu chí | Framework 1: ____ | Framework 2: ____ |
|---|---|---|
| Setup complexity | | |
| Metrics available | | |
| CI/CD integration | | |
| Kết quả trên cùng dataset | | |
| Insight rút ra | | |

- Scores có nhất quán không?
- Framework nào strict hơn và vì sao?
- Hai framework có tìm ra cùng failure cases không?

> *Phân tích:*

### Exercise 3.5 — Retrieval Reranking (Bonus +5)

Mục tiêu: kiểm tra việc đổi thứ tự chunks có tăng Context Precision mà không
thay đổi Context Recall hay không.

1. Chọn ít nhất 5 cases từ `artifacts/actual_answers.json`.
2. Tính Context Recall và Context Precision trước rerank.
3. Implement `rerank_by_overlap()` hoặc một reranker khác.
4. Rerank cùng tập chunks, không thêm hoặc xóa chunk.
5. Tính lại hai metrics và giải thích kết quả.

| ID | Recall before | Recall after | Precision before | Precision after | Delta Precision |
|---|---:|---:|---:|---:|---:|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| **Avg** | | | | | |

**Tại sao Recall dự kiến không đổi?**

> *Câu trả lời:*

**Khi nào reranking không đủ và cần sửa retriever/query/chunking?**

> *Câu trả lời:*

---

## Part 4 — Reflection (11:35–11:50)

Hoàn thành `reflection.md` bằng kết quả thật từ Exercise 3.2.

---

## Completion Checklist

Hoàn thành kiểm tra cuối trong khoảng 11:50–12:00.

- [ ] Tất cả required tests pass.
- [ ] `golden_dataset.json` validate thành công.
- [ ] Exercise 3.1 hoàn thành trong file JSON và bảng kết quả phía trên.
- [ ] Exercise 3.2 có năm metrics, aggregate report và ba cases thấp nhất.
- [ ] Exercise 3.3 có rubric 1–5 và bias controls.
- [ ] `reflection.md` có ba failure analyses và regression strategy.
- [ ] Đã copy `template.py` thành `solution/solution.py`.
- [ ] Exercise 3.4 và 3.5 chỉ làm nếu chọn bonus.
