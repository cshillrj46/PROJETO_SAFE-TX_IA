// src/App.tsx
import {
  BrowserRouter as Router,
  Routes,
  Route,
  NavLink
} from "react-router-dom";
import TransactionAnalyzer from "./TransactionAnalyzer";
import TransactionHistory from "./TransactionHistory";
import ReclassificationForm from "./ReclassificationForm";

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-black text-white p-4">
        <header className="text-center mb-8">
          <h1 className="text-5xl font-extrabold mb-4">
            <span className="text-white">$afe</span>
            <span className="text-blue-500">TX</span>
          </h1>
          <nav className="flex justify-center gap-4">
            <NavLink
              to="/"
              className={({ isActive }) =>
                `text-white font-semibold ${isActive ? 'underline text-blue-400' : 'hover:text-blue-300'}`
              }
              end
            >
              Analyzer
            </NavLink>
            <NavLink
              to="/history"
              className={({ isActive }) =>
                `text-white font-semibold ${isActive ? 'underline text-blue-400' : 'hover:text-blue-300'}`
              }
            >
              History
            </NavLink>
            <NavLink
              to="/reclassify"
              className={({ isActive }) =>
                `text-white font-semibold ${isActive ? 'underline text-blue-400' : 'hover:text-blue-300'}`
              }
            >
              Manual Classification
            </NavLink>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<TransactionAnalyzer />} />
            <Route path="/history" element={<TransactionHistory />} />
            <Route path="/reclassify" element={<ReclassificationForm />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
