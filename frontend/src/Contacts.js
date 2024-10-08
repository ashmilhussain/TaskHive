import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CreateContact from './CreateContact'; // Import the CreateContact component
import ConfirmationModal from './ConfirmationModal'; // Import the ConfirmationModal component
import './styles.css'; // Import the consolidated CSS file

const Contacts = () => {
    const [contacts, setContacts] = useState([]); // State to hold contacts
    const [loading, setLoading] = useState(true); // State to manage loading
    const [isModalOpen, setIsModalOpen] = useState(false); // State to manage modal visibility
    const [isConfirmOpen, setIsConfirmOpen] = useState(false); // State for confirmation modal
    const [contactToDelete, setContactToDelete] = useState(null); // Store the contact to delete

    useEffect(() => {
        const fetchContacts = async () => {
            try {
                const response = await axios.get('http://localhost:8080/contacts'); // Adjust the URL if needed
                setContacts(response.data); // Set the contacts state
            } catch (error) {
                console.error('Error fetching contacts:', error);
            } finally {
                setLoading(false); // Set loading to false after fetching
            }
        };

        fetchContacts(); // Call the fetch function
    }, []); // Empty dependency array means this runs once on mount

    const handleCreateContact = () => {
        setIsModalOpen(true); // Open the modal
    };

    const closeModal = () => {
        setIsModalOpen(false); // Close the modal
    };

    const openConfirmModal = (contactId) => {
        setContactToDelete(contactId); // Set the contact to delete
        setIsConfirmOpen(true); // Open the confirmation modal
    };

    const closeConfirmModal = () => {
        setIsConfirmOpen(false); // Close the confirmation modal
        setContactToDelete(null); // Clear the contact to delete
    };

    const deleteContact = async () => {
        if (contactToDelete) {
            try {
                await axios.delete(`http://localhost:8080/contacts/${contactToDelete}`);
                // Refresh the contact list after deletion
                setContacts(contacts.filter(contact => contact.id !== contactToDelete));
            } catch (error) {
                console.error("Error deleting contact:", error);
            } finally {
                closeConfirmModal(); // Close the confirmation modal
            }
        }
    };

    if (loading) {
        return <p>Loading contacts...</p>; // Show loading message
    }

    return (
        <div>
            <h1>Contacts</h1>
            <button onClick={handleCreateContact} style={{ marginBottom: '20px' }}>
                Create New Contact
            </button>
            {contacts.length === 0 ? (
                <p className="no-contacts">No contacts found.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Phone</th>
                            <th>Email</th>
                            <th>Organization</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {contacts.map(contact => (
                            <tr key={contact.id}>
                                <td>{contact.name}</td>
                                <td>{contact.mobile}</td>
                                <td>{contact.email}</td>
                                <td>{contact.organization}</td>
                                <td>
                                    <i className="fas fa-trash-alt delete-icon" onClick={() => openConfirmModal(contact.id)}></i>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
            {isModalOpen && (
                <div className={`modal ${isModalOpen ? 'open' : ''}`}>
                    <div className="modal-content">
                        <span className="close" onClick={closeModal}>&times;</span>
                        <CreateContact closeModal={closeModal} />
                    </div>
                </div>
            )}
            <ConfirmationModal
                isOpen={isConfirmOpen}
                onClose={closeConfirmModal}
                onConfirm={deleteContact} // Ensure this is set correctly
            />
        </div>
    );
};

export default Contacts;