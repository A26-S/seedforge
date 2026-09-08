import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import {
  FiHome,
  FiDatabase,
  FiGitBranch,
  FiZap,
  FiBarChart2,
  FiMenu,
  FiX,
} from 'react-icons/fi'
import { useUiStore } from '../stores/ui'

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const navigate = useNavigate()
  const location = useLocation()
  const { sidebarOpen, toggleSidebar } = useUiStore()

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: FiHome },
    { path: '/seeds', label: 'Seed Library', icon: FiDatabase },
    { path: '/rules', label: 'Rule Editor', icon: FiGitBranch },
    { path: '/generator', label: 'Generator', icon: FiZap },
    { path: '/analysis', label: 'Analysis', icon: FiBarChart2 },
  ]

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-gray-900 text-white transition-transform duration-300 transform ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } md:relative md:translate-x-0`}
      >
        <div className="flex items-center justify-between h-16 px-4 border-b border-gray-800">
          <h1 className="text-xl font-bold">🌱 SeedForge</h1>
          <button
            onClick={toggleSidebar}
            className="md:hidden p-1 rounded hover:bg-gray-800"
          >
            <FiX size={20} />
          </button>
        </div>

        <nav className="mt-8 space-y-2 px-4">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <button
                key={item.path}
                onClick={() => {
                  navigate(item.path)
                  if (window.innerWidth < 768) toggleSidebar()
                }}
                className={`w-full flex items-center space-x-3 px-4 py-2 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800'
                }`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </button>
            )
          })}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 h-16 flex items-center px-4 md:px-8">
          <button
            onClick={toggleSidebar}
            className="md:hidden p-2 rounded hover:bg-gray-100 mr-4"
          >
            <FiMenu size={20} />
          </button>
          <h2 className="text-lg font-semibold text-gray-900">Password Dictionary Generator</h2>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-auto">
          <div className="container py-8">{children}</div>
        </main>
      </div>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 md:hidden z-40"
          onClick={toggleSidebar}
        />
      )}
    </div>
  )
}

export default Layout
