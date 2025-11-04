import { useEffect, useState } from 'react'
import { measuresApi } from '@/services/api'
import { ClipboardList } from 'lucide-react'
import type { Measure, MeasureStatus } from '@/types'
import clsx from 'clsx'

const statusLabels: Record<MeasureStatus, string> = {
  not_started: 'Nicht begonnen',
  planned: 'Geplant',
  in_progress: 'In Bearbeitung',
  implemented: 'Umgesetzt',
  verified: 'Verifiziert',
  not_applicable: 'Nicht anwendbar',
}

const statusColors: Record<MeasureStatus, string> = {
  not_started: 'bg-gray-100 text-gray-800',
  planned: 'bg-blue-100 text-blue-800',
  in_progress: 'bg-yellow-100 text-yellow-800',
  implemented: 'bg-green-100 text-green-800',
  verified: 'bg-green-200 text-green-900',
  not_applicable: 'bg-gray-200 text-gray-600',
}

export default function MeasuresPage() {
  const [measures, setMeasures] = useState<Measure[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedStatus, setSelectedStatus] = useState<string>('all')

  useEffect(() => {
    const loadMeasures = async () => {
      try {
        const data = await measuresApi.list()
        setMeasures(data)
      } catch (error) {
        console.error('Failed to load measures:', error)
      } finally {
        setLoading(false)
      }
    }

    loadMeasures()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const filteredMeasures = selectedStatus === 'all'
    ? measures
    : measures.filter((m) => m.status === selectedStatus)

  const statuses = Array.from(new Set(measures.map((m) => m.status)))

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center">
          <ClipboardList className="h-8 w-8 mr-3 text-primary-600" />
          Compliance-Maßnahmen
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Übersicht über alle {measures.length} Maßnahmen zur Erfüllung der NIS2-Anforderungen
        </p>
      </div>

      {/* Filter */}
      <div className="card">
        <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">
          Status filtern
        </label>
        <select
          id="status"
          value={selectedStatus}
          onChange={(e) => setSelectedStatus(e.target.value)}
          className="input max-w-md"
        >
          <option value="all">Alle Status ({measures.length})</option>
          {statuses.map((status) => (
            <option key={status} value={status}>
              {statusLabels[status]} ({measures.filter((m) => m.status === status).length})
            </option>
          ))}
        </select>
      </div>

      {/* Measures List */}
      {filteredMeasures.length > 0 ? (
        <div className="grid grid-cols-1 gap-4">
          {filteredMeasures.map((measure) => (
            <div key={measure.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      {measure.code}
                    </span>
                    <span className={clsx('badge', statusColors[measure.status])}>
                      {statusLabels[measure.status]}
                    </span>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900">
                    {measure.title}
                  </h3>
                  <p className="mt-1 text-sm text-gray-600">
                    {measure.description}
                  </p>

                  {measure.implementation_details && (
                    <div className="mt-3 p-3 bg-gray-50 rounded-md">
                      <h4 className="text-xs font-medium text-gray-700 mb-1">
                        Umsetzungsdetails
                      </h4>
                      <p className="text-sm text-gray-600">
                        {measure.implementation_details}
                      </p>
                    </div>
                  )}

                  {/* Dates */}
                  <div className="mt-3 flex flex-wrap gap-4 text-xs text-gray-500">
                    {measure.planned_start_date && (
                      <div>
                        <span className="font-medium">Geplanter Start:</span>{' '}
                        {new Date(measure.planned_start_date).toLocaleDateString('de-DE')}
                      </div>
                    )}
                    {measure.planned_completion_date && (
                      <div>
                        <span className="font-medium">Geplanter Abschluss:</span>{' '}
                        {new Date(measure.planned_completion_date).toLocaleDateString('de-DE')}
                      </div>
                    )}
                    {measure.actual_completion_date && (
                      <div>
                        <span className="font-medium">Tatsächlicher Abschluss:</span>{' '}
                        {new Date(measure.actual_completion_date).toLocaleDateString('de-DE')}
                      </div>
                    )}
                  </div>

                  {/* Effectiveness Score */}
                  {measure.effectiveness_score !== null && (
                    <div className="mt-3">
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-medium text-gray-700">
                          Wirksamkeit:
                        </span>
                        <div className="flex-1 max-w-xs bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-green-600 h-2 rounded-full"
                            style={{ width: `${measure.effectiveness_score * 100}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-600">
                          {Math.round(measure.effectiveness_score * 100)}%
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <ClipboardList className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">
            {selectedStatus === 'all'
              ? 'Noch keine Maßnahmen vorhanden.'
              : 'Keine Maßnahmen mit diesem Status gefunden.'}
          </p>
        </div>
      )}
    </div>
  )
}
