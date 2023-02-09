import { useNavigate } from "react-router-dom"
import { ModelForm } from "./ModelForm"

export const NewModel = () => {
    const navigate = useNavigate()
    return (
        <>
            <div>New Model</div>
            <ModelForm />
            <button onClick={() => navigate(-1)}>Go back</button>
            
        </>
    )

}