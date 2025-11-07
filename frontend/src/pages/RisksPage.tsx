import React, { useState, useEffect } from 'react'
import { risksApi } from '@/services/api'
import type { Risk, RiskCreate, RiskUpdate, RiskLevel, RiskStatus, RiskStatistics } from '@/types'

const RisksPage: React.FC = () => {
  const [risks, setRisks] = useState<Risk[]>([])
  const [statistics, setStatistics] = useState<RiskStatistics | null>(null)
  const [loading, setLoading] = useState(true)
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [showEditDialog, setShowEditDialog] = useState(false)
  const [selectedRisk, setSelectedRisk] = useState<Risk | null>(null)
  const [filterStatus, setFilterStatus] = useState<RiskStatus | 'all'>('all')
  const [filterLevel, setFilterLevel] = useState<RiskLevel | 'all'>('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [showMatrix, setShowMatrix] = useState(false)
  const [riskMatrix, setRiskMatrix] = useState<Record<string, number>>({})

  useEffect(() => {
    loadRisks()
    loadStatistics()
  }, [filterStatus, filterLevel, searchTerm])

  const loadRisks = async () => {
    try {
      setLoading(true)
      const params: any = {}
      if (filterStatus !== 'all') params.status = filterStatus
      if (filterLevel !== 'all') params.level = filterLevel
      if (searchTerm) params.search = searchTerm

      const data = await risksApi.list(params)
      setRisks(data)
    } catch (error) {
      console.error('Error loading risks:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadStatistics = async () => {
    try {
      const stats = await risksApi.getStatistics()
      setStatistics(stats)
    } catch (error) {
      console.error('Error loading statistics:', error)
    }
  }

  const loadMatrix = async () => {
    try {
      const data = await risksApi.getMatrix()
      setRiskMatrix(data.matrix)
      setShowMatrix(true)
    } catch (error) {
      console.error('Error loading risk matrix:', error)
    }
  }

  const handleCreateRisk = async (data: RiskCreate) => {
    try {
      await risksApi.create(data)
      setShowCreateDialog(false)
      loadRisks()
      loadStatistics()
    } catch (error) {
      console.error('Error creating risk:', error)
      alert('Error creating risk')
    }
  }

  const handleUpdateRisk = async (id: number, data: RiskUpdate) => {
    try {
      await risksApi.update(id, data)
      setShowEditDialog(false)
      setSelectedRisk(null)
      loadRisks()
      loadStatistics()
    } catch (error) {
      console.error('Error updating risk:', error)
      alert('Error updating risk')
    }
  }

  const handleDeleteRisk = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this risk?')) return

    try {
      await risksApi.delete(id)
      loadRisks()
      loadStatistics()
    } catch (error) {
      console.error('Error deleting risk:', error)
      alert('Error deleting risk')
    }
  }

  const handleAcceptRisk = async (id: number) => {
    try {
      await risksApi.accept(id)
      loadRisks()
      loadStatistics()
    } catch (error) {
      console.error('Error accepting risk:', error)
      alert('Error accepting risk')
    }
  }

  const handleCloseRisk = async (id: number) => {
    try {
      await risksApi.close(id)
      loadRisks()
      loadStatistics()
    } catch (error) {
      console.error('Error closing risk:', error)
      alert('Error closing risk')
    }
  }

  const getRiskLevelColor = (level: RiskLevel): string => {
    const colors: Record<RiskLevel, string> = {
      critical: 'bg-red-900 text-white',
      high: 'bg-red-600 text-white',
      medium: 'bg-yellow-500 text-black',
      low: 'bg-blue-500 text-white',
      negligible: 'bg-gray-400 text-white',
    }
    return colors[level]
  }

  const getStatusColor = (status: RiskStatus): string => {
    const colors: Record<RiskStatus, string> = {
      identified: 'bg-gray-200 text-gray-800',
      assessed: 'bg-blue-200 text-blue-800',
      treated: 'bg-green-200 text-green-800',
      accepted: 'bg-purple-200 text-purple-800',
      monitored: 'bg-yellow-200 text-yellow-800',
      closed: 'bg-gray-400 text-white',
    }
    return colors[status]
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Risk Management</h1>
        <p className="text-gray-600">Manage and assess risks for NIS2 compliance</p>
      </div>

      {/* Statistics Cards */}
      {statistics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Total Risks</h3>
            <p className="text-3xl font-bold text-gray-900">{statistics.total_risks}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">High Priority</h3>
            <p className="text-3xl font-bold text-red-600">{statistics.high_priority_risks}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Overdue</h3>
            <p className="text-3xl font-bold text-orange-600">{statistics.overdue_risks}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-sm font-medium text-gray-500">Avg. Risk Score</h3>
            <p className="text-3xl font-bold text-blue-600">{statistics.average_risk_score}</p>
          </div>
        </div>
      )}

      {/* Actions and Filters */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="flex flex-wrap items-center gap-4">
          <button
            onClick={() => setShowCreateDialog(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            + New Risk
          </button>
          <button
            onClick={loadMatrix}
            className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
          >
            Risk Matrix
          </button>

          <input
            type="text"
            placeholder="Search risks..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border rounded flex-1 min-w-[200px]"
          />

          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value as RiskStatus | 'all')}
            className="px-4 py-2 border rounded"
          >
            <option value="all">All Statuses</option>
            <option value="identified">Identified</option>
            <option value="assessed">Assessed</option>
            <option value="treated">Treated</option>
            <option value="accepted">Accepted</option>
            <option value="monitored">Monitored</option>
            <option value="closed">Closed</option>
          </select>

          <select
            value={filterLevel}
            onChange={(e) => setFilterLevel(e.target.value as RiskLevel | 'all')}
            className="px-4 py-2 border rounded"
          >
            <option value="all">All Levels</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
            <option value="negligible">Negligible</option>
          </select>
        </div>
      </div>

      {/* Risks Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading ? (
          <div className="p-8 text-center">Loading risks...</div>
        ) : risks.length === 0 ? (
          <div className="p-8 text-center text-gray-500">No risks found</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">L</th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">I</th>
                  <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Level</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {risks.map((risk) => (
                  <tr key={risk.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">{risk.risk_id}</td>
                    <td className="px-6 py-4 text-sm text-gray-900">{risk.title}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{risk.category || '-'}</td>
                    <td className="px-6 py-4 text-sm text-center">{risk.likelihood}</td>
                    <td className="px-6 py-4 text-sm text-center">{risk.impact}</td>
                    <td className="px-6 py-4 text-sm text-center font-bold">{risk.risk_score}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded ${getRiskLevelColor(risk.risk_level)}`}>
                        {risk.risk_level.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded ${getStatusColor(risk.status)}`}>
                        {risk.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <div className="flex gap-2">
                        <button
                          onClick={() => {
                            setSelectedRisk(risk)
                            setShowEditDialog(true)
                          }}
                          className="text-blue-600 hover:text-blue-800"
                        >
                          Edit
                        </button>
                        {risk.status === 'identified' && (
                          <button
                            onClick={() => handleAcceptRisk(risk.id)}
                            className="text-green-600 hover:text-green-800"
                          >
                            Accept
                          </button>
                        )}
                        {risk.status !== 'closed' && (
                          <button
                            onClick={() => handleCloseRisk(risk.id)}
                            className="text-gray-600 hover:text-gray-800"
                          >
                            Close
                          </button>
                        )}
                        <button
                          onClick={() => handleDeleteRisk(risk.id)}
                          className="text-red-600 hover:text-red-800"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Create Risk Dialog */}
      {showCreateDialog && (
        <CreateRiskDialog
          onClose={() => setShowCreateDialog(false)}
          onSubmit={handleCreateRisk}
        />
      )}

      {/* Edit Risk Dialog */}
      {showEditDialog && selectedRisk && (
        <EditRiskDialog
          risk={selectedRisk}
          onClose={() => {
            setShowEditDialog(false)
            setSelectedRisk(null)
          }}
          onSubmit={(data) => handleUpdateRisk(selectedRisk.id, data)}
        />
      )}

      {/* Risk Matrix Dialog */}
      {showMatrix && (
        <RiskMatrixDialog
          matrix={riskMatrix}
          onClose={() => setShowMatrix(false)}
        />
      )}
    </div>
  )
}

// Create Risk Dialog Component
const CreateRiskDialog: React.FC<{
  onClose: () => void
  onSubmit: (data: RiskCreate) => void
}> = ({ onClose, onSubmit }) => {
  const [formData, setFormData] = useState<RiskCreate>({
    risk_id: '',
    title: '',
    description: '',
    category: '',
    likelihood: 1,
    impact: 1,
    treatment_plan: '',
    identified_date: new Date().toISOString().split('T')[0],
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <h2 className="text-2xl font-bold mb-4">Create New Risk</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Risk ID *</label>
              <input
                type="text"
                required
                value={formData.risk_id}
                onChange={(e) => setFormData({ ...formData, risk_id: e.target.value })}
                className="w-full px-3 py-2 border rounded"
                placeholder="e.g., RISK-2024-001"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Title *</label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Description *</label>
              <textarea
                required
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-3 py-2 border rounded h-24"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Category</label>
              <input
                type="text"
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full px-3 py-2 border rounded"
                placeholder="e.g., Cyber Security"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Likelihood (1-5) *</label>
                <input
                  type="number"
                  required
                  min="1"
                  max="5"
                  value={formData.likelihood}
                  onChange={(e) => setFormData({ ...formData, likelihood: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Impact (1-5) *</label>
                <input
                  type="number"
                  required
                  min="1"
                  max="5"
                  value={formData.impact}
                  onChange={(e) => setFormData({ ...formData, impact: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Treatment Plan</label>
              <textarea
                value={formData.treatment_plan}
                onChange={(e) => setFormData({ ...formData, treatment_plan: e.target.value })}
                className="w-full px-3 py-2 border rounded h-24"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Identified Date *</label>
              <input
                type="date"
                required
                value={formData.identified_date}
                onChange={(e) => setFormData({ ...formData, identified_date: e.target.value })}
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            <div className="flex gap-2 justify-end pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 border rounded hover:bg-gray-100"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Create Risk
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

// Edit Risk Dialog Component
const EditRiskDialog: React.FC<{
  risk: Risk
  onClose: () => void
  onSubmit: (data: RiskUpdate) => void
}> = ({ risk, onClose, onSubmit }) => {
  const [formData, setFormData] = useState<RiskUpdate>({
    title: risk.title,
    description: risk.description,
    category: risk.category || '',
    likelihood: risk.likelihood,
    impact: risk.impact,
    status: risk.status,
    treatment_plan: risk.treatment_plan || '',
    residual_likelihood: risk.residual_likelihood || undefined,
    residual_impact: risk.residual_impact || undefined,
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <h2 className="text-2xl font-bold mb-4">Edit Risk: {risk.risk_id}</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Title</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-3 py-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-3 py-2 border rounded h-24"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Likelihood (1-5)</label>
                <input
                  type="number"
                  min="1"
                  max="5"
                  value={formData.likelihood}
                  onChange={(e) => setFormData({ ...formData, likelihood: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Impact (1-5)</label>
                <input
                  type="number"
                  min="1"
                  max="5"
                  value={formData.impact}
                  onChange={(e) => setFormData({ ...formData, impact: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border rounded"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value as RiskStatus })}
                className="w-full px-3 py-2 border rounded"
              >
                <option value="identified">Identified</option>
                <option value="assessed">Assessed</option>
                <option value="treated">Treated</option>
                <option value="accepted">Accepted</option>
                <option value="monitored">Monitored</option>
                <option value="closed">Closed</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Treatment Plan</label>
              <textarea
                value={formData.treatment_plan}
                onChange={(e) => setFormData({ ...formData, treatment_plan: e.target.value })}
                className="w-full px-3 py-2 border rounded h-24"
              />
            </div>

            <div className="flex gap-2 justify-end pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 border rounded hover:bg-gray-100"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Update Risk
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

// Risk Matrix Dialog Component
const RiskMatrixDialog: React.FC<{
  matrix: Record<string, number>
  onClose: () => void
}> = ({ matrix, onClose }) => {
  const getCellColor = (likelihood: number, impact: number): string => {
    const score = likelihood * impact
    if (score >= 20) return 'bg-red-900 text-white'
    if (score >= 15) return 'bg-red-600 text-white'
    if (score >= 10) return 'bg-yellow-500'
    if (score >= 5) return 'bg-blue-500 text-white'
    return 'bg-gray-300'
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full p-6">
        <h2 className="text-2xl font-bold mb-6">Risk Assessment Matrix</h2>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr>
                <th className="border p-2 bg-gray-100"></th>
                {[1, 2, 3, 4, 5].map((impact) => (
                  <th key={impact} className="border p-2 bg-gray-100">Impact {impact}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[5, 4, 3, 2, 1].map((likelihood) => (
                <tr key={likelihood}>
                  <td className="border p-2 bg-gray-100 font-bold">Likelihood {likelihood}</td>
                  {[1, 2, 3, 4, 5].map((impact) => {
                    const key = `${likelihood}_${impact}`
                    const count = matrix[key] || 0
                    return (
                      <td
                        key={impact}
                        className={`border p-4 text-center font-bold text-2xl ${getCellColor(likelihood, impact)}`}
                      >
                        {count}
                      </td>
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

export default RisksPage
