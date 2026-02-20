import streamlit as st
import json

# Load questions from JSON file
def load_questions(filename="questions.json"):
    with open(filename, "r") as f:
        return json.load(f)

# Main app
def main():
    st.title("Multiple Choice Quiz")
    st.write("Answer the questions and see your score at the end!")

    # Load questions
    questions = load_questions()
    if not questions:
        st.error("No questions found in questions.json")
        return

    # Initialize session state for score and current question
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []

    current_q = st.session_state.current_question
    total_questions = len(questions)

    if current_q < total_questions:
        q = questions[current_q]
        st.subheader(f"Question {current_q + 1} of {total_questions}")
        st.write(q["question"])

        # Radio button for options
        selected_option = st.radio("Choose an answer:", q["options"], key=f"q_{current_q}")

        # Submit button
        if st.button("Submit Answer"):
            st.session_state.answers.append(selected_option)
            if selected_option == q["answer"]:
                st.session_state.score += 1
            st.session_state.current_question += 1
            st.rerun()  # Refresh to next question
    else:
        # Quiz complete
        st.subheader("Quiz Complete!")
        st.write(f"Your score: {st.session_state.score} out of {total_questions}")
        st.write("Review your answers:")
        for i, (q, ans) in enumerate(zip(questions, st.session_state.answers)):
            status = "Correct" if ans == q["answer"] else f"Incorrect (Correct: {q['answer']})"
            st.write(f"Q{i+1}: {q['question']} - Your answer: {ans} - {status}")

        # Reset button
        if st.button("Restart Quiz"):
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.rerun()

if __name__ == "__main__":
    main()