import { useState, useEffect } from 'react'

export const MatchList = () => {
    const [matches, setMatches] = useState([])

    useEffect(() =>{
        fetch(apiendpoint)
        .then(response => response.json())
        .then(data => setMatches(data))
        .catch((err) => {
            console.log(err)
        })
    }, [])

    return <div>
        <ul>
            {
                matches.map(match => {
                    return <li key={match.id}>{match.home_team}</li>
                })
            }
        </ul>
    </div>
}