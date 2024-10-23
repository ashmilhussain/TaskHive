import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles.css'; // Import your styles

const Notes = () => {
    const [notes, setNotes] = useState([]); // State to hold tasks
    const [loading, setLoading] = useState(true); // State to manage loading
    const [isModalOpen, setIsModalOpen] = useState(false); // State to manage modal visibility
    const [newNote, setNewNote] = useState({ title: '', description: '', completed: false }); // State for new task

    useEffect(() => {
        const fetchNotes = async () => {
            try {
                const response = await axios.get('http://localhost:8080/notes'); // Adjust the URL if needed
                setNotes(response.data); // Set the tasks state
            } catch (error) {
                console.error('Error fetching notes:', error);
            } finally {
                setLoading(false); // Set loading to false after fetching
            }
        };

        fetchNotes(); // Call the fetch function
    }, []); // Empty dependency array means this runs once on mount

    // const handleAddTask = async () => {
    //     try {
    //         const response = await axios.post('http://localhost:8080/tasks', newTask); // Send new task to backend
    //         setTasks([...tasks, response.data]); // Add the new task to the list
    //         setNewTask({ title: '', description: '', completed: false }); // Reset the new task state
    //         setIsModalOpen(false); // Close the modal
    //     } catch (error) {
    //         console.error('Error adding task:', error);
    //     }
    // };

    // const handleInputChange = (e) => {
    //     const { name, value } = e.target;
    //     setNewTask({ ...newTask, [name]: value }); // Update the new task state
    // };

    if (loading) {
        return <p>Loading notes...</p>; // Show loading message
    }

    return (
            <div class="px-4 py-3 justify-between">
            <div class="flex px-4 py-3 justify-end">
            <button onClick={() => setIsModalOpen(true)} class="min-w-[84px] max-w-[480px] cursor-pointer overflow-hidden rounded-xl h-8 px-4 bg-[#1d8cd7] text-white text-sm font-medium leading-normal @[480px]:block">
            <span class="truncate">New Note</span>                
            </button>
            </div>
            {notes.length === 0 ? (
                <p className="no-tasks">No notes found.</p>
            ) : (
                <div class="px-4 py-3 justify-between">
                <h3 class="text-[#111517] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Notes Area</h3>
                {notes.map(note => (
                <div class="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2 justify-between">
                <div class="flex items-center gap-4">
                  <div class="text-[#111517] flex items-center justify-center rounded-lg bg-[#f0f3f4] shrink-0 size-12" data-icon="Note" data-size="24px" data-weight="regular">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                      <path
                        d="M88,96a8,8,0,0,1,8-8h64a8,8,0,0,1,0,16H96A8,8,0,0,1,88,96Zm8,40h64a8,8,0,0,0,0-16H96a8,8,0,0,0,0,16Zm32,16H96a8,8,0,0,0,0,16h32a8,8,0,0,0,0-16ZM224,48V156.69A15.86,15.86,0,0,1,219.31,168L168,219.31A15.86,15.86,0,0,1,156.69,224H48a16,16,0,0,1-16-16V48A16,16,0,0,1,48,32H208A16,16,0,0,1,224,48ZM48,208H152V160a8,8,0,0,1,8-8h48V48H48Zm120-40v28.7L196.69,168Z"
                      ></path>
                    </svg>
                  </div>
                  <div class="flex flex-col justify-center">
                    <p class="text-[#111517] text-base font-medium leading-normal line-clamp-1">{note.title}</p>
                    <p class="text-[#647987] text-sm font-normal leading-normal line-clamp-2">{note.description}</p>
                    <p class="text-[#647987] text-sm font-normal leading-normal line-clamp-2">2 days ago</p>
                  </div>
                </div>
                <div class="shrink-0"><button class="text-base font-medium leading-normal">Edit</button></div>
              </div>

                ))}
                </div>
            //     <table>
            //         <thead>
            //             <tr>
            //                 <th>Title</th>
            //                 <th>Description</th>
            //                 <th>Completed</th>
            //             </tr>
            //         </thead>
            //         <tbody>
            //             {tasks.map(task => (
            //                 <tr key={task.id}>
            //                     <td>{task.title}</td>
            //                     <td>{task.description}</td>
            //                     <td>{task.completed ? 'Yes' : 'No'}</td>
            //                 </tr>
            //             ))}
            //         </tbody>
            //     </table>
            // )}
            // {isModalOpen && (
            //     <div className={`modal ${isModalOpen ? 'open' : ''}`}>
            //         <div className="modal-content">
            //             <span className="close" onClick={() => setIsModalOpen(false)}>&times;</span>
            //             <h2>Add New Task</h2>
            //             <input
            //                 type="text"
            //                 name="title"
            //                 value={newTask.title}
            //                 onChange={handleInputChange}
            //                 placeholder="Task Title"
            //                 required
            //             />
            //             <input
            //                 type="text"
            //                 name="description"
            //                 value={newTask.description}
            //                 onChange={handleInputChange}
            //                 placeholder="Task Description"
            //                 required
            //             />
            //             <button onClick={handleAddTask}>Add Task</button>
            //         </div>
            //     </div>
            )}
        </div>
    );
};

export default Notes;