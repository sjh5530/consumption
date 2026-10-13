"""소비 MBTI 성향 탐색기 — Streamlit 앱

실행:
    pip install streamlit
    streamlit run streamlit_consumption_mbti.py

사이다경제의 소비 MBTI 콘텐츠에서 소개한 네 가지 축
(E/G: 돈 관리, R/I: 소비 일관성, F/S: 소비 패턴, Q/D: 여가 패턴)을
참고해 새로 구성한 비공식 자기성찰용 미니 테스트입니다.
원문 문항·점수표를 복제하지 않으며, 재무 진단이나 공식 심리검사가 아닙니다.
"""

import streamlit as st

st.set_page_config(
    page_title="소비 MBTI 성향 탐색기",
    page_icon="💸",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 850px; padding-top: 2.2rem; padding-bottom: 3rem;}
    div[data-testid="stButton"] button {
        border-radius: 14px; min-height: 84px; white-space: normal;
        text-align: left; line-height: 1.5; padding: 16px;
    }
    .hero {
        padding: 1.25rem 1.4rem; border-radius: 18px;
        background: linear-gradient(120deg, #eef2ff, #fdf2f8);
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 콘텐츠에서 다루는 네 축을 바탕으로 문항을 새로 작성했습니다.
# 각 문항은 두 성향 중 현재 자신에게 더 가까운 쪽을 고르게 합니다.
AXES = [
    {
        "id": "EG",
        "name": "돈 관리 성향",
        "letters": ("E", "G"),
        "labels": ("경제적·관리형", "자유로운·관대한형"),
        "description": {
            "E": "예산과 잔액을 확인하고, 지출을 계획적으로 관리하려는 편입니다.",
            "G": "돈을 세세하게 통제하기보다 필요와 만족을 고려해 유연하게 쓰는 편입니다.",
        },
    },
    {
        "id": "RI",
        "name": "소비 일관성",
        "letters": ("R", "I"),
        "labels": ("일관형", "변동형"),
        "description": {
            "R": "월별 지출 흐름이 비교적 일정하고, 소비 기준을 유지하려는 편입니다.",
            "I": "일정이나 기분, 특별한 상황에 따라 지출 규모가 달라지는 편입니다.",
        },
    },
    {
        "id": "FS",
        "name": "소비 패턴",
        "letters": ("F", "S"),
        "labels": ("푸드·문화형", "쇼핑형"),
        "description": {
            "F": "외식, 카페, 공연, 영화 등 경험과 문화생활에 가치를 두는 편입니다.",
            "S": "옷, 소품, 전자제품 등 물건을 탐색하고 구매하는 데 흥미를 느끼는 편입니다.",
        },
    },
    {
        "id": "QD",
        "name": "여가 패턴",
        "letters": ("Q", "D"),
        "labels": ("정적인 여가형", "활동적인 여가형"),
        "description": {
            "Q": "집에서 쉬거나 혼자 즐기는 차분한 활동에서 만족을 얻는 편입니다.",
            "D": "여행, 운동, 모임처럼 밖에서 움직이고 사람들과 어울리는 활동을 즐기는 편입니다.",
        },
    },
]

QUESTIONS = [
    # E / G
    {"axis": "EG", "prompt": "월급이나 수입이 들어오면 가장 먼저 하는 행동은?", "options": [
        ("E", "예산과 저축할 금액을 정하고 남은 돈을 쓴다"),
        ("G", "당장 필요한 지출을 하고 상황에 맞춰 돈을 관리한다"),
    ]},
    {"axis": "EG", "prompt": "물건을 사기 전, 나는 보통?", "options": [
        ("E", "가격과 할인, 예산을 비교해 구매 여부를 결정한다"),
        ("G", "필요하거나 마음에 들면 가격 비교에 많은 시간을 쓰지 않는다"),
    ]},
    {"axis": "EG", "prompt": "통장 잔액과 카드 사용 내역은?", "options": [
        ("E", "정기적으로 확인해 지출 흐름을 파악한다"),
        ("G", "필요할 때 확인하는 편이고 매번 점검하지는 않는다"),
    ]},
    # R / I
    {"axis": "RI", "prompt": "평소 한 달 지출 규모는 어떤 편인가요?", "options": [
        ("R", "큰 변수가 없다면 매달 비슷한 수준을 유지한다"),
        ("I", "약속이나 기분, 일정에 따라 달마다 차이가 큰 편이다"),
    ]},
    {"axis": "RI", "prompt": "여행이나 기념일처럼 특별한 일이 생기면?", "options": [
        ("R", "평소 예산 안에서 미리 비용을 마련해 둔다"),
        ("I", "평소보다 지출이 늘어도 그때그때 결정하는 편이다"),
    ]},
    {"axis": "RI", "prompt": "예상보다 지출이 많았던 달의 다음 달에는?", "options": [
        ("R", "지출을 조정해 원래의 소비 흐름으로 돌아가려 한다"),
        ("I", "다음 달에도 상황에 따라 소비 규모가 달라질 수 있다"),
    ]},
    # F / S
    {"axis": "FS", "prompt": "여유 자금이 생겼을 때 더 끌리는 사용처는?", "options": [
        ("F", "맛있는 음식, 카페, 공연이나 전시 같은 경험"),
        ("S", "옷, 취미용품, 생활 소품 등 갖고 싶은 물건"),
    ]},
    {"axis": "FS", "prompt": "주말에 돈을 쓰며 즐기고 싶은 활동은?", "options": [
        ("F", "새로운 식당을 가거나 영화·공연·전시를 즐긴다"),
        ("S", "쇼핑몰이나 온라인몰을 둘러보며 필요한 물건을 찾는다"),
    ]},
    {"axis": "FS", "prompt": "소비 후 가장 만족감이 오래가는 것은?", "options": [
        ("F", "좋은 장소에서 보낸 시간이나 사람들과의 추억"),
        ("S", "오래 찾던 물건을 구매했거나 마음에 드는 제품을 발견한 일"),
    ]},
    # Q / D
    {"axis": "QD", "prompt": "휴일에 가장 회복이 잘 되는 방식은?", "options": [
        ("Q", "집에서 쉬거나 독서·영상 등 차분한 활동을 한다"),
        ("D", "외출하거나 운동·여행·모임 등 활동적인 일정을 보낸다"),
    ]},
    {"axis": "QD", "prompt": "여가 계획을 세울 때 더 마음에 드는 것은?", "options": [
        ("Q", "이동이 적고 여유롭게 쉴 수 있는 일정"),
        ("D", "새로운 장소와 활동을 여러 가지 경험하는 일정"),
    ]},
    {"axis": "QD", "prompt": "스트레스를 풀기 위해 더 자주 선택하는 것은?", "options": [
        ("Q", "혼자만의 시간이나 가까운 사람과의 조용한 시간"),
        ("D", "사람들과 만나거나 밖에서 몸을 움직이는 활동"),
    ]},
]

TYPE_SUMMARIES = {
    "ERFQ": "계획적으로 돈을 관리하고 지출 흐름을 일정하게 유지하며, 경험과 차분한 여가를 선호하는 경향입니다.",
    "ERFD": "계획적인 관리와 일정한 소비를 바탕으로, 문화·미식 경험과 활동적인 여가를 함께 즐기는 경향입니다.",
    "ERSQ": "예산과 소비 기준을 중시하고, 물건을 구매하는 즐거움과 조용한 휴식을 선호하는 경향입니다.",
    "ERSD": "돈 관리와 소비 흐름을 체계적으로 유지하면서 쇼핑과 외부 활동을 즐기는 경향입니다.",
    "EIFQ": "돈을 꼼꼼히 관리하려 하지만 상황에 따라 지출이 달라질 수 있으며, 경험과 휴식을 중시하는 경향입니다.",
    "EIFD": "예산을 의식하면서도 특별한 경험에 유연하게 지출하고, 활동적인 여가를 즐기는 경향입니다.",
    "EISQ": "돈을 관리하려는 의식은 강하지만 지출은 상황에 따라 달라질 수 있으며, 쇼핑과 휴식을 선호하는 경향입니다.",
    "EISD": "예산을 확인하면서 필요에 따라 소비하고, 쇼핑과 다양한 외부 활동을 즐기는 경향입니다.",
    "GRFQ": "돈을 지나치게 통제하기보다 유연하게 다루면서 비교적 일정한 소비를 하고, 경험과 휴식을 선호하는 경향입니다.",
    "GRFD": "돈을 유연하게 관리하고 소비 흐름은 비교적 일정하게 유지하며, 경험과 활동적인 여가를 즐기는 경향입니다.",
    "GRSQ": "돈을 자유롭게 쓰는 편이지만 소비 흐름은 비교적 일정하고, 물건 구매와 조용한 여가를 선호하는 경향입니다.",
    "GRSD": "돈을 유연하게 관리하고 일정한 소비 흐름을 보이며, 쇼핑과 활동적인 여가를 즐기는 경향입니다.",
    "GIFQ": "돈 관리 방식과 지출 규모가 상황에 따라 달라질 수 있으며, 경험과 차분한 여가를 선호하는 경향입니다.",
    "GIFD": "상황에 따라 유연하게 소비하고, 음식·문화 경험과 활동적인 여가를 즐기는 경향입니다.",
    "GISQ": "지출이 상황에 따라 달라지는 편이며, 물건을 구매하는 즐거움과 조용한 여가를 선호하는 경향입니다.",
    "GISD": "상황에 맞춰 유연하게 소비하며, 쇼핑과 여행·모임 같은 활동적인 여가를 즐기는 경향입니다.",
}


def initialize_state():
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "completed" not in st.session_state:
        st.session_state.completed = False


def restart_test():
    st.session_state.answers = {}
    st.session_state.current_index = 0
    st.session_state.completed = False


def calculate_result():
    result_letters = []
    axis_results = []
    for axis in AXES:
        axis_questions = [q for q in QUESTIONS if q["axis"] == axis["id"]]
        counts = {letter: 0 for letter in axis["letters"]}
        for index, question in enumerate(QUESTIONS):
            if question["axis"] == axis["id"] and index in st.session_state.answers:
                counts[st.session_state.answers[index]] += 1
        first, second = axis["letters"]
        winner = first if counts[first] >= counts[second] else second
        result_letters.append(winner)
        axis_results.append({
            "axis": axis,
            "winner": winner,
            "count": counts[winner],
            "total": len(axis_questions),
        })
    return "".join(result_letters), axis_results


def show_results():
    result_type, axis_results = calculate_result()
    st.success("테스트를 완료했어요!")
    st.markdown(f"## 나의 소비 MBTI는 **{result_type}**")
    st.write(TYPE_SUMMARIES.get(result_type, "나의 소비와 여가에서 나타나는 경향을 확인해 보세요."))
    st.caption("이 결과는 답변을 요약한 참고용 콘텐츠이며, 부자가 될 가능성이나 재무 건전성을 예측하지 않습니다.")

    st.divider()
    st.subheader("네 가지 성향 살펴보기")
    for item in axis_results:
        axis = item["axis"]
        letter = item["winner"]
        label = axis["labels"][axis["letters"].index(letter)]
        st.markdown(f"### {axis['name']} · {letter} ({label})")
        st.write(axis["description"][letter])
        st.progress(item["count"] / item["total"], text=f"이번 축에서 {item['count']}/{item['total']}개 문항 선택")

    st.info("소비 성향에는 정답이나 우열이 없습니다. 소득, 생활 환경, 목표에 따라 적절한 돈 관리 방식은 달라질 수 있어요.")
    if st.button("🔄 다시 테스트하기", use_container_width=True, type="primary"):
        restart_test()
        st.rerun()


initialize_state()

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.title("💸 소비 MBTI 성향 탐색기")
st.write("돈 관리, 소비 습관, 소비 패턴, 여가 스타일을 가볍게 살펴보세요.")
st.markdown("</div>", unsafe_allow_html=True)
st.caption("총 12문항 · 4가지 성향 축 · 정답 없음")

if st.session_state.completed:
    show_results()
else:
    idx = st.session_state.current_index
    question = QUESTIONS[idx]
    answered = len(st.session_state.answers)
    st.progress(answered / len(QUESTIONS), text=f"응답 진행률 · {answered}/{len(QUESTIONS)}")
    axis = next(a for a in AXES if a["id"] == question["axis"])
    st.caption(f"문항 {idx + 1} / {len(QUESTIONS)} · {axis['name']} ({axis['letters'][0]} / {axis['letters'][1]})")
    st.subheader(question["prompt"])
    st.write("두 선택지 중 현재 나에게 더 가까운 쪽을 선택하세요.")

    cols = st.columns(2, gap="medium")
    for option_index, (letter, option_text) in enumerate(question["options"]):
        selected = st.session_state.answers.get(idx) == letter
        with cols[option_index]:
            st.markdown(f"**선택지 {chr(65 + option_index)}**")
            if st.button(
                f"{'✓ 선택됨 · ' if selected else ''}{option_text}",
                key=f"answer_{idx}_{option_index}",
                type="primary" if selected else "secondary",
                use_container_width=True,
            ):
                st.session_state.answers[idx] = letter
                st.rerun()

    st.divider()
    prev_col, next_col = st.columns(2)
    with prev_col:
        previous = st.button("← 이전", disabled=idx == 0, use_container_width=True)
    with next_col:
        last = idx == len(QUESTIONS) - 1
        next_button = st.button(
            "결과 보기 ✨" if last else "다음 →",
            disabled=idx not in st.session_state.answers,
            type="primary",
            use_container_width=True,
        )

    if previous:
        st.session_state.current_index -= 1
        st.rerun()
    if next_button:
        if last:
            st.session_state.completed = True
        else:
            st.session_state.current_index += 1
        st.rerun()

    if idx not in st.session_state.answers:
        st.caption("다음 문항으로 이동하려면 선택지를 먼저 골라주세요.")

    st.markdown("---")
    if st.button("처음부터 다시 시작", use_container_width=True):
        restart_test()
        st.rerun()

st.markdown("---")
st.caption("참고: 사이다경제 「소비 MBTI 부자가 될 유형은? 4가지 성향 테스트」의 네 가지 축을 참고해 새롭게 구성했습니다.")
st.caption("출처 콘텐츠: https://cidermics.com/contents/detail/2928")
