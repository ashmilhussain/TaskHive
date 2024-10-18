import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './styles.css'; // Import your styles

const ChatBox = () => {
    const [messages, setMessages] = useState(["tes","test message","message","replay"]);
    const [input, setInput] = useState('hello');

    const sendMessage = () => {
        if (input) {
            setMessages([...messages, input]);
            setInput('');
        }
    };

    return (
        <div>
            <div className="chat-box">
                {messages.map((msg, index) => (
                    <div key={index}>{msg}</div>
                ))}
            </div>
            <input 
                type="text" 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
                placeholder="Type a message..." 
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

// Render the App component into the root div
ReactDOM.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    document.getElementById('root') // This should match the ID in index.html
);