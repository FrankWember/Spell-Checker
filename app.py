from flask import Flask, request, render_template, jsonify
import re

app = Flask(__name__)

MATCH = 0
CC_VV_MISMATCH = 1
VC_MISMATCH = 3
GAP = 2

def is_vowel(char):
    return char.lower() in "aeiou"

def sequence_alignment(word1, word2):
    n, m = len(word1), len(word2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i * GAP
    for j in range(1, m + 1):
        dp[0][j] = j * GAP
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + MATCH
            else:
                mismatch_penalty = CC_VV_MISMATCH if (is_vowel(word1[i - 1]) == is_vowel(word2[j - 1])) else VC_MISMATCH
                dp[i][j] = min(
                    dp[i - 1][j - 1] + mismatch_penalty,
                    dp[i - 1][j] + GAP,
                    dp[i][j - 1] + GAP
                )
    return dp[n][m]

def get_suggestions(word, dictionary):
    penalties = [(sequence_alignment(word, dict_word), dict_word) for dict_word in dictionary]
    penalties.sort(key=lambda x: (x[0], x[1]))
    return penalties[:10]

def load_dictionary(file_path):
    with open(file_path, "r") as file:
        words = file.read().split()
    cleaned_words = list(set([word.lower() for word in words if re.match(r"^[a-zA-Z]+$", word)]))
    return cleaned_words

dictionary = load_dictionary("dictionary.txt")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/suggestions", methods=["POST"])
def suggestions():
    word = request.json.get("word", "").lower()
    if word:
        suggestions = get_suggestions(word, dictionary)
        return jsonify(suggestions=[{"word": s[1], "penalty": s[0]} for s in suggestions])
    return jsonify(suggestions=[])

if __name__ == "__main__":
    app.run(debug=True)
