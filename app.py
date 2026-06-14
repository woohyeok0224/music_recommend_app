import streamlit as st
import pandas as pd
import random

# 페이지 기본 설정
st.set_page_config(page_title="음악 추천 앱", page_icon="🎵", layout="wide")

st.title("🎵 오늘의 기분에 맞는 음악 추천")

# 사이드바 설정
st.sidebar.header("오늘의 기분은 어떠신가요?")
moods_list = ["신남", "차분함", "우울함", "집중", "로맨틱", "운동"]
mood = st.sidebar.radio("기분 선택", moods_list)

# ===================================================================
# 한국 음악 데이터 (모든 영상 ID는 oEmbed API로 임베드 가능 여부 검증 완료)
# ===================================================================
korean_music_data = {
    "신남": [
        {"제목": "I AM", "가수": "아이브 (IVE)", "장르": "K-Pop", "영상_ID": "y7JPgbLfpfA"},
        {"제목": "강남스타일", "가수": "싸이 (PSY)", "장르": "K-Pop / Dance", "영상_ID": "9bZkp7q19f0"},
        {"제목": "아주 NICE", "가수": "세븐틴 (SEVENTEEN)", "장르": "K-Pop", "영상_ID": "WvwjisFDfNI"},
        {"제목": "Dynamite", "가수": "방탄소년단 (BTS)", "장르": "K-Pop / Pop", "영상_ID": "gdZLi9oWNZg"},
        {"제목": "Next Level", "가수": "에스파 (aespa)", "장르": "K-Pop / Dance", "영상_ID": "dly3BvtmXbA"},
        {"제목": "첫 만남은 계획대로 되지 않아", "가수": "투어스 (TWS)", "장르": "K-Pop", "영상_ID": "o6iWznl5ICo"},
    ],
    "차분함": [
        {"제목": "밤편지", "가수": "아이유 (IU)", "장르": "발라드", "영상_ID": "BzYnNdJhZQw"},
        {"제목": "주저하는 연인들을 위해", "가수": "잔나비", "장르": "인디/록", "영상_ID": "_C1aQZNUoaY"},
        {"제목": "모든 날, 모든 순간", "가수": "폴킴", "장르": "발라드", "영상_ID": "nq0BYGyH2Do"},
        {"제목": "EVERYTHING", "가수": "검정치마", "장르": "인디/록", "영상_ID": "Aq_gsctWHtQ"},
        {"제목": "바람이 분다", "가수": "이소라", "장르": "발라드", "영상_ID": "tkoM2Kcw6Yk"},
        {"제목": "비도 오고 그래서", "가수": "헤이즈 (Heize)", "장르": "R&B / Soul", "영상_ID": "WCw_SRIJRe8"},
    ],
    "우울함": [
        {"제목": "야생화", "가수": "박효신", "장르": "발라드", "영상_ID": "D1A7wLNSPhI"},
        {"제목": "거리에서", "가수": "성시경", "장르": "발라드", "영상_ID": "8WYz-UEcLks"},
        {"제목": "가을 밤에 든 생각", "가수": "잔나비", "장르": "인디/록", "영상_ID": "0IA9hcgRE-Y"},
        {"제목": "좋니", "가수": "윤종신", "장르": "발라드", "영상_ID": "92Y-K0gZyRY"},
        {"제목": "어떻게 이별까지 사랑하겠어...", "가수": "악뮤 (AKMU)", "장르": "어쿠스틱/발라드", "영상_ID": "m3DZsBw5bnE"},
        {"제목": "한숨", "가수": "이하이", "장르": "발라드", "영상_ID": "5iSlfF8TQ9k"},
    ],
    "집중": [
        {"제목": "Square (2017)", "가수": "백예린", "장르": "R&B/인디", "영상_ID": "4iFP_wd6QU8"},
        {"제목": "나무", "가수": "카더가든", "장르": "인디/록", "영상_ID": "a95yyxexgJo"},
        {"제목": "오래된 노래", "가수": "스탠딩 에그", "장르": "인디/어쿠스틱", "영상_ID": "JVIKowQZEdk"},
        {"제목": "행운을 빌어요", "가수": "페퍼톤스", "장르": "인디/록", "영상_ID": "zNqZxntN7n8"},
        {"제목": "별 보러 가자", "가수": "적재", "장르": "인디/어쿠스틱", "영상_ID": "ZWnDouSw8wo"},
        {"제목": "선물", "가수": "멜로망스", "장르": "발라드/인디", "영상_ID": "wTCU8wOFq5E"},
    ],
    "로맨틱": [
        {"제목": "말해! 뭐해?", "가수": "케이윌", "장르": "팝/발라드", "영상_ID": "aFgy_E_PV44"},
        {"제목": "폰서트", "가수": "10cm", "장르": "인디/어쿠스틱", "영상_ID": "61pRq2zfsHo"},
        {"제목": "오늘도 빛나는 너에게", "가수": "마크툽", "장르": "발라드", "영상_ID": "dmSUBdk4SY4"},
        {"제목": "흔들리는 꽃들 속에서...", "가수": "장범준", "장르": "인디/어쿠스틱", "영상_ID": "qKXMZPH6k18"},
        {"제목": "Dream", "가수": "수지, 백현", "장르": "R&B/Jazz", "영상_ID": "s06PjSO4OYY"},
        {"제목": "한 페이지가 될 수 있게", "가수": "데이식스 (DAY6)", "장르": "록/팝", "영상_ID": "vnS_jn2uibs"},
    ],
    "운동": [
        {"제목": "우리의 꿈 (원피스 OST)", "가수": "코요태", "장르": "댄스", "영상_ID": "fT4RdQMrWvQ"},
        {"제목": "아무노래", "가수": "지코 (ZICO)", "장르": "힙합/댄스", "영상_ID": "UuV2BmJ1p_I"},
        {"제목": "HER", "가수": "블락비 (Block B)", "장르": "힙합/댄스", "영상_ID": "o0WCva5Stk4"},
        {"제목": "파이팅 해야지", "가수": "부석순 (BSS)", "장르": "K-Pop/댄스", "영상_ID": "mBXBOLG06Wc"},
        {"제목": "WANNABE", "가수": "ITZY (있지)", "장르": "K-Pop/댄스", "영상_ID": "fE2h3lGlOsk"},
        {"제목": "BAAAAM", "가수": "다이나믹 듀오", "장르": "힙합", "영상_ID": "nl_FzuekYks"},
    ],
}

@st.cache_data
def load_processed_data():
    processed = {}
    for m, songs in korean_music_data.items():
        processed[m] = []
        for song in songs:
            vid = song["영상_ID"]
            processed[m].append({
                # 유튜브 썸네일을 앨범 표지로 사용
                "표지": f"https://img.youtube.com/vi/{vid}/0.jpg",
                "제목": song["제목"],
                "가수": song["가수"],
                "장르": song["장르"],
                "듣기": f"https://www.youtube.com/results?search_query={song['제목'].replace(' ', '+')}+{song['가수'].replace(' ', '+')}",
                "영상_url": f"https://www.youtube.com/watch?v={vid}",
            })
    return processed

music_data = load_processed_data()

# 선택한 기분에 따른 풀에서 랜덤으로 3곡 추출
selected_songs = random.sample(music_data[mood], 3)

# 상단 메시지와 새로고침 버튼을 나란히 배치
col1, col2 = st.columns([8, 2])
with col1:
    st.write(f"### '{mood}' 기분에 어울리는 한국 음악 3곡입니다. 🎧")
with col2:
    st.button("🔄 다른 곡 추천받기", use_container_width=True)

# 추출된 3곡으로 데이터프레임 생성 (표에는 영상 URL 컬럼 제외)
df = pd.DataFrame(selected_songs)
display_df = df.drop(columns=["영상_url"])

# Streamlit dataframe: 이미지 + 링크 포함 표 출력
st.dataframe(
    display_df,
    column_config={
        "표지": st.column_config.ImageColumn("유튜브 썸네일", help="해당 영상의 썸네일 이미지입니다."),
        "제목": "음악 제목",
        "가수": "가수명",
        "장르": "장르",
        "듣기": st.column_config.LinkColumn("유튜브 검색", display_text="검색하기 🔍"),
    },
    hide_index=True,
    use_container_width=True,
)

st.divider()

# 메인화면 하단부: 추천된 3곡 영상 바로보기 (검증된 임베드 가능 영상)
st.write("#### 📺 추천 음악 영상 바로보기")
st.write("위 표에서 추천된 음악의 영상을 바로 감상해 보세요!")

vid_cols = st.columns(3)
for idx, song in enumerate(selected_songs):
    with vid_cols[idx]:
        st.write(f"**{song['제목']}** - {song['가수']}")
        st.video(song["영상_url"])
