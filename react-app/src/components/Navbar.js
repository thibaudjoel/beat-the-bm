import { NavLink } from "react-router-dom"

export const NavBar = () => {

    const navlinkStyles = ({ isActive }) => {
        return {
            fontWeight: isActive? 'bold' : 'normal',
            textDecoration: isActive? 'none' : 'underlined'
        }
    }
    return (
        <nav>
            <NavLink style={navlinkStyles} to='/'>Home</NavLink>
            <NavLink style={navlinkStyles} to='about'>About</NavLink>
        </nav>
    )
}