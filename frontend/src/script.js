document.getElementById("send-button").addEventListener("click", async () => {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    // Display user query in chat box
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div>User: ${userInput}</div>`;

    // Send query to backend
    const response = await fetch("http://localhost:8080/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: userInput }),
    });

    const data = await response.json();
    chatBox.innerHTML += `<div>Bot: ${data.message}</div>`;
    document.getElementById("user-input").value = ""; // Clear input
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
});