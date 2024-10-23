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
        <div class="px-4 py-3 justify-between">
            <div class="flex px-4 py-3 justify-end">
            <button onClick={handleCreateContact} class="min-w-[84px] max-w-[480px] cursor-pointer overflow-hidden rounded-xl h-8 px-4 bg-[#1d8cd7] text-white text-sm font-medium leading-normal @[480px]:block">
            <span class="truncate">Create New Contact</span>                
            </button>
            </div>
            {contacts.length === 0 ? (
                <p className="no-contacts">No contacts found.</p>
            ) : (
                <div class="px-4 py-3 justify-between">
                <h3 class="text-[#111517] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Idle Contacts</h3>
                {contacts.map(contact => (
                    <div class="flex gap-4 bg-white px-4 py-3 justify-between">
                    <div class="flex items-start gap-4">
                      <div
                        class="bg-center bg-no-repeat aspect-square bg-cover rounded-full h-[70px] w-fit"
                        style={{backgroundImage: 'url("https://cdn.usegalileo.ai/stability/a70cd5bb-a687-4667-9525-da1a3eafc973.png")'}}
                      ></div>
                      <div class="flex flex-1 flex-col justify-center">
                        <p class="text-[#111517] text-base font-medium leading-normal">{contact.name}</p>
                        <p class="text-[#647987] text-sm font-normal leading-normal">Personal</p>
                        <p class="text-[#647987] text-sm font-normal leading-normal">No recent activity</p>
                      </div>
                    </div>
                    <div class="shrink-0"><button class="text-base font-medium leading-normal">Email</button></div>
                  </div>
                        ))}
                </div>
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