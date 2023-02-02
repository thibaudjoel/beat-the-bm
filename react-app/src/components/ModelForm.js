import { useState } from 'react'

export const ModelForm = () => {
    const [modelname, setModelname] = useState("")
    const [number_games, setNumbergames] = useState(0)
    const [seasons, setSeasons] = useState([])
    const [modeltype, setModeltype] = useState("")
    const [features, setFeatures] = useState([])

    const handleSubmit = (event) => {
        event.preventDefault()
        // alert('Form data is ${modelname}')
        fetch(apiendpoint, {
            method: 'POST',
            body: JSON.stringify({
                name: modelname
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
            .then((response) => response.json())
            .then((json) => console.log(json))
        })
    }

    return <form onSubmit={handleSubmit}>
        <div>
            <label>Model name</label>
            <input
            type='text'
            placeholder='model name'
            value={modelname}
            onChange={(event) => setModelname(event.target.value)}
            />
            <label>#Games</label>
            <input
            type='number'
            placeholder='number of previous games to use for prediction'
            value={number_games}
            onChange={(event) => setNumbergames(event.target.value)}
            />
            <label>Seasons</label>
            <select
            multiple={true}
            placeholder='seasons whose matches are used for training the model'
            value={seasons}
            onChange={(event) => setSeasons(event.target.value)}
            >
                <option value="feature_d">Feature 1</option>
            </select>

            <label>Modeltype</label>
            <select
            required
            placeholder='Statistical model that is used for prediction'
            value={modeltype}
            onChange={(event) => setModeltype(event.target.value)}
            >
                <option value="modeltype_id">Modeltype 1</option>
            </select>
            <label>Features</label>
            <select
            multiple={true}
            required
            placeholder='Features that will be used for prediction'
            value={features}
            onChange={(event) => setFeatures(event.target.value)}
            >
                <option value="feature_id">Feature 1</option>
            </select>
        </div>
        <button type='submit'>Submit</button>
    </form>
}