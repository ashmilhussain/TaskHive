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
        <div>
            <h1>Tasks</h1>
            <button onClick={() => setIsModalOpen(true)} style={{ marginBottom: '20px' }}>
                Add New Task
            </button>
            {tasks.length === 0 ? (
                <p className="no-tasks">No tasks found.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Description</th>
                            <th>Completed</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tasks.map(task => (
                            <tr key={task.id}>
                                <td>{task.title}</td>
                                <td>{task.description}</td>
                                <td>{task.completed ? 'Yes' : 'No'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
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