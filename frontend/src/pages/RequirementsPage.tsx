import { useEffect, useState } from 'react'
import { requirementsApi } from '@/services/api'
import { FileCheck, ChevronDown, ChevronUp } from 'lucide-react'
import type { Requirement, RequirementCategory } from '@/types'

const categoryLabels: Record<RequirementCategory, string> = {
  risk_management: 'Risikomanagement',
  incident_management: 'Incident Management',
  business_continuity: 'Business Continuity',
  supply_chain: 'Lieferkettensicherheit',
  security_acquisition: 'Sichere Beschaffung',
  effectiveness_testing: 'Wirksamkeitsprüfung',
  cyber_hygiene: 'Cyber-Hygiene',
  cryptography: 'Kryptografie',
  personnel_security: 'Personalsicherheit',
  mfa_communication: 'MFA & Kommunikation',
}

export default function RequirementsPage() {
  const [requirements, setRequirements] = useState<Requirement[]>([])
  const [loading, setLoading] = useState(true)
  const [expandedId, setExpandedId] = useState<number | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  useEffect(() => {
    const loadRequirements = async () => {
      try {
        const data = await requirementsApi.list()
        setRequirements(data)
      } catch (error) {
        console.error('Failed to load requirements:', error)
      } finally {
        setLoading(false)
      }
    }

    loadRequirements()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const filteredRequirements = selectedCategory === 'all'
    ? requirements
    : requirements.filter((r) => r.category === selectedCategory)

  const categories = Array.from(new Set(requirements.map((r) => r.category)))

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center">
          <FileCheck className="h-8 w-8 mr-3 text-primary-600" />
          NIS2-Anforderungen
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Übersicht über alle {requirements.length} NIS2-Compliance-Anforderungen nach Artikel 21
        </p>
      </div>

      {/* Filter */}
      <div className="card">
        <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
          Kategorie filtern
        </label>
        <select
          id="category"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="input max-w-md"
        >
          <option value="all">Alle Kategorien ({requirements.length})</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {categoryLabels[category]} ({requirements.filter((r) => r.category === category).length})
            </option>
          ))}
        </select>
      </div>

      {/* Requirements List */}
      <div className="space-y-4">
        {filteredRequirements.map((requirement) => (
          <div key={requirement.id} className="card">
            {/* Header */}
            <div
              className="flex items-start justify-between cursor-pointer"
              onClick={() => setExpandedId(expandedId === requirement.id ? null : requirement.id)}
            >
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                    {requirement.code}
                  </span>
                  <span className="badge badge-info">
                    {categoryLabels[requirement.category]}
                  </span>
                  {requirement.is_mandatory && (
                    <span className="badge badge-danger">
                      Verpflichtend
                    </span>
                  )}
                  <span className="text-xs text-gray-500">
                    Priorität {requirement.priority}
                  </span>
                </div>
                <h3 className="text-lg font-medium text-gray-900">
                  {requirement.title}
                </h3>
                <p className="mt-1 text-sm text-gray-600">
                  {requirement.description}
                </p>
              </div>
              <button className="ml-4 text-gray-400 hover:text-gray-600">
                {expandedId === requirement.id ? (
                  <ChevronUp className="h-5 w-5" />
                ) : (
                  <ChevronDown className="h-5 w-5" />
                )}
              </button>
            </div>

            {/* Expanded Details */}
            {expandedId === requirement.id && (
              <div className="mt-4 pt-4 border-t border-gray-200 space-y-4">
                {requirement.legal_reference && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900">Rechtsgrundlage</h4>
                    <p className="mt-1 text-sm text-gray-600">{requirement.legal_reference}</p>
                  </div>
                )}

                {requirement.implementation_guidance && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900">Umsetzungshinweise</h4>
                    <p className="mt-1 text-sm text-gray-600">{requirement.implementation_guidance}</p>
                  </div>
                )}

                {requirement.evidence_required && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900">Erforderliche Nachweise</h4>
                    <p className="mt-1 text-sm text-gray-600">{requirement.evidence_required}</p>
                  </div>
                )}

                {requirement.iso27001_controls && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900">ISO 27001 Mapping</h4>
                    <p className="mt-1 text-sm text-gray-600">
                      Controls: {JSON.parse(requirement.iso27001_controls).join(', ')}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {filteredRequirements.length === 0 && (
          <div className="card text-center py-12">
            <p className="text-gray-500">Keine Anforderungen in dieser Kategorie gefunden.</p>
          </div>
        )}
      </div>
    </div>
  )
}
