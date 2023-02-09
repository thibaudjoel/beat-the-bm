import { useNavigate } from "react-router-dom"
import { ModelList } from "./ModelList"

export const Home = () => {
    const navigate = useNavigate()
    return (
        <>
            <div>Home Page</div>
            <button onClick={() => navigate('new-model')}>Create model</button>
            <ModelList />
        </>
    )

}