
import streamlit as st
import pandas as pd
import random
import random  # Select random words
import nltk
from nltk.corpus import brown  # Word corpus

st.title('Wordle clone')
st.write("Built by [Johnathan Fernandes](johnathanfernandes.github.io/)")

st.write("Slide Word size to choose the number of letters")
st.write("Slide Number of attempts to choose the number of tries you get")
st.write("The answer is tied to game_code, so if you use the same code as a friend, you'll both be guessing the same answer. Type in RANDOM to get a random word.")

nltk.download("brown")

word_size = st.slider("Word size", 4, 12, 5)
number_attempts = st.slider("Number of attempts", 3, 8, 6)
game_code = st.text_input("Game code", "HELLO THERE")

if "number_attempts" not in st.session_state:
    st.session_state.number_attempts = number_attempts
if "total_results" not in st.session_state:
    st.session_state.total_results = []
if "guess" not in st.session_state:
    st.session_state.guess = ""

if game_code == "RANDOM":
    pass
else:
    random.seed(a=game_code, version=2)

word_list = [
    word.lower() for word in brown.words() if len(word) == word_size and word.isalpha()
]
answer = random.choice(word_list)

left, right = st.columns(2)

with right:
    if st.session_state.number_attempts >= 0:
        st.session_state.number_attempts -= 1

        st.info(f"{st.session_state.number_attempts+1} attempts remaining")
        st.session_state.guess = st.text_input("Guess here", "")
        st.session_state.guess = str(
            st.session_state.guess
        ).lower()  # Convert to lowercase to check
        if len(st.session_state.guess) < word_size:  # If the word is too small
            st.error("Too few letters")
        elif len(st.session_state.guess) > word_size:
            st.error("Too many letters")
        elif st.session_state.guess not in word_list:  # If the word isn't a word
            st.error(
                "Word not in dictionary. Check [here](http://icame.uib.no/brown/bcm.html) for this game's list of legal words"
            )
        elif st.session_state.guess == answer:
            st.session_state.number_attempts = -1
            st.text("A winner is you")
        else:
            try:
                st.session_state.total_results.append(
                    list(st.session_state.guess.upper())
                )  # Add this result to the list of all results
            except AttributeError:
                pass

    with left:
        df = pd.DataFrame(st.session_state.total_results)
        style = df.style.applymap(
            lambda x: "height: 100px; width: 100px; text-align: center; font-size: 40px;"
        )
        style = style.applymap(
            lambda x: "background-color: orange"
            if x.lower() in list(answer)
            else "background-color: black"
        )
        # style = style.applymap(lambda x: "background-color: blue" if x.lower() == answer[st.session_state.guess.index(str(x.lower()))] else "background-color: black")

        style = style.hide(axis=0)
        style = style.hide(axis=1)

        st.write(style.to_html(), unsafe_allow_html=True)

        if st.session_state.number_attempts < 0:
            st.text(f"The word was {answer}")
