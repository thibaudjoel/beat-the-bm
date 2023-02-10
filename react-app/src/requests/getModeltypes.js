import axios from 'axios'

export function getModeltypes() {
    let modeltypes = null
    axios.get('/modeltypes')
    .then((response) => {
        modeltypes = response.data.data
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
    if (!modeltypes) return null;

    return modeltypes;
}