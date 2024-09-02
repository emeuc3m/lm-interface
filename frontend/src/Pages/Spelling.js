import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BACKEND_URL } from '../Constants';

export default function Spelling() {

    const navigate = useNavigate();
    const [prompt, setPrompt] = useState("");
    const [correction, setCorrection] = useState("");
    const [showCorrection, setShowCorrection] = useState(false);
    const [loadingRequest, setLoadingRequest] = useState(false);
    const [disableButton, setDisableButton] = useState(true);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setShowCorrection(false)
        setLoadingRequest(true)

        try {
            const jwt_token = localStorage.getItem("auth") ? localStorage.getItem("auth") : "";
            const response = await fetch(BACKEND_URL+'/spelling/', {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Authorization': jwt_token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'text': prompt,
                })
                });
            
            if (response.ok) {
                const data = await response.json()
                setCorrection(data["correction"])
                setShowCorrection(true)
            } else {
                console.log("error")
                // If unauthorized, go to login
                if (response.status===401){
                    navigate("/login")
                }
                console.error('Request failed:', response.status);
            }
        } catch (error) {
            console.error('Error:', error);
        }
        setLoadingRequest(false)
    };

    useEffect(() => {
        if (prompt !== ""){
            setDisableButton(false)
        } else {
            setDisableButton(true)
        }
    }, [prompt])

    return(
        <>
        <div className="page">
            <h1>Fix spelling</h1>
        </div>

        <div className="card">
            <div className="card-body">
                <h5 className="card-title">Enter the text you want to spell check</h5>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label className="form-label" htmlFor="toTranslate"/>
                        <input
                            type="text"
                            id="toTranslate"
                            className="form-control"
                            onChange={(e) => setPrompt(e.target.value)}
                        />
                    </div>
                    <button 
                        type="submit"
                        disabled={disableButton}
                        className={`btn ${disableButton ? "disabled-btn"  : "enabled-btn"} btn btn-primary btn-block mb-4`}>
                        Fix spelling
                    </button>
                </form>
                {loadingRequest && (
                    <div>Correcting... This might take some time...</div>
                )}
            </div>
            
            {showCorrection && (
                <div className="card-body">
                    <h5 className="card-title">Corrected text</h5>
                    <div style={{backgroundColor:"#ffffff", color: "#000000", padding:"5px", borderRadius:"5px"}}>
                        {correction}
                    </div>
                </div>
            )}
        </div>
        </>
    )
}
