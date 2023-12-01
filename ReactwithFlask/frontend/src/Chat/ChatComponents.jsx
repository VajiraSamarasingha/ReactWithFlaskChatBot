import React, {useState} from 'react'
import axios from 'axios';

const ChatComponents = () => {
    const [message, setMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);

    const sendMessage = async() => {
        const response = await axios.post('http://192.168.174.209:5000/send_message', {message})

        //setChatHistory([...chatHistory,{user:'You', message}]);
        //setChatHistory([...chatHistory,{user:'Bot', message:response.data.message}]);
        //setMessage('');

        const newChat = { user: 'You', message };
        const botResponse = { user: 'Bot', message: response.data.message };
        setChatHistory([...chatHistory, newChat, botResponse]);
        setMessage('');


    };

    return (
        <div>
            <div>
                {chatHistory.map((chat, index)=>(
                    <div key={[index]}>
                        <strong>{chat.user}:</strong>{chat.message}
                    </div>
                ))}
            </div>
            <input
                type='text'
                value={message}
                onChange={(e)=> setMessage(e.target.value)}
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default ChatComponents;
