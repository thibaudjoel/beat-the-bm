import { Routes, Route } from 'react-router-dom';
import { Home } from './components/Home';
import { About } from './components/About';
import { NavBar } from './components/Navbar';
import { NewModel } from './components/NewModel';
import { NoMatch } from './components/NoMatch';
import './App.css';

function App() {
  return (
    <>
    <NavBar />
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='about' element={<About />} />
      <Route path='new-model' element={<NewModel />} />
      <Route path='*' element={<NoMatch />} />
    </Routes>
    </>
  );
}

export default App;
