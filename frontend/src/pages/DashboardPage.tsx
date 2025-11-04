import { useEffect, useState } from 'react'
import { useAuthStore } from '@/store/authStore'
import { requirementsApi, measuresApi } from '@/services/api'
import { Shield, AlertTriangle, CheckCircle2, Clock } from 'lucide-react'
import type { Requirement, Measure } from '@/types'

export default function DashboardPage() {
  const { user } = useAuthStore()
  const [requirements, setRequirements] = useState<Requirement[]>([])
  const [measures, setMeasures] = useState<Measure[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      try {
        const [reqData, measuresData] = await Promise.all([
          requirementsApi.list(),
          measuresApi.list(),
        ])
        setRequirements(reqData)
        setMeasures(measuresData)
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const stats = {
    totalRequirements: requirements.length,
    mandatoryRequirements: requirements.filter((r) => r.is_mandatory).length,
    totalMeasures: measures.length,
    implementedMeasures: measures.filter((m) => m.status === 'implemented' || m.status === 'verified').length,
    inProgressMeasures: measures.filter((m) => m.status === 'in_progress').length,
    notStartedMeasures: measures.filter((m) => m.status === 'not_started').length,
  }

  const completionRate = stats.totalMeasures > 0
    ? Math.round((stats.implementedMeasures / stats.totalMeasures) * 100)
    : 0

  return (
    <div className="space-y-6">
      {/* Welcome */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Willkommen, {user?.full_name || user?.username}!
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Übersicht über Ihren NIS2-Compliance-Status
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* Total Requirements */}
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Shield className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  NIS2-Anforderungen
                </dt>
                <dd className="flex items-baseline">
                  <div className="text-2xl font-semibold text-gray-900">
                    {stats.totalRequirements}
                  </div>
                  <div className="ml-2 text-sm text-gray-500">
                    ({stats.mandatoryRequirements} verpflichtend)
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>

        {/* Implemented Measures */}
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircle2 className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Umgesetzte Maßnahmen
                </dt>
                <dd className="flex items-baseline">
                  <div className="text-2xl font-semibold text-gray-900">
                    {stats.implementedMeasures}
                  </div>
                  <div className="ml-2 text-sm text-gray-500">
                    von {stats.totalMeasures}
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>

        {/* In Progress */}
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Clock className="h-8 w-8 text-yellow-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  In Bearbeitung
                </dt>
                <dd className="flex items-baseline">
                  <div className="text-2xl font-semibold text-gray-900">
                    {stats.inProgressMeasures}
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>

        {/* Not Started */}
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-8 w-8 text-red-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  Nicht begonnen
                </dt>
                <dd className="flex items-baseline">
                  <div className="text-2xl font-semibold text-gray-900">
                    {stats.notStartedMeasures}
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      {/* Compliance Progress */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Compliance-Fortschritt
        </h3>
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-600">Umsetzungsgrad</span>
            <span className="font-semibold text-gray-900">{completionRate}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className="bg-primary-600 h-4 rounded-full transition-all duration-500"
              style={{ width: `${completionRate}%` }}
            />
          </div>
        </div>

        {completionRate < 100 && (
          <p className="mt-4 text-sm text-gray-600">
            {stats.notStartedMeasures + stats.inProgressMeasures} Maßnahmen müssen noch umgesetzt werden,
            um vollständige NIS2-Compliance zu erreichen.
          </p>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
        <div className="card hover:shadow-lg transition-shadow cursor-pointer">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Anforderungen ansehen
          </h3>
          <p className="text-sm text-gray-600 mb-4">
            Überblick über alle {stats.totalRequirements} NIS2-Anforderungen
          </p>
          <a href="/requirements" className="btn btn-primary">
            Zu den Anforderungen
          </a>
        </div>

        <div className="card hover:shadow-lg transition-shadow cursor-pointer">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Maßnahmen verwalten
          </h3>
          <p className="text-sm text-gray-600 mb-4">
            Verwalten und tracken Sie Ihre Compliance-Maßnahmen
          </p>
          <a href="/measures" className="btn btn-primary">
            Zu den Maßnahmen
          </a>
        </div>
      </div>

      {/* NIS2 Info */}
      <div className="card bg-blue-50 border border-blue-200">
        <div className="flex">
          <Shield className="h-6 w-6 text-blue-600 flex-shrink-0" />
          <div className="ml-3">
            <h3 className="text-sm font-medium text-blue-800">
              Über NIS2
            </h3>
            <div className="mt-2 text-sm text-blue-700">
              <p>
                Die NIS2-Richtlinie verpflichtet Unternehmen ab 50 Mitarbeitenden und 10 Mio. € Umsatz
                in bestimmten Sektoren zur Implementierung von Cybersicherheitsmaßnahmen.
              </p>
              <p className="mt-2">
                <strong>Deutschland:</strong> Umsetzung bis Ende 2025/Anfang 2026 erwartet.
                <br />
                <strong>Sanktionen:</strong> Bis zu 10 Mio. € oder 2% des weltweiten Jahresumsatzes.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
