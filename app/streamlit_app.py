# app/streamlit_app.py

import streamlit as st

from coding_cards.storage import CardStorage
from coding_cards.models import QACard, CodingCard
from coding_cards.utils import generate_uuid

storage = CardStorage("data/cards.json")


def create_card_ui():
    st.header("Create a New Card")

    card_type = st.selectbox("Card Type", ["qa", "coding"])
    title = st.text_input("Title")
    concept = st.text_input("Concept / Topic")
    categories_raw = st.text_input("Categories (comma-separated)", "")
    difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
    important = st.checkbox("Important?")

    categories = [c.strip() for c in categories_raw.split(",") if c.strip()]

    if card_type == "qa":
        question = st.text_area("Question")
        answer = st.text_area("Answer")

        if st.button("Save Q/A Card"):
            card = QACard(
                id=generate_uuid(),
                title=title,
                concept=concept,
                categories=categories,
                difficulty=difficulty,
                important=important,
                card_type="qa",
                question=question,
                answer=answer,
            )
            cards = storage.load()
            cards.append(card)
            storage.save(cards)
            st.success("Q/A card saved!")

    else:
        starter_code = st.text_area("Starter Code")
        solution_code = st.text_area("Solution Code")

        if st.button("Save Coding Card"):
            card = CodingCard(
                id=generate_uuid(),
                title=title,
                concept=concept,
                categories=categories,
                difficulty=difficulty,
                important=important,
                card_type="coding",
                starter_code=starter_code,
                solution_code=solution_code,
                test_cases=[],  # we’ll add UI for this later
            )
            cards = storage.load()
            cards.append(card)
            storage.save(cards)
            st.success("Coding card saved!")


def list_cards_ui():
    st.header("Existing Cards")

    cards = storage.load()
    if not cards:
        st.info("No cards yet. Create one above!")
        return

    for card in cards:
        with st.expander(f"[{card.card_type.upper()}] {card.title}"):
            st.write(f"**Concept:** {card.concept}")
            st.write(f"**Categories:** {', '.join(card.categories)}")
            st.write(f"**Difficulty:** {card.difficulty}")
            st.write(f"**Important:** {card.important}")
            st.write(f"**Times Seen:** {card.times_seen}")
            st.write(f"**Success Rate:** {card.success_rate:.2f}")

            if isinstance(card, QACard):
                st.markdown("**Question:**")
                st.code(card.question, language="markdown")
                st.markdown("**Answer:**")
                st.code(card.answer, language="markdown")
            elif isinstance(card, CodingCard):
                st.markdown("**Starter Code:**")
                st.code(card.starter_code, language="python")
                st.markdown("**Solution Code:**")
                st.code(card.solution_code, language="python")


def main():
    st.title("Coding Cards – Phase 1")
    create_card_ui()
    st.markdown("---")
    list_cards_ui()


if __name__ == "__main__":
    main()
