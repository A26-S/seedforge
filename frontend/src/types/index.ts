export type UUID = string

export interface Seed {
  id: UUID
  value: string
  category: string
  source: 'builtin' | 'imported'
  tags: string[]
  enabled: boolean
}

export interface Rule {
  id: UUID
  type: string
  name: string
  config: Record<string, any>
  enabled: boolean
  order: number
}

export interface ProgressInfo {
  current: number
  total: number
  speed: number
  eta: number
}

export interface ResultInfo {
  generated: number
  deduplicated: number
  filtered: number
  filePath?: string
}

export type TaskStatus = 'pending' | 'running' | 'paused' | 'completed' | 'failed' | 'cancelled'

export interface Task {
  id: UUID
  name: string
  seedIds: UUID[]
  ruleIds: UUID[]
  status: TaskStatus
  progress: ProgressInfo
  results: ResultInfo
  createdAt: string
  startedAt?: string
  completedAt?: string
  errorMessage?: string
}
