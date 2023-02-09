import axios from 'axios'

export function getSeasons() {
    let seasons = null
    axios.get('/features')
    .then((response) => {
        seasons = response.data.data
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
    if (!seasons) return null;

    return seasons;
}