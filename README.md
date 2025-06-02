# auto-gmail-sender

# 📬 자동 이메일 전송기 (Auto Mail Sender)

Gmail API를 활용하여 CSV 파일에 정의된 수신자들에게 이메일을 첨부파일과 함께 자동으로 전송하는 파이썬 스크립트입니다.

---

## 🚀 주요 기능

- Gmail 계정을 통해 다수에게 자동 이메일 발송
- 수신자 이름을 반영한 개인화된 제목과 본문
- 첨부파일 복수 개 전송 지원 (CSV 파일에서 `;`로 구분)
- Gmail API OAuth 인증 처리

---

## 📁 프로젝트 구조

```
auto_mail_send/
├── sending.py # 메일 전송 메인 스크립트
├── recipients.csv # 수신자 정보 목록
├── .gitignore
├── README.md
└── files/ # 첨부파일 저장 폴더
```

---

## 🧑‍💻 사용 방법

### 1. Gmail API 사용 설정

- [Google Cloud Console](https://console.cloud.google.com/)에 접속하여 프로젝트 생성
- Gmail API 활성화
- OAuth 클라이언트 ID 생성 (데스크톱 앱)
- `credentials.json` 다운로드하여 프로젝트 루트에 저장

### 2. 테스트 사용자 등록

- OAuth 동의 화면 설정 → 대상 → 테스트 사용자로 본인 Gmail 주소 등록

---

### 3. CSV 파일 작성 예시 (`recipients.csv`)

- 복수개의 파일을 보낼때는 ";"로 구분
- 보낼 파일들은 프로젝트 루트 아래 files폴더 안에 있어야함

```csv
name,email,files
홍길동,hong@example.com,"files/intro.pdf;files/schedule.pdf"
김민지,kim@example.com,"files/notice.pdf"

```

---

### 4. 실행

```
python sending.py
```

- 처음 실행시 브라우저가 열리며 Google 로그인 필요
- 인증이 완료되면 token.json 파일이 생성됨

---

### 📌주의사항

- Gmail Api 사용량 제한: 하루 약 100~500 건
- 메일 1건당 첨부파일 용량은 총 25MB 이하로 제한됨
