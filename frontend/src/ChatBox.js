import React, { useState } from 'react';
import './styles.css'; // Import your styles
import axios from 'axios'; // Import axios for making HTTP requests

const ChatBox = () => {
    const [messages, setMessages] = useState([]); // State to hold chat messages
    const [input, setInput] = useState(''); // State for the input field

    const handleSend = async () => {
        if (input.trim()) {
            const userMessage = { message: input };
            setMessages([...messages, { text: input, sender: 'user' }]); // Add user message
            setInput(''); // Clear input field

            try {
                // Send the message to the backend
                const response = await axios.post('http://localhost:8080/chat', userMessage);
                // Add the bot's response to the messages
                console.log(response.data)
                setMessages(prevMessages => [
                    ...prevMessages,
                    { text: response.data.status +" : "+ response.data.message, sender: 'bot' }
                ]);
    
            } catch (error) {
                console.error('Error sending message:', error);
            }
        }
    };

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default behavior (like a new line)
            handleSend(); // Call the send message function
        }
    };

    return (
        <div className="chat-container">
            <div className="messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <div className="message-input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    onKeyDown={handleKeyDown} // Add keydown event listener
                />
                <button onClick={handleSend}>Send</button>
            </div>
        </div>
    );
};

export default ChatBox;
