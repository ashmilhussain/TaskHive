import React, { useState } from 'react';
import axios from 'axios';

const CreateContact = ({ closeModal }) => {
    const [name, setName] = useState('');
    const [mobile, setMobile] = useState('');
    const [email, setEmail] = useState('');
    const [organization, setOrganization] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8080/contacts', {
                name,
                mobile,
                email,
                organization,
            });
            closeModal(); // Close the modal after successful submission
        } catch (error) {
            console.error('Error creating contact:', error);
        }
    };

    return (
        <div className="modal-content">
            <span className="close" onClick={closeModal}>&times;</span>
            <h2>Create New Contact</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Mobile"
                    value={mobile}
                    onChange={(e) => setMobile(e.target.value)}
                    required
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Organization"
                    value={organization}
                    onChange={(e) => setOrganization(e.target.value)}
                    required
                />
                <button type="submit">Create Contact</button>
            </form>
        </div>
    );
};

export default CreateContact;