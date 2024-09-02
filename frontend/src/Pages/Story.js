import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BACKEND_URL } from '../Constants';

export default function Story() {

    const navigate = useNavigate();
    // This is just terrible. API supports multiple characters and personalities, refactor code to adapt to that
    const [characterName, setCharacterName] = useState("");
    const [characterRole, setCharacterRole] = useState("");
    const [characterFirstTrait, setCharacterFirstTrait] = useState("");
    const [characterSecondTrait, setCharacterSecondTrait] = useState("");
    const [setting, setSetting] = useState("");
    const [theme, setTheme] = useState("");
    const [genre, setGenre] = useState("");

    var params = [
        characterName,
        characterRole,
        characterFirstTrait,
        characterSecondTrait,
        setting,
        theme,
        genre
    ]
    const [story, setStory] = useState("");
    const [showStory, setShowStory] = useState(false);
    const [loadingRequest, setLoadingRequest] = useState(false);
    const [disableButton, setDisableButton] = useState(true);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setShowStory(false)
        setLoadingRequest(true)

        try {
            const jwt_token = localStorage.getItem("auth") ? localStorage.getItem("auth") : "";
            const response = await fetch(BACKEND_URL+'/story/', {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Authorization': jwt_token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'characters': [
                      {
                        'name': characterName,
                        'role': characterRole,
                        'traits': [
                          characterFirstTrait,
                          characterSecondTrait
                        ]
                      }
                    ],
                    'setting': setting,
                    'theme': theme,
                    'genre': genre
                  })
                });
            
            if (response.ok) {
                const data = await response.json()
                setStory(data["story"])
                setShowStory(true)
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
        var areParamsValid = true
        params.forEach((param)=>{
            if (param === ""){
                areParamsValid = false
            }
        })
        if (areParamsValid){
            setDisableButton(false)
        } else {
            setDisableButton(true)
        }
    }, [params])

    return(
        <>
        <div className="page">
            <h1>Create a story</h1>
        </div>

        <div className="card card-wide">
            <div className="card-body card-elem">
                <h5 className="card-title">Enter the details of your story</h5>
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <div>
                            <label className="form-label" htmlFor="Name">Character's name</label>
                            <input
                                type="text"
                                id="Name"
                                className="form-control"
                                onChange={(e) => setCharacterName(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="form-label" htmlFor="Role">Charater's role</label>
                            <input
                                type="text"
                                id="Role"
                                className="form-control"
                                onChange={(e) => setCharacterRole(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="form-label" htmlFor="Trait1">Charater's main personality trait</label>
                            <input
                                type="text"
                                id="Trait1"
                                className="form-control"
                                onChange={(e) => setCharacterFirstTrait(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="form-label" htmlFor="Trait2">Charater's secondary personality trait</label>
                            <input
                                type="text"
                                id="Trait2"
                                className="form-control"
                                onChange={(e) => setCharacterSecondTrait(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="form-label" htmlFor="Setting">Where the story will take place</label>
                            <input
                                type="text"
                                id="Setting"
                                className="form-control"
                                onChange={(e) => setSetting(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="form-label" htmlFor="Theme">What the story will be about</label>
                            <input
                                type="text"
                                id="Theme"
                                className="form-control"
                                onChange={(e) => setTheme(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="form-label" htmlFor="Genre">Genre of the story</label>
                            <input
                                type="text"
                                id="Genre"
                                className="form-control"
                                onChange={(e) => setGenre(e.target.value)}
                            />
                        </div>
                        <button 
                            type="submit"
                            disabled={disableButton}
                            className={`btn ${disableButton ? "disabled-btn"  : "enabled-btn"} btn btn-primary btn-block mb-4`}>
                            Generate
                        </button>
                    </form>
                    {loadingRequest && (
                        <div>Generating story... This WILL take some time...</div>
                    )}
                </div>
            </div>
            
            {showStory && (
                <div className="card-body card-elem">
                    <h5 className="card-title story">Here's your story!</h5>
                    <div style={{backgroundColor:"#ffffff", color: "#000000", marginTop: "4rem", padding:"0.5rem", borderRadius:"5px"}}>
                        {story}
                    </div>
                </div>
            )}
        </div>
        </>
    )
}
