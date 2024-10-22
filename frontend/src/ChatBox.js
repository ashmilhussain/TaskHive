import React, { useState, useRef } from 'react';
import './styles.css'; // Import your styles
import axios from 'axios'; // Import axios for making HTTP requests

const ChatBox = () => {
    const [messages, setMessages] = useState([]); // State to hold chat messages
    const [input, setInput] = useState(''); // State for the input field
    const [loading, setLoading] = useState(false); // State for loading indicator
    const [isRecording, setIsRecording] = useState(false); // State to track recording status
    const mediaRecorderRef = useRef(null); // Ref to store MediaRecorder
    const [audioChunks, setAudioChunks] = useState([]); // State to hold audio chunks
    const [mediaStream, setMediaStream] = useState(null); // State to hold the media stream

    const handleSend = async () => {
        if (input.trim()) {
            const userMessage = { message: input };
            setMessages([...messages, { text: input, sender: 'user' }]); // Add user message
            setInput(''); // Clear input field
            setLoading(true); // Set loading to true

            try {
                // Send the message to the backend
                const response = await axios.post('http://localhost:8080/chat', userMessage);
                // Add the bot's response to the messages
                console.log(response.data);
                setMessages(prevMessages => [
                    ...prevMessages,
                    { text: response.data.status + " : " + response.data.message, sender: 'bot' }
                ]);
            } catch (error) {
                console.error('Error sending message:', error);
            } finally {
                setLoading(false); // Set loading to false after response
            }
        }
    };

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default behavior (like a new line)
            handleSend(); // Call the send message function
        }
    };

    const toggleRecording = async () => {
        if (isRecording) {
            // Stop recording
            if (mediaRecorderRef.current) {
                mediaRecorderRef.current.stop();
                console.log("Recording stopped."); // Log when recording stops
                if (mediaStream) {
                    mediaStream.getTracks().forEach(track => track.stop()); // Stop all tracks of the media stream
                    setMediaStream(null); // Clear the media stream reference
                }
            }
        } else {
            // Start recording
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorderRef.current = new MediaRecorder(stream);
                setMediaStream(stream); // Store the media stream

                mediaRecorderRef.current.ondataavailable = (event) => {
                    console.log("Data available:", event.data.size); // Log the size of the data available
                    if (event.data.size > 0) {
                        setAudioChunks(prev => [...prev, event.data]);
                    } else {
                        console.error('No audio data available.');
                    }
                };

                mediaRecorderRef.current.onstop = handleSendAudio; // Automatically send audio when stopped

                mediaRecorderRef.current.start();
                console.log("Recording started."); // Log when recording starts
            } catch (error) {
                console.error('Error starting recording:', error);
            }
        }
        setIsRecording(!isRecording); // Toggle the recording state
    };

    const handleSendAudio = async () => {
        // Check if there are audio chunks before creating the blob
        if (audioChunks.length === 0) {
            console.error('No audio chunks available to send.');
            return; // Exit if there are no audio chunks
        }

        // Create a Blob from the audio chunks
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

        // Ensure the audio blob is not empty before proceeding
        if (audioBlob.size === 0) {
            console.error('Audio blob is empty. Recording may not have been successful.');
            return; // Exit if the audio blob is empty
        }

        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.wav'); // Ensure the key is 'file'
        console.log('Audio Blob Size:', audioBlob.size);
        console.log('Audio Blob Type:', audioBlob.type);
            
        try {
            const response = await axios.post('http://localhost:8080/chat/audio', formData, {
                headers: {
                    'Content-Type': 'audio/wav', // This is optional; axios handles it automatically
                },
            });
            console.log(response.data);
            setMessages(prevMessages => [
                ...prevMessages,
                { text: response.data.transcription, sender: 'bot' } // Adjust based on your API response structure
            ]);
        } catch (error) {
            console.error('Error sending audio:', error);
        } finally {
            setAudioChunks([]); // Clear audio chunks after sending
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
                {loading && <div className="loading-dots">
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="dot"></span>
                </div>} {/* Loading indicator */}
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
                <button onClick={toggleRecording}>{isRecording ? 'Stop' : '🎤'}</button> {/* Microphone button */}
            </div>
        </div>
    );
};

export default ChatBox;
