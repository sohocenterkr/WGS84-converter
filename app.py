import streamlit as st
import pandas as pd
from pyproj import Transformer
import io

st.title('좌표 변환 시스템')
st.subheader('EPSG:5174 → EPSG:4326(WGS84) 변환기')

# 좌표 변환 함수
def transform_5174_to_wgs84(x, y):
    transformer = Transformer.from_crs("EPSG:5174", "EPSG:4326", always_xy=True)
    lng, lat = transformer.transform(x, y)
    return lat, lng  # 위도, 경도 순으로 반환

# 사이드바 - 변환 방식 선택
conversion_type = st.sidebar.radio(
    "변환 방식 선택",
    ["단일 좌표 변환", "CSV/Excel 파일 변환", "일괄 좌표 변환"]
)

# 단일 좌표 변환
if conversion_type == "단일 좌표 변환":
    st.header("단일 좌표 변환")
    
    col1, col2 = st.columns(2)
    with col1:
        x_coord = st.number_input("X 좌표 (EPSG:5174)", value=200000.0)
    with col2:
        y_coord = st.number_input("Y 좌표 (EPSG:5174)", value=500000.0)
    
    if st.button("변환"):
        try:
            lat, lng = transform_5174_to_wgs84(x_coord, y_coord)
            st.success("변환 성공!")
            st.write(f"위도(WGS84): {round(lat, 6)}")
            st.write(f"경도(WGS84): {round(lng, 6)}")
            
            # 지도에 표시 (선택사항)
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lng]}))
        except Exception as e:
            st.error(f"변환 오류: {e}")

# CSV/Excel 파일 변환
elif conversion_type == "CSV/Excel 파일 변환":
    st.header("파일 업로드 및 변환")
    
    uploaded_file = st.file_uploader("CSV 또는 Excel 파일 업로드", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        x_col = st.text_input("X 좌표 컬럼명", "좌표정보X")
        y_col = st.text_input("Y 좌표 컬럼명", "좌표정보Y")
        
        if st.button("파일 변환"):
            try:
                # 파일 형식에 따라 읽기
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # 좌표 컬럼 확인
                if x_col not in df.columns or y_col not in df.columns:
                    st.error(f"파일에 {x_col} 또는 {y_col} 컬럼이 없습니다.")
                else:
                    # 좌표 변환 적용
                    results = []
                    for idx, row in df.iterrows():
                        try:
                            lat, lng = transform_5174_to_wgs84(row[x_col], row[y_col])
                            
                            # 원본 행 복사
                            result_row = row.to_dict()
                            
                            # 변환된 좌표 추가
                            result_row['위도(WGS84)'] = round(lat, 6)
                            result_row['경도(WGS84)'] = round(lng, 6)
                            
                            results.append(result_row)
                        except Exception as e:
                            st.warning(f"{idx+1}번 행 변환 실패: {e}")
                    
                    # 결과 데이터프레임 생성
                    if results:
                        result_df = pd.DataFrame(results)
                        
                        st.success(f"변환 완료! 총 {len(results)}개 행 처리됨")
                        st.dataframe(result_df)
                        
                        # CSV 다운로드 버튼
                        csv = result_df.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="CSV 파일 다운로드",
                            data=csv,
                            file_name="변환결과.csv",
                            mime="text/csv",
                        )
                    else:
                        st.error("변환 가능한 좌표가 없습니다.")
            except Exception as e:
                st.error(f"파일 처리 중 오류 발생: {e}")

# 일괄 좌표 변환
else:
    st.header("일괄 좌표 변환")
    
    sample_text = """가쿠니 식당,208417.6428,453882.7854
꼬숩다 누룽지 닭죽 상봉점,207683.1458,455292.3352
빅스타피자 중랑구점,207909.6018,454643.2744"""
    
    coordinates_text = st.text_area(
        "좌표 목록 입력 (이름,X좌표,Y좌표 형식, 줄바꿈으로 구분)",
        value=sample_text,
        height=200
    )
    
    if st.button("일괄 변환"):
        if not coordinates_text.strip():
            st.error("변환할 좌표를 입력해주세요.")
        else:
            lines = coordinates_text.strip().split('\n')
            results = []
            
            for line in lines:
                parts = line.split(',')
                if len(parts) >= 3:
                    try:
                        name = parts[0].strip()
                        x = float(parts[1].strip())
                        y = float(parts[2].strip())
                        
                        lat, lng = transform_5174_to_wgs84(x, y)
                        
                        results.append({
                            "이름": name,
                            "X좌표(EPSG:5174)": x,
                            "Y좌표(EPSG:5174)": y,
                            "위도(WGS84)": round(lat, 6),
                            "경도(WGS84)": round(lng, 6)
                        })
                    except Exception as e:
                        st.warning(f"'{line}' 변환 실패: {e}")
            
            if results:
                result_df = pd.DataFrame(results)
                st.success(f"변환 완료! 총 {len(results)}개 좌표 처리됨")
                st.dataframe(result_df)
                
                # CSV 다운로드 버튼
                csv = result_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="CSV 파일 다운로드",
                    data=csv,
                    file_name="변환결과.csv",
                    mime="text/csv",
                )
            else:
                st.error("변환 가능한 좌표가 없습니다.")

# 푸터
st.markdown("---")
st.caption("© 2025 좌표변환 시스템 | EPSG:5174(중부원점) → EPSG:4326(WGS84)")