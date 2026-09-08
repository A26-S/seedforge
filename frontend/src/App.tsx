import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import SeedLibrary from './pages/SeedLibrary'
import RuleEditor from './pages/RuleEditor'
import Generator from './pages/Generator'
import Analysis from './pages/Analysis'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/seeds" element={<SeedLibrary />} />
          <Route path="/rules" element={<RuleEditor />} />
          <Route path="/generator" element={<Generator />} />
          <Route path="/analysis" element={<Analysis />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
