import React from 'react';
import { Link } from 'react-router-dom'; // Ensure react-router-dom is installed

const Sidebar = () => {
    return (
        <div className="sidebar">
            <h2>TaskHive</h2>
            <ul>
                <li>
                    <Link to="/">
                        <i className="fas fa-home"></i> Home
                    </Link>
                </li>
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
                    <Link to="/notes">
                        <i className="fas fa-sticky-note"></i> Notes
                    </Link>
                </li>
            </ul>
        </div>
    );
};

export default Sidebar;