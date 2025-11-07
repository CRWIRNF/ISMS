import { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import RequirementsPage from './pages/RequirementsPage'
import MeasuresPage from './pages/MeasuresPage'
import RisksPage from './pages/RisksPage'
import Layout from './components/Layout'

function App() {
  const { isAuthenticated, isLoading, checkAuth } = useAuthStore()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={
          isAuthenticated ? <Navigate to="/" replace /> : <LoginPage />
        } />

        <Route element={<Layout />}>
          <Route path="/" element={
            isAuthenticated ? <DashboardPage /> : <Navigate to="/login" replace />
          } />
          <Route path="/requirements" element={
            isAuthenticated ? <RequirementsPage /> : <Navigate to="/login" replace />
          } />
          <Route path="/measures" element={
            isAuthenticated ? <MeasuresPage /> : <Navigate to="/login" replace />
          } />
          <Route path="/risks" element={
            isAuthenticated ? <RisksPage /> : <Navigate to="/login" replace />
          } />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
