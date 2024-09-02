import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BACKEND_URL } from '../Constants';
 

export default function Login () {

    const navigate = useNavigate();
    const [userName, setUserName] = useState("");
    const [password, setPassword] = useState("");
    const [wrongCredentials, setWrongCredentials] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch(BACKEND_URL+'/login/', {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'username': userName,
                    'password': password
                })
                })
    
            if (response.ok) {
                setWrongCredentials(false)
            // Authenticate user
                const authHeader = response.headers.get('authorization');
                localStorage.setItem("auth", authHeader);
                navigate("/")
            } else {
                setWrongCredentials(true)
                console.error('Request failed:', response.status);
            }
        } catch (error) {
            console.error('Error:', error);
        }
        };

    return (
        <div>
            <section className="vh-100" style={{ backgroundColor: "#1e2b2e" }}>
                <div className="container py-5 h-100" style={{fontFamily: "Overpass, sans-serif"}}>
                    <div className="row d-flex justify-content-center align-items-center h-100">
                        <div className="col-12 col-md-8 col-lg-6 col-xl-5">
                            <div className="card shadow-2-strong" style={{ borderRadius: "1rem", backgroundColor: "" }}>
                                <div className="card-body p-5 text-center">
                                    <h2 className="mb-5">LM Interface</h2>
                                    <h3 className="mb-5">Sign in</h3>
                                    <form onSubmit={handleSubmit}>
                                        {/* Username input */}
                                        <div className="form-outline mb-4">
                                            <label className="form-label" htmlFor="user">
                                            Username
                                            </label>
                                            <input
                                                type="text"
                                                id="user"
                                                className="form-control"
                                                onChange={(e) => setUserName(e.target.value)} 
                                            />
                                        </div>
                                        {/* Password input */}
                                        <div className="form-outline mb-4">
                                            <label className="form-label" htmlFor="pass">
                                            Password
                                            </label>
                                            <input
                                                type="password"
                                                id="pass"
                                                className="form-control"
                                                onChange={(e) => setPassword(e.target.value)}
                                            />
                                        </div>
                                        {wrongCredentials && <div className="mb-4" style={{color: "#db1f3d"}}>
                                            <small>Incorrect username or password</small>
                                        </div>}
                                        {/* Submit button */}
                                        <button
                                            className="btn btn-primary btn-block mb-4"
                                            style={{
                                                backgroundColor: "#01ecb4",
                                                borderColor: "#01ecb4"
                                            }}
                                        >
                                            Log in
                                        </button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
}