import axios from 'axios'
import { useState } from 'react';
import { useEffect } from 'react';

export const ModelList = () => {
    const [models, setModels] = useState(null);

    useEffect(() => {
        axios.get('/models')
        .then((response) => {
            setModels(response.data.data)
            // handle success
            console.log(response);
            })
        .catch((error) => {
            // handle error
            console.log(error);
        })
        .finally(() => {
            // always executed
        });
    })
    if (!models) return null;
    
    return (
        <div>
            <h1>List of Models</h1>
            <>
                {models.map((model,  id) => {
                    return (
                        <div key={id}>
                            <p>{model.user.name}</p>
                            <p>{model.modeltype.name}</p>
                            <p>{model.number_of_last_games.name}</p>
                        </div>
                    )
                }
                )
            }
            </>

        </div>

    )
}