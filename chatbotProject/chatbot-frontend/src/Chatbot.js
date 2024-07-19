import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        if (input.trim()) {
            const userMessage = { sender: 'user', text: input };
            setMessages([...messages, userMessage]);

            try {
                const response = await axios.post('http://localhost:8000/api/chatbot/', { query: input });
                const botMessage = { sender: 'bot', text: response.data.response };
                setMessages([...messages, userMessage, botMessage]);
            } catch (error) {
                console.error('Error al enviar el mensaje:', error);
            }

            setInput('');
        }
    };

    return (
        <div>
            <div>
                {messages.map((msg, index) => (
                    <div key={index} className={msg.sender}>
                        <span>{msg.sender}:</span> {msg.text}
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                }}
            />
            <button onClick={sendMessage}>Enviar</button>
        </div>
    );
};

export default Chatbot;
