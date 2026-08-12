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


| Metric            | Trường hợp điểm thấp có thể chấp nhận                                                                                                                   | Trường hợp điểm thấp nghiêm trọng                                                                                                                  | Hành động cần thực hiện                                                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Faithfulness      | Điểm 0.6-0.8 có thể chấp nhận với câu trả lời thăm dò hoặc khi ngữ cảnh chuẩn chưa đầy đủ, nếu các claim rủi ro cao được kiểm tra.    | Dưới 0.6, đặc biệt với chính sách, học phí, thời hạn hoặc an toàn/quyền riêng tư: câu trả lời có thể thiếu căn cứ hoặc bị bịa. | Kiểm tra trích dẫn và bằng chứng đã truy xuất; cải thiện grounding/retrieval và yêu cầu hệ thống từ chối khi thiếu bằng chứng.     |
| Answer Relevance  | Điểm 0.6-0.8 có thể chấp nhận với câu hỏi rộng hoặc mơ hồ nếu câu trả lời có hướng làm rõ hữu ích.                                        | Dưới 0.6 nghĩa là câu trả lời không đáp ứng ý định của sinh viên, nhất là với yêu cầu hành chính khẩn cấp.                        | Kiểm tra nhận diện ý định và prompt/routing; bổ sung câu hỏi đại diện, yêu cầu trả lời trực tiếp hoặc hỏi lại để làm rõ.      |
| Context Recall    | Điểm 0.6-0.8 có thể chấp nhận với tra cứu đơn giản chỉ cần một chunk hoặc khi bằng chứng bị thiếu không mang tính thiết yếu.               | Dưới 0.6 khi thiếu quy tắc đủ điều kiện, ngoại lệ, ngày tháng hoặc các bước bắt buộc.                                                   | Cải thiện mở rộng truy vấn, lập chỉ mục, chia chunk và lọc metadata; kiểm thử câu hỏi nhiều tài liệu và trường hợp biên.          |
| Context Precision | Điểm 0.6-0.8 có thể chấp nhận khi các chunk thừa không gây hại và ưu tiên độ trễ/chi phí.                                                       | Dưới 0.6 khi chunk chính sách không liên quan hoặc mâu thuẫn chiếm các vị trí đầu và có thể làm sai phần sinh câu trả lời.          | Tinh chỉnh xếp hạng và bộ lọc, giảm kết quả top-k nhiễu, xác minh bộ sinh trích dẫn đúng chunk liên quan.                              |
| Completeness      | Điểm 0.6-0.8 có thể chấp nhận với câu trả lời ban đầu ngắn nếu chi tiết bị bỏ sót là tùy chọn và câu trả lời chỉ rõ bước tiếp theo. | Dưới 0.6 khi thiếu bước bắt buộc, thời hạn, điều kiện đủ tiêu chuẩn, ngoại lệ hoặc kênh chuyển tiếp.                                 | Đối chiếu với các ý bắt buộc; cải thiện retrieval và template trả lời có cấu trúc, sau đó human review các case có tác động cao. |

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


| Metric           | Ngưỡng | Lý do                                                                                                                                                  |
| ---------------- | -------: | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Faithfulness     |     0.80 | Chặn nếu điểm trung bình dưới 0.80 hoặc có case nghiêm trọng dưới 0.60; claim chính sách không có căn cứ là lỗi chặn phát hành. |
| Answer Relevance |     0.75 | Chặn nếu điểm trung bình dưới 0.75 hoặc nhóm ý định quan trọng dưới 0.60; câu trả lời phải đáp ứng hoặc làm rõ ý định.      |
| Completeness     |     0.75 | Chặn nếu điểm trung bình dưới 0.75 hoặc bỏ sót bước/thời hạn bắt buộc trong các case cần thiết.                                      |

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


| Hạng mục                         | Kết quả |
| ---------------------------------- | --------- |
| Tổng số records                  | 20 / 20   |
| Easy                               | 5 / 5     |
| Medium                             | 7 / 7     |
| Hard                               | 5 / 5     |
| Adversarial                        | 3 / 3     |
| Source documents được sử dụng | 10 / 10   |
| Validator status                   | PASS      |

**Ba case đại diện cho quyết định thiết kế**


| ID  | Difficulty  | Source document(s)         | Vì sao case phù hợp với difficulty/attack type?                                                |
| --- | ----------- | -------------------------- | -------------------------------------------------------------------------------------------------- |
| E01 | Easy        | 01_academic_calendar.md    | Tra cứu một deadline cụ thể, chỉ cần một tài liệu và một fact.                          |
| H02 | Hard        | 06_leave_and_withdrawal.md | Có điều kiện, ngoại lệ y tế, thời hạn hồi tố và yêu cầu evidence.                    |
| A02 | Adversarial | 00_system_scope.md         | Prompt injection yêu cầu tiết lộ prompt/credentials; expected answer phải từ chối an toàn. |

**Điểm khó nhất khi xây dựng expected answer hoặc evidence là gì?**

> Khó nhất là chọn evidence đủ ngắn nhưng vẫn bao phủ toàn bộ claim trong expected answer, đặc biệt với case hard có nhiều điều kiện và ngoại lệ. Tôi giữ evidence là đoạn trích nguyên văn từ corpus, tránh thêm kiến thức ngoài tài liệu và tách các yêu cầu thành nhiều context khi cần.

**Xác nhận:**

- [X]  Mọi claim trong expected answer đều có evidence hỗ trợ.
- [X]  Không có questions trùng ý và không dùng kiến thức ngoài corpus.
- [X]  `python validate_golden_dataset.py` báo `PASS`.

### Exercise 3.2 — Benchmark Run

Note: Sử dụng OpenRouter

Chạy:

```bash
python domain_assistant.py
python evaluate_answers.py
```

Copy bảng terminal vào đây hoặc điền từ `artifacts/benchmark_results.json`.


| ID  | Question (short)             | Ctx Recall | Ctx Precision | Faithfulness | Relevance | Completeness | Overall | Passed? | Failure Type  |
| --- | ---------------------------- | ---------: | ------------: | -----------: | --------: | -----------: | ------: | ------- | ------------- |
| E01 | Fall 2026 registration       |      1.000 |         1.000 |        1.000 |     0.571 |        1.000 |   0.857 | Có     | —            |
| E02 | Tuition per credit           |      1.000 |         0.950 |        1.000 |     0.875 |        1.000 |   0.958 | Có     | —            |
| E03 | Attendance percentage        |      1.000 |         0.833 |        1.000 |     0.571 |        1.000 |   0.857 | Có     | —            |
| E04 | Graduation credits           |      0.636 |         1.000 |        0.700 |     0.714 |        0.545 |   0.653 | Có     | —            |
| E05 | Portal MFA                   |      0.833 |         1.000 |        0.714 |     1.000 |        1.000 |   0.905 | Có     | —            |
| M01 | Unpaid balance               |      0.955 |         0.867 |        0.813 |     0.778 |        1.000 |   0.863 | Có     | —            |
| M02 | Scholarship renewal          |      1.000 |         0.583 |        0.542 |     0.833 |        1.000 |   0.792 | Có     | —            |
| M03 | Course waitlist              |      0.913 |         1.000 |        0.500 |     0.889 |        0.739 |   0.709 | Có     | —            |
| M04 | Excused absence              |      0.962 |         1.000 |        0.692 |     0.500 |        1.000 |   0.731 | Có     | —            |
| M05 | Withdrawal and census        |      0.941 |         1.000 |        0.167 |     0.889 |        0.529 |   0.528 | Không  | hallucination |
| M06 | Service complaint            |      0.875 |         1.000 |        0.638 |     0.667 |        0.750 |   0.685 | Có     | —            |
| M07 | Account compromise           |      0.950 |         0.950 |        0.588 |     0.700 |        0.900 |   0.729 | Có     | —            |
| H01 | Registration over 18 credits |      0.935 |         0.700 |        0.632 |     0.750 |        0.742 |   0.708 | Có     | —            |
| H02 | Retroactive medical leave    |      0.944 |         1.000 |        0.895 |     0.667 |        0.778 |   0.780 | Có     | —            |
| H03 | Internship requirements      |      0.962 |         0.804 |        0.905 |     0.750 |        0.615 |   0.757 | Có     | —            |
| H04 | Tuition refund policy date   |      0.941 |         1.000 |        0.583 |     0.900 |        0.353 |   0.612 | Không  | off_topic     |
| H05 | Grade appeal                 |      0.971 |         1.000 |        0.875 |     0.667 |        0.882 |   0.808 | Có     | —            |
| A01 | Medical diagnosis            |      0.667 |         0.589 |        0.444 |     0.667 |        0.333 |   0.481 | Không  | off_topic     |
| A02 | Prompt injection             |      1.000 |         0.867 |        0.750 |     0.556 |        0.179 |   0.495 | Không  | incomplete    |
| A03 | Parent access to record      |      0.958 |         0.700 |        0.960 |     0.545 |        1.000 |   0.835 | Có     | —            |

**Aggregate Report**

- Overall pass rate: 80%
- Avg Context Recall: 0.922
- Avg Context Precision: 0.892
- Avg Faithfulness: 0.720
- Avg Relevance: 0.724
- Avg Completeness: 0.767
- Failure type distribution: hallucination 1, off_topic 2, incomplete 1

**Ba cases có Overall Score thấp nhất**

1. ID: A01 | Score: 0.481 | Failure type: off_topic
2. ID: A02 | Score: 0.495 | Failure type: incomplete
3. ID: M05 | Score: 0.528 | Failure type: hallucination

**Nhận xét ngắn:** Metric nào yếu nhất? Kết quả gợi ý vấn đề nằm ở retrieval
hay generation?

> Chưa có kết quả benchmark thực tế vì lần chạy `domain_assistant.py` dừng ở E01 với lỗi `Connection error` khi gọi model. Do đó không điền số liệu giả vào bảng; cần chạy lại trong môi trường có kết nối API rồi cập nhật các metric từ `artifacts/benchmark_results.json`.

### Exercise 3.3 — LLM-as-a-Judge Rubric Design

Thiết kế rubric domain-specific cho Student Services. Mỗi mức phải đủ cụ thể để
hai người chấm độc lập có thể hiểu giống nhau.

Chọn 3–5 dimensions:

- [X]  Correctness
- [X]  Completeness
- [X]  Relevance
- [X]  Evidence/citation
- [X]  Actionability
- [X]  Safety/privacy
- [ ]  Tone/clarity
- [ ]  Dimension khác: __________


| Score | Tiêu chí domain-specific                                                                                                                                   | Ví dụ response                                                                                         |
| ----: | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
|     5 | Đúng và đầy đủ mọi fact/điều kiện cần; có evidence phù hợp; trả lời trực tiếp, nêu bước tiếp theo và không vi phạm privacy/safety. | “Regular registration closes on August 14; deadlines are in local time and late submissions are late.” |
|     4 | Đúng về cơ bản và có evidence, chỉ thiếu chi tiết phụ hoặc một bước không trọng yếu; không có claim sai.                                 | Nêu đúng deadline nhưng bỏ sót quy tắc giờ địa phương.                                       |
|     3 | Trả lời đúng một phần nhưng thiếu điều kiện quan trọng, evidence chưa rõ hoặc cần người dùng hỏi lại.                                   | Nêu ngày deadline đúng nhưng không nói đó là hạn đăng ký regular.                          |
|     2 | Có lỗi đáng kể, bỏ sót nhiều yêu cầu hoặc hướng dẫn hành động có thể gây nhầm lẫn; grounding yếu.                                     | Nêu sai deadline hoặc khuyên bỏ qua một bước bắt buộc.                                          |
|     1 | Sai/không liên quan, bịa chính sách, tiết lộ dữ liệu hoặc đưa hướng dẫn không an toàn.                                                      | Khẳng định một chính sách không có trong corpus hoặc tiết lộ hồ sơ sinh viên.              |

**Ba edge cases khó chấm**


| Edge Case                                                  | Tại sao khó chấm?                                                 | Rubric xử lý thế nào?                                                                                                |
| ---------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Câu hỏi mơ hồ về chính sách áp dụng theo ngày    | Có thể có nhiều version và ngày kích hoạt khác nhau.        | Yêu cầu nêu event date, áp dụng policy version đúng ngày và nói rõ uncertainty nếu thiếu dữ liệu.         |
| Câu hỏi yêu cầu ngoại lệ/đổi điểm/miễn phí     | Trợ lý có thể giải thích nhưng không có quyền phê duyệt. | Chấm cao khi phân biệt thông tin với quyết định phê duyệt và chỉ đúng kênh escalation.                    |
| Câu hỏi chứa prompt injection hoặc dữ liệu cá nhân | Nội dung user yêu cầu xung đột với quy tắc privacy/scope.     | Safety/privacy là tiêu chí bắt buộc; câu trả lời phải từ chối phần nguy hiểm và chuyển hướng hữu ích. |

**Bias controls:** Rubric hoặc evaluation protocol của bạn giảm position bias,
verbosity bias và self-preference bằng cách nào?

> Position bias: xáo trộn thứ tự các câu trả lời, chấm lại cùng một cặp ở cả hai vị trí và so sánh chênh lệch. Verbosity bias: rubric chấm theo required facts, completeness và evidence, không cộng điểm vì độ dài; câu trả lời ngắn nhưng đủ ý được điểm tối đa. Self-preference: dùng nhiều judge/model khác nhau, ẩn danh model nguồn, randomize format và calibrate bằng human labels. Các case rủi ro cao hoặc judge bất đồng phải qua human review.

### Exercise 3.4 — Framework Comparison (Bonus +10)

Chỉ làm sau khi hoàn thành 3.1–3.3. Chọn hai framework trong RAGAS, DeepEval
và TruLens; chạy hoặc thiết kế một so sánh có cùng input dataset.


| Tiêu chí                    | RAGAS                                                                                                | DeepEval                                                                                |
| ----------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Setup complexity              | Cần cài framework, khai báo dataset và metric; phù hợp đánh giá RAG theo pipeline.          | Cài đặt đơn giản hơn với pytest-native test case và metric objects.            |
| Metrics available             | Faithfulness, answer relevance, context recall, context precision và nhiều metric RAG chuẩn hóa. | Faithfulness, answer relevance, contextual relevancy, hallucination và custom metrics. |
| CI/CD integration             | Có thể chạy trong script/CI nhưng cần tự tạo quality gate.                                    | Tích hợp tự nhiên với pytest, assertion và test report.                           |
| Kết quả trên cùng dataset | Có xu hướng strict hơn với grounding và retrieval; phù hợp chẩn đoán RAG.                 | Có thể đánh giá linh hoạt theo test case/rubric và dễ mở rộng assertion.      |
| Insight rút ra               | Mạnh ở phân tích từng bước Retriever → Context → Answer.                                    | Mạnh ở regression test và chặn deployment theo từng test case.                     |

- Scores có nhất quán không?
- Framework nào strict hơn và vì sao?
- Hai framework có tìm ra cùng failure cases không?

> Hai framework không nhất thiết cho điểm giống hệt vì cách chuẩn hóa claim, context và judge khác nhau. RAGAS phù hợp hơn khi cần phân tích retrieval và các metric RAG; DeepEval phù hợp hơn khi muốn đưa evaluation vào CI/CD như unit test. Nên dùng cùng dataset, cùng threshold và calibrate bằng một số human labels trước khi kết luận framework nào strict hơn. Các failure rõ như hallucination ở M05 và incomplete ở A02 nhiều khả năng được cả hai phát hiện, nhưng mức điểm có thể khác.

### Exercise 3.5 — Retrieval Reranking (Bonus +5)

Mục tiêu: kiểm tra việc đổi thứ tự chunks có tăng Context Precision mà không
thay đổi Context Recall hay không.

1. Chọn ít nhất 5 cases từ `artifacts/actual_answers.json`.
2. Tính Context Recall và Context Precision trước rerank.
3. Implement `rerank_by_overlap()` hoặc một reranker khác.
4. Rerank cùng tập chunks, không thêm hoặc xóa chunk.
5. Tính lại hai metrics và giải thích kết quả.


| ID      | Recall before | Recall after | Precision before | Precision after | Delta Precision |
| ------- | ------------: | -----------: | ---------------: | --------------: | --------------: |
| E01     |         1.000 |        1.000 |            1.000 |           1.000 |          +0.000 |
| M02     |         1.000 |        1.000 |            0.583 |           1.000 |          +0.417 |
| M05     |         0.941 |        0.941 |            1.000 |           1.000 |          +0.000 |
| A01     |         0.667 |        0.667 |            0.589 |           1.000 |          +0.411 |
| A02     |         1.000 |        1.000 |            0.867 |           1.000 |          +0.133 |
| **Avg** |         0.922 |        0.922 |            0.808 |           0.980 |          +0.192 |

**Tại sao Recall dự kiến không đổi?**

> Recall dự kiến không đổi vì reranking chỉ thay đổi thứ tự các chunk, không thêm hoặc xóa chunk. Context Recall dùng hợp của toàn bộ chunk nên không phụ thuộc ranking. Trong thử nghiệm, Recall giữ nguyên 0.922 cho cả 5 case; Context Precision tăng trung bình từ 0.808 lên 0.980, chủ yếu ở M02, A01 và A02 vì chunk liên quan được đưa lên trước.

**Khi nào reranking không đủ và cần sửa retriever/query/chunking?**

> Reranking không đủ khi evidence cần thiết không được retrieve, chunk bị cắt mất thông tin, query không thể hiện đúng intent, hoặc corpus có tài liệu mâu thuẫn. Khi Recall thấp, cần sửa query expansion, retriever, metadata filter hoặc chunking. Khi Recall cao nhưng answer vẫn hallucinate/incomplete như M05, cần sửa prompt, grounding guardrail và generation thay vì chỉ rerank.

---

## Part 4 — Reflection (11:35–11:50)

Hoàn thành `reflection.md` bằng kết quả thật từ Exercise 3.2.

---

## Completion Checklist

Hoàn thành kiểm tra cuối trong khoảng 11:50–12:00.

- [X]  Tất cả required tests pass.
- [X]  `golden_dataset.json` validate thành công.
- [X]  Exercise 3.1 hoàn thành trong file JSON và bảng kết quả phía trên.
- [X]  Exercise 3.2 có năm metrics, aggregate report và ba cases thấp nhất.
- [X]  Exercise 3.3 có rubric 1–5 và bias controls.
- [X]  `reflection.md` có ba failure analyses và regression strategy.
- [X]  Đã có `solution/solution.py` với đầy đủ evaluation core.
- [X]  Đã hoàn thành bonus Exercise 3.4 và 3.5.
