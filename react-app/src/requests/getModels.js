import axios from 'axios'

export function getModels() {
    let models = null
    axios.get('/models')
    .then((response) => {
        models = response.data.data
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
    if (!models) return null;

    return models;
}