// Function to delete a contact
window.deleteContact = function(contactId) {
    fetch(`https://api.example.com/delete-contact/${contactId}`, { // Replace with your actual API endpoint
        method: 'DELETE',
    })
    .then(response => {
        if (response.ok) {
            console.log('Contact deleted successfully');
            // Remove the contact row from the table
            removeContactRow(contactId);
        } else {
            console.error('Failed to delete contact');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};

// Function to remove the contact row from the table
function removeContactRow(contactId) {
    const tableBody = document.getElementById('contactTableBody');
    const rows = tableBody.getElementsByTagName('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const deleteButton = row.querySelector('.delete-icon');
        if (deleteButton && deleteButton.getAttribute('onclick').includes(contactId)) {
            tableBody.removeChild(row);
            break; // Exit the loop after removing the row
        }
    }
}