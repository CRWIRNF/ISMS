// User types
export enum UserRole {
  ADMIN = 'admin',
  MANAGER = 'manager',
  AUDITOR = 'auditor',
  USER = 'user',
}

export enum AuthProvider {
  LOCAL = 'local',
  ENTRA = 'entra',
}

export interface User {
  id: number
  username: string
  email: string
  full_name: string | null
  role: UserRole
  auth_provider: AuthProvider
  is_active: boolean
  created_at: string
  last_login: string | null
}

export interface LoginRequest {
  username: string
  password: string
}

export interface Token {
  access_token: string
  token_type: string
}

// Requirement types
export enum RequirementCategory {
  RISK_MANAGEMENT = 'risk_management',
  INCIDENT_MANAGEMENT = 'incident_management',
  BUSINESS_CONTINUITY = 'business_continuity',
  SUPPLY_CHAIN = 'supply_chain',
  SECURITY_ACQUISITION = 'security_acquisition',
  EFFECTIVENESS_TESTING = 'effectiveness_testing',
  CYBER_HYGIENE = 'cyber_hygiene',
  CRYPTOGRAPHY = 'cryptography',
  PERSONNEL_SECURITY = 'personnel_security',
  MFA_COMMUNICATION = 'mfa_communication',
}

export interface Requirement {
  id: number
  code: string
  category: RequirementCategory
  title: string
  description: string
  legal_reference: string | null
  iso27001_controls: string | null
  is_mandatory: boolean
  priority: number
  implementation_guidance: string | null
  evidence_required: string | null
  created_at: string
  updated_at: string
}

// Measure types
export enum MeasureStatus {
  NOT_STARTED = 'not_started',
  PLANNED = 'planned',
  IN_PROGRESS = 'in_progress',
  IMPLEMENTED = 'implemented',
  VERIFIED = 'verified',
  NOT_APPLICABLE = 'not_applicable',
}

export interface Measure {
  id: number
  requirement_id: number
  code: string
  title: string
  description: string
  status: MeasureStatus
  implementation_details: string | null
  responsible_user_id: number | null
  planned_start_date: string | null
  planned_completion_date: string | null
  actual_completion_date: string | null
  last_review_date: string | null
  next_review_date: string | null
  effectiveness_score: number | null
  created_at: string
  updated_at: string
}

// Risk types
export enum RiskLevel {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
  NEGLIGIBLE = 'negligible',
}

export enum RiskStatus {
  IDENTIFIED = 'identified',
  ASSESSED = 'assessed',
  TREATED = 'treated',
  ACCEPTED = 'accepted',
  MONITORED = 'monitored',
  CLOSED = 'closed',
}

export interface Risk {
  id: number
  risk_id: string
  title: string
  description: string
  category: string | null
  likelihood: number
  impact: number
  risk_score: number
  risk_level: RiskLevel
  status: RiskStatus
  treatment_plan: string | null
  residual_likelihood: number | null
  residual_impact: number | null
  residual_risk_score: number | null
  residual_risk_level: RiskLevel | null
  requirement_id: number | null
  related_measure_id: number | null
  owner_id: number
  identified_date: string
  target_closure_date: string | null
  actual_closure_date: string | null
  last_review_date: string | null
  next_review_date: string | null
  created_at: string
  updated_at: string
}

export interface RiskCreate {
  risk_id: string
  title: string
  description: string
  category?: string
  likelihood: number
  impact: number
  treatment_plan?: string
  requirement_id?: number
  related_measure_id?: number
  identified_date: string
}

export interface RiskUpdate {
  title?: string
  description?: string
  category?: string
  likelihood?: number
  impact?: number
  status?: RiskStatus
  treatment_plan?: string
  residual_likelihood?: number
  residual_impact?: number
  target_closure_date?: string
  actual_closure_date?: string
  last_review_date?: string
  next_review_date?: string
}

export interface RiskStatistics {
  total_risks: number
  status_distribution: Record<string, number>
  level_distribution: Record<string, number>
  average_risk_score: number
  high_priority_risks: number
  overdue_risks: number
  review_required: number
}

// API Error
export interface ApiError {
  detail: string
}
