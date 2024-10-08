document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('sendButton');
    const messageInput = document.getElementById('messageInput');
    const messagesContainer = document.getElementById('messages');

    // Sample messages (you can replace this with actual message fetching logic)
    const messages = [
        { text: 'Hello!', sender: 'User' },
        { text: 'Hi there!', sender: 'Bot' },
    ];

    // Function to display messages
    function displayMessages() {
        messagesContainer.innerHTML = ''; // Clear existing messages
        messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.textContent = `${message.sender}: ${message.text}`;
            messagesContainer.appendChild(messageElement);
        });
        messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll to the bottom
    }

    // Function to send a message
    sendButton.addEventListener('click', () => {
        const messageText = messageInput.value.trim();
        if (messageText) {
            messages.push({ text: messageText, sender: 'User' }); // Add user message
            messageInput.value = ''; // Clear input
            displayMessages(); // Update message display
        }
    });

    // Initial display of messages
    displayMessages();
});