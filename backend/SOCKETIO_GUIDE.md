# Socket.IO 연동 가이드 (AI 비동기 처리 버전)

## 📌 개요

챕터 생성 시 AI가 콘텐츠를 생성하는 동안 실시간으로 진행 상황을 클라이언트에 알리기 위해 Socket.IO를 사용합니다.

Kafka → n8n → AI 처리가 오래 걸릴 수 있으므로, 클라이언트가 대기 중에도 연결을 유지하고 진행 상황을 확인할 수 있습니다.

## 🔄 처리 흐름

```
1. 클라이언트: Socket.IO 연결 + join_chapter
   ↓
2. 클라이언트: POST /v1/chapter/ (챕터 생성 요청)
   ↓
3. 백엔드: 챕터 + 빈 리소스 생성 (DB 저장)
   ↓
4. 백엔드: Socket.IO 알림 발송
   - chapter_processing_started (챕터 생성 시작)
   - concept_processing (개념 정리 AI 처리 시작)
   - exercise_processing (실습 과제 AI 처리 시작)
   - quiz_processing (퀴즈 AI 처리 시작)
   ↓
5. 백엔드: Kafka로 AI 생성 요청 전송 (3개 방향)
   ↓
   [시간이 오래 걸릴 수 있음 - 클라이언트는 Socket.IO로 대기 중]
   ↓
6. n8n: AI로부터 콘텐츠 생성 후 Webhook으로 응답
   - POST /v1/chapter/{id}/concept-finish
   - POST /v1/chapter/{id}/exercise-finish
   - POST /v1/chapter/{id}/quiz-finish
   ↓
7. 백엔드: DB 업데이트 + Socket.IO 완료 알림 발송
   - concept_completed
   - exercise_completed
   - quiz_completed
   - all_completed (모두 완료 시)
   ↓
8. 클라이언트: 실시간으로 완료 알림 수신 ✅
```

---

## 🚀 빠른 시작

### 1. 서버 실행
```bash
python main.py
```

### 2. 브라우저 테스트
```bash
open socket_client_example.html
```

---

## 🔌 클라이언트 연동

### JavaScript/TypeScript

```javascript
import io from 'socket.io-client';

// 1. Socket.IO 연결
const socket = io('http://localhost:8000');

// 2. 챕터 룸 참여
socket.on('connect', () => {
  console.log('Connected!');
  socket.emit('join_chapter', { chapter_id: 1 });
});

// 3. 이벤트 리스너 등록

// 챕터 생성 시작
socket.on('chapter_processing_started', (data) => {
  console.log('챕터 생성 시작:', data);
  // { chapter_id: 1, title: "...", status: "processing_started", message: "..." }
});

// AI 처리 시작 알림들
socket.on('concept_processing', (data) => {
  console.log('개념 정리 AI 생성 중:', data);
  // { chapter_id: 1, concept_id: 1, status: "processing", message: "..." }
});

socket.on('exercise_processing', (data) => {
  console.log('실습 과제 AI 생성 중:', data);
  // { chapter_id: 1, exercise_id: 1, status: "processing", message: "..." }
});

socket.on('quiz_processing', (data) => {
  console.log('퀴즈 AI 생성 중:', data);
  // { chapter_id: 1, quiz_count: 3, status: "processing", message: "..." }
});

// AI 생성 완료 알림들
socket.on('concept_completed', (data) => {
  console.log('개념 정리 완료:', data);
  // { chapter_id: 1, concept_id: 1, status: "completed", message: "..." }
});

socket.on('exercise_completed', (data) => {
  console.log('실습 과제 완료:', data);
  // { chapter_id: 1, exercise_id: 1, status: "completed", message: "..." }
});

socket.on('quiz_completed', (data) => {
  console.log('퀴즈 완료:', data);
  // { chapter_id: 1, quiz_count: 3, status: "completed", message: "..." }
});

socket.on('all_completed', (data) => {
  console.log('모든 콘텐츠 생성 완료:', data);
  // { chapter_id: 1, status: "all_completed", message: "..." }
});

// 4. 챕터 생성 API 호출
async function createChapter() {
  const response = await fetch('http://localhost:8000/v1/chapter/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      course_id: 1,
      title: '변수와 자료형',
      description: 'Python 기초',
      owner_id: 1
    })
  });

  const data = await response.json();
  console.log('챕터 ID:', data.chapter_id);
}
```

### React 예제

```jsx
import { useEffect, useState } from 'react';
import io from 'socket.io-client';

function ChapterPage() {
  const [socket, setSocket] = useState(null);
  const [chapterId, setChapterId] = useState(null);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const newSocket = io('http://localhost:8000');
    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log('Socket.IO 연결됨');
    });

    newSocket.on('chapter_processing_started', (data) => {
      setNotifications(prev => [...prev, `챕터 생성 시작: ${data.title}`]);
    });

    newSocket.on('concept_processing', (data) => {
      setNotifications(prev => [...prev, '개념 정리 AI 생성 중...']);
    });

    newSocket.on('concept_completed', (data) => {
      setNotifications(prev => [...prev, '✅ 개념 정리 완료']);
    });

    newSocket.on('exercise_processing', (data) => {
      setNotifications(prev => [...prev, '실습 과제 AI 생성 중...']);
    });

    newSocket.on('exercise_completed', (data) => {
      setNotifications(prev => [...prev, '✅ 실습 과제 완료']);
    });

    newSocket.on('quiz_processing', (data) => {
      setNotifications(prev => [...prev, `퀴즈 ${data.quiz_count}개 AI 생성 중...`]);
    });

    newSocket.on('quiz_completed', (data) => {
      setNotifications(prev => [...prev, `✅ 퀴즈 ${data.quiz_count}개 완료`]);
    });

    newSocket.on('all_completed', (data) => {
      setNotifications(prev => [...prev, '🎉 모든 콘텐츠 생성 완료!']);
    });

    return () => newSocket.close();
  }, []);

  const handleCreateChapter = async () => {
    const response = await fetch('http://localhost:8000/v1/chapter/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        course_id: 1,
        title: '변수와 자료형',
        description: 'Python 기초',
        owner_id: 1
      })
    });

    const data = await response.json();
    setChapterId(data.chapter_id);

    // 룸 참여
    socket.emit('join_chapter', { chapter_id: data.chapter_id });
  };

  return (
    <div>
      <button onClick={handleCreateChapter}>챕터 생성</button>
      <div>
        {notifications.map((msg, i) => (
          <div key={i}>{msg}</div>
        ))}
      </div>
    </div>
  );
}
```

---

## 📡 주요 이벤트

### 서버 → 클라이언트

| 이벤트 | 발생 시점 | 데이터 |
|--------|----------|--------|
| `connect` | 연결 성공 | - |
| `connection_established` | 연결 확인 | `{status: "connected"}` |
| `joined_chapter` | 룸 참여 성공 | `{chapter_id}` |
| `chapter_processing_started` | 챕터 생성 시작 (DB 저장 완료) | `{chapter_id, title, status, message}` |
| `concept_processing` | 개념 정리 AI 처리 시작 | `{chapter_id, concept_id, status, message}` |
| `exercise_processing` | 실습 과제 AI 처리 시작 | `{chapter_id, exercise_id, status, message}` |
| `quiz_processing` | 퀴즈 AI 처리 시작 | `{chapter_id, quiz_count, status, message}` |
| `concept_completed` | 개념 정리 생성 완료 | `{chapter_id, concept_id, status, message}` |
| `exercise_completed` | 실습 과제 생성 완료 | `{chapter_id, exercise_id, status, message}` |
| `quiz_completed` | 퀴즈 생성 완료 | `{chapter_id, quiz_count, status, message}` |
| `all_completed` | 모든 콘텐츠 생성 완료 | `{chapter_id, status, message}` |
| `progress_update` | 진행률 업데이트 (선택적) | `{chapter_id, progress, message}` |

### 클라이언트 → 서버

| 이벤트 | 용도 | 데이터 |
|--------|------|--------|
| `join_chapter` | 챕터 룸 참여 | `{chapter_id}` |
| `leave_chapter` | 챕터 룸 나가기 | `{chapter_id}` |

---

## 🧪 테스트

### HTML 클라이언트
```bash
open socket_client_example.html
```

1. "Join Chapter Room" 클릭 (Chapter ID: 1)
2. 다른 탭에서 챕터 생성 API 호출
3. 실시간 알림 확인

### cURL 테스트
```bash
# 챕터 생성
curl -X POST http://localhost:8000/v1/chapter/ \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "title": "테스트 챕터",
    "description": "설명",
    "owner_id": 1
  }'
```

---

## 🎯 장점

✅ **실시간 알림** - AI 처리 진행 상황을 실시간으로 알림
✅ **긴 대기 시간 대응** - Kafka → n8n → AI 처리가 오래 걸려도 클라이언트 연결 유지
✅ **양방향 통신** - WebSocket 사용
✅ **Room 기반** - 챕터별 독립적 알림
✅ **비동기 처리** - 클라이언트가 응답을 기다리지 않고 다른 작업 가능

---

## 🔧 커스터마이징

### 진행률 업데이트 추가
```python
# 백엔드에서
from socketio_manager import emit_progress_update

await emit_progress_update(chapter_id, 50, "개념 정리 생성 중...")
await emit_progress_update(chapter_id, 75, "실습 과제 생성 중...")
await emit_progress_update(chapter_id, 100, "완료!")
```

```javascript
// 프론트엔드에서
socket.on('progress_update', (data) => {
  console.log(`진행률: ${data.progress}% - ${data.message}`);
  // 프로그레스 바 업데이트
});
```

---

## 📝 파일 구조

```
backend/
├── socketio_manager.py           # Socket.IO 서버 및 이벤트
├── main.py                        # Socket.IO 통합
├── chapter.py                     # ✏️ 챕터 생성 시 알림 발송
├── socket_client_example.html    # 테스트 페이지
└── SOCKETIO_GUIDE.md              # 이 문서
```

---

## 🐛 트러블슈팅

### Socket.IO 연결 안 됨
- 서버가 `socket_app`으로 실행되는지 확인: `python main.py`
- CORS 설정 확인
- 브라우저 콘솔에서 WebSocket 연결 확인

### 이벤트 수신 안 됨
- `join_chapter`를 먼저 호출했는지 확인
- 올바른 chapter_id 사용 확인
- 서버 로그에서 이벤트 발송 확인

---

## 🔌 N8N Webhook 엔드포인트

n8n이 AI 생성 완료 후 호출할 webhook 엔드포인트:

### 1. 개념 정리 완료
```bash
POST /v1/chapter/{chapter_id}/concept-finish
Content-Type: application/json

{
  "title": "변수와 자료형 개념 정리",
  "content": "Python에서 변수는..."
}
```

### 2. 실습 과제 완료
```bash
POST /v1/chapter/{chapter_id}/exercise-finish
Content-Type: application/json

{
  "question": "다음 코드의 출력 결과는?",
  "answer": "정답 설명...",
  "difficulty": "easy"
}
```

### 3. 퀴즈 완료
```bash
POST /v1/chapter/{chapter_id}/quiz-finish
Content-Type: application/json

{
  "quizzes": [
    {
      "question": "Python에서 변수 선언 시 필요한 키워드는?",
      "correct_answer": "필요 없음",
      "options": ["var", "let", "필요 없음", "def"],
      "type": "multiple"
    },
    {
      "question": "...",
      "correct_answer": "...",
      "options": [...],
      "type": "multiple"
    },
    {
      "question": "...",
      "correct_answer": "...",
      "options": [...],
      "type": "multiple"
    }
  ]
}
```

## 📚 다음 단계

Socket.IO를 통해 AI 비동기 처리의 진행 상황을 실시간으로 클라이언트에 알려줄 수 있습니다.

추가 가능한 기능:
- Redis pub/sub (다중 서버 환경에서 Socket.IO 이벤트 동기화)
- 재시도 로직 (AI 생성 실패 시 자동 재시도)
- 타임아웃 처리 (일정 시간 내 응답 없으면 알림)

현재 구조로 Kafka → n8n → AI 처리의 긴 대기 시간에도 클라이언트가 안정적으로 대기할 수 있습니다! 🎉
