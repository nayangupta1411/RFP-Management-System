import './App.css';
import { Routes, Route } from 'react-router-dom';
import './styles/request.css';
import './styles/main.css';
import './styles/showAnalysis.css';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Request from './components/dashboard/Request';
import Response from './components/dashboard/Response';
import ShowAnalysis from './components/dashboard/ShowAnalysis';

function App() {
  return (
    <div className="App">
      <Header title="RFP Management System" />
      <Footer title="Version 1.0.0" />
      <Routes>
        <Route path="/" element={<Request />} />
        <Route path="/dashboard/getRequest" element={<Request />} />
        <Route path="/dashboard/getResponse" element={<Response />} />
        <Route path="/dashboard/showAnalysis" element={<ShowAnalysis />} />
      </Routes>
    </div>
  );
}

export default App;
