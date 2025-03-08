# WGS84-converter
대한민국 좌표계를 위도, 경도로 변환
# 좌표변환 시스템 (WGS84-converter)

EPSG:5174(중부원점) 좌표를 EPSG:4326(WGS84) 좌표로 변환하는 웹 애플리케이션입니다.

## 기능

- 단일 좌표 변환: 개별 좌표 변환 및 지도 표시
- CSV/Excel 파일 변환: 파일 업로드를 통한 대량 좌표 변환
- 일괄 좌표 변환: 텍스트 입력을 통한 여러 좌표 동시 변환

## 사용 방법

1. 단일 좌표 변환
   - X, Y 좌표 입력 후 변환 버튼 클릭
   - 변환된 위도/경도 확인 및 지도 표시

2. CSV/Excel 파일 변환
   - 좌표 정보가 포함된 파일 업로드
   - X, Y 좌표 컬럼명 지정
   - 변환 결과 확인 및 CSV 다운로드

3. 일괄 좌표 변환
   - 여러 좌표를 텍스트 영역에 입력
   - 형식: 이름,X좌표,Y좌표 (줄바꿈으로 구분)
   - 변환 결과 확인 및 CSV 다운로드

## 기술 스택

- Streamlit: 웹 애플리케이션 프레임워크
- Pyproj: 좌표계 변환 라이브러리
- Pandas: 데이터 처리
- Streamlit Community Cloud: 호스팅 플랫폼

## 설치 및 실행 (로컬)

```bash
# 저장소 클론
git clone https://github.com/사용자명/WGS84-converter.git
cd WGS84-converter

# 필요 패키지 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

## 라이센스

MIT License