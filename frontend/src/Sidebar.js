import React from 'react';
import { Link } from 'react-router-dom'; // Ensure react-router-dom is installed

const Sidebar = () => {
    return (
        <div className="sidebar">
            <h2>TaskHive</h2>
            <ul>
                <li>
                    <Link to="/contacts">
                        <i className="fas fa-address-book"></i> Contacts
                    </Link>
                </li>
                <li>
                    <Link to="/tasks">
                        <i className="fas fa-tasks"></i> Tasks
                    </Link>
                </li>
                <li>
                    <Link to="/calendar">
                        <i className="fas fa-calendar-alt"></i> Calendar
                    </Link>
                </li>
            </ul>
        </div>
    );
};

export default Sidebar;