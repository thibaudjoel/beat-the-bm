import axios from 'axios'

export function getFeatures() {
    let features = null
    axios.get('/features')
    .then((response) => {
        features = response.data.data
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
    if (!features) return null;

    return features;
}