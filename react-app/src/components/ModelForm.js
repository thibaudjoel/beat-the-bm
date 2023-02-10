import axios from 'axios'
import { useState } from 'react'
import { getSeasons } from '../requests/getSeasons'
import { getModeltypes } from '../requests/getModeltypes'
import { getFeatures } from '../requests/getFeatures'

export const ModelForm = () => {
    const seasonsData = getSeasons()
    const modeltypesData = getModeltypes()
    const featuresData = getFeatures()

    const [modelname, setModelname] = useState("")
    const [number_games, setNumbergames] = useState(0)
    const [seasons, setSeasons] = useState([])
    const [modeltype, setModeltype] = useState("")
    const [features, setFeatures] = useState([])

    // const handleSubmit = (event) => {
    //     PostModel({name: {event.target.modelname.value},
    //                 user_id:
    //             modeltype_id
    //             number_of_last_games
    //             seasonss})
        

    // }

    return <form /*onSubmit={handleSubmit}*/>
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
            {() => {if (seasonsData) return seasonsData.map((season, season_id) => {
                if (!season) return null;
                return (
                    
                    <option value={season_id}>
                        {season.name}
                    </option>
                )
                }
                )
            }
            }
            </select>

            <label>Modeltype</label>
            <select
            required
            placeholder='Statistical model that is used for prediction'
            value={modeltype}
            onChange={(event) => setModeltype(event.target.value)}
            >
                {() => {if (modeltypesData) return modeltypesData.map((modeltype, modeltype_id) => {
                    return (
                        <option value={modeltype_id}>
                            {modeltype.name}
                        </option>
                    )
                    }
                )
            }
            }
            </select>
            <label>Features</label>
            <select
            multiple={true}
            required
            placeholder='Features that will be used for prediction'
            value={features}
            onChange={(event) => setFeatures(event.target.value)}
            >
            {() => {if (featuresData) return featuresData.map((feature, feature_id) => {
                return (
                    <option value={feature_id}>
                        {feature.name}
                    </option>
                )
                }
                )
            }
        }
            </select>
        </div>
        <button type='submit'>Submit</button>
    </form>
}