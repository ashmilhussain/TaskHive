import React from 'react';

const ConfirmationModal = ({ isOpen, onClose, onConfirm }) => {
    if (!isOpen) return null; // Don't render if not open

    return (
        <div className="confirmation-modal"> {/* Use a specific class for the confirmation modal */}
            <div className="modal-content">
                <h2>Confirm Deletion</h2>
                <p>Are you sure you want to delete this contact?</p>
                <div className="modal-buttons">
                    <button onClick={onConfirm}>Delete</button>
                    <button onClick={onClose}>Cancel</button>
                </div>
            </div>
        </div>
    );
};

export default ConfirmationModal;