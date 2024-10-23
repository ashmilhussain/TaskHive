import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles.css'; // Import your styles

const Tasks = () => {
    const [tasks, setTasks] = useState([]); // State to hold tasks
    const [loading, setLoading] = useState(true); // State to manage loading
    const [isModalOpen, setIsModalOpen] = useState(false); // State to manage modal visibility
    const [newTask, setNewTask] = useState({ title: '', description: '', completed: false }); // State for new task

    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const response = await axios.get('http://localhost:8080/tasks'); // Adjust the URL if needed
                setTasks(response.data); // Set the tasks state
            } catch (error) {
                console.error('Error fetching tasks:', error);
            } finally {
                setLoading(false); // Set loading to false after fetching
            }
        };

        fetchTasks(); // Call the fetch function
    }, []); // Empty dependency array means this runs once on mount

    const handleAddTask = async () => {
        try {
            const response = await axios.post('http://localhost:8080/tasks', newTask); // Send new task to backend
            setTasks([...tasks, response.data]); // Add the new task to the list
            setNewTask({ title: '', description: '', completed: false }); // Reset the new task state
            setIsModalOpen(false); // Close the modal
        } catch (error) {
            console.error('Error adding task:', error);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewTask({ ...newTask, [name]: value }); // Update the new task state
    };

    if (loading) {
        return <p>Loading tasks...</p>; // Show loading message
    }

    return (
            <div class="px-4 py-3 justify-between">
            <div class="flex px-4 py-3 justify-end">
            <button onClick={() => setIsModalOpen(true)} class="min-w-[84px] max-w-[480px] cursor-pointer overflow-hidden rounded-xl h-8 px-4 bg-[#1d8cd7] text-white text-sm font-medium leading-normal @[480px]:block">
            <span class="truncate">Add New Task</span>                
            </button>
            </div>
            {tasks.length === 0 ? (
                <p className="no-tasks">No tasks found.</p>
            ) : (
                <div class="px-4 py-3 justify-between">
                <h3 class="text-[#111517] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Tasks for you</h3>
                {tasks.map(task => (
                <div class="flex gap-4 bg-white px-4 py-3 justify-between">
                    <div class="flex items-start gap-4">
                        <div class="text-[#111517] flex items-center justify-center rounded-lg bg-[#f0f3f4] shrink-0 size-12" data-icon="Clock" data-size="24px" data-weight="regular">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                            <path
                            d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm64-88a8,8,0,0,1-8,8H128a8,8,0,0,1-8-8V72a8,8,0,0,1,16,0v48h48A8,8,0,0,1,192,128Z"
                            ></path>
                        </svg>
                        </div>
                        <div class="flex flex-1 flex-col justify-center">
                        <p class="text-[#111517] text-base font-medium leading-normal">{task.title}</p>
                        <p class="text-[#647987] text-sm font-normal leading-normal">Business</p>
                        <p class="text-[#647987] text-sm font-normal leading-normal">{task.description}</p>
                        </div>
                    </div>
                    <div class="shrink-0"><p class="text-[#647987] text-sm font-normal leading-normal">1 hour from now</p></div>
            </div>

                ))}
                </div>
                )}
            {isModalOpen && (
                <div className={`modal ${isModalOpen ? 'open' : ''}`}>
                    <div className="modal-content">
                        <span className="close" onClick={() => setIsModalOpen(false)}>&times;</span>
                        <h2>Add New Task</h2>
                        <input
                            type="text"
                            name="title"
                            value={newTask.title}
                            onChange={handleInputChange}
                            placeholder="Task Title"
                            required
                        />
                        <input
                            type="text"
                            name="description"
                            value={newTask.description}
                            onChange={handleInputChange}
                            placeholder="Task Description"
                            required
                        />
                        <button onClick={handleAddTask}>Add Task</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Tasks;