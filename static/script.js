const inputField = document.getElementById("word-input");
const suggestionsList = document.getElementById("suggestions-list");

inputField.addEventListener("input", async () => {
    const query = inputField.value.trim();

    if (!query) {
        suggestionsList.innerHTML = "";
        return;
    }

    const response = await fetch("/suggestions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ word: query }),
    });

    const data = await response.json();
    const suggestions = data.suggestions;

    suggestionsList.innerHTML = suggestions.length
        ? suggestions
              .map(
                  (s) =>
                      `<li><strong>${s.word}</strong> <span>(Penalty: ${s.penalty})</span></li>`
              )
              .join("")
        : `<li>No suggestions found.</li>`;
});
