import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './Sidebar';
import Contacts from './Contacts'; // Import your Contacts component
import Tasks from './Tasks'; // Import your Tasks component
import Notes from './Notes'; // Import your Notes component
import CreateContact from './CreateContact'; // Import the CreateContact component
import ChatBox from './ChatBox'; // Import the ChatBox component

const App = () => {
    return (
        <Router>
            <div className="app">
                <Sidebar />
                <div className="content">
                    <Routes>
                        <Route path="/contacts" element={<Contacts />} />
                        <Route path="/tasks" element={<Tasks />} /> {/* New route for tasks */}
                        <Route path="/notes" element={<Notes />} />
                        <Route path="/create-contact" element={<CreateContact />} />
                        <Route path="/" element={<ChatBox />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

export default App;