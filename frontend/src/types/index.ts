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

// API Error
export interface ApiError {
  detail: string
}
