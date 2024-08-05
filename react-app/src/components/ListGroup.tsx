import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function ListGroup() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loginStatus, setLoginStatus] = useState<null | 'success' | 'error'>(null);

    const handleClick = (event: React.FormEvent) => {
        event.preventDefault();
        fetch('http://localhost:8000/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
            .then(response => {
                if (response.status === 200) {
                    setLoginStatus('success');
                } else {
                    setLoginStatus('error');
                }
                return response.json();
            })
            .then(data => {
                console.log(data); // Log the response data
                // Handle the response data
            })
            .catch(error => {
                setLoginStatus('error');
                // Handle any errors
            });
    };

    return (
        <div className="container mt-5">
            <h1 className="mb-4">This is the heading.</h1>
            {loginStatus === 'success' && (
                <div className="alert alert-success" role="alert">
                    Login successful!
                </div>
            )}
            {loginStatus === 'error' && (
                <div className="alert alert-danger" role="alert">
                    Login unsuccessful!
                </div>
            )}
            <form onSubmit={handleClick}>
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username:</label>
                    <input
                        type="text"
                        id="username"
                        className="form-control"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password:</label>
                    <input
                        type="password"
                        id="password"
                        className="form-control"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </div>
    );
}

export default ListGroup;