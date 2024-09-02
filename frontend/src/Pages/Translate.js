import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BACKEND_URL } from '../Constants';

export default function Translate() {

    // This whole implementation should be refactored into a component with args and be reused for other pages
    const navigate = useNavigate();
    const [prompt, setPrompt] = useState("");
    const [language, setLanguage] = useState("");
    const [translated, setTranslated] = useState("");
    const [showTranslation, setShowTranslation] = useState(false);
    const [loadingRequest, setLoadingRequest] = useState(false);
    const [disableButton, setDisableButton] = useState(true);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setShowTranslation(false)
        setLoadingRequest(true)

        try {
            const jwt_token = localStorage.getItem("auth") ? localStorage.getItem("auth") : "";
            const response = await fetch(BACKEND_URL+'/translate/', {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Authorization': jwt_token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'text': prompt,
                    'language': language
                })
                });
            
            if (response.ok) {
                const data = await response.json()
                setTranslated(data["translation"])
                setShowTranslation(true)
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
        if (prompt !== "" && language !==""){
            setDisableButton(false)
        } else {
            setDisableButton(true)
        }
    }, [prompt, language])

    return(
        <>
        <div className="page">
            <h1>Translate</h1>
        </div>

        <div className="card">
            <div className="card-body">
                <h5 className="card-title">Enter the text you want to translate</h5>
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
                    <div>
                        <label className="form-label" htmlFor="language">Language to translate to</label>
                        <input
                            type="text"
                            id="language"
                            className="form-control"
                            onChange={(e) => setLanguage(e.target.value)}
                        />
                    </div>
                    <button 
                        type="submit"
                        disabled={disableButton}
                        className={`btn ${disableButton ? "disabled-btn"  : "enabled-btn"} btn btn-primary btn-block mb-4`}>
                        Translate
                    </button>
                </form>
                {loadingRequest && (
                    <div>Translating... This might take some time...</div>
                )}
            </div>
            
            {showTranslation && (
                <div className="card-body">
                    <h5 className="card-title">Translated text</h5>
                    <div style={{backgroundColor:"#ffffff", color: "#000000", padding:"5px", borderRadius:"5px"}}>
                        {translated}
                    </div>
                </div>
            )}
        </div>
        </>
    )
}
