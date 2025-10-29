import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Lead {
  id: number
  first_name: string | null
  last_name: string | null
  company: string | null
  title: string | null
  website: string | null
  linkedin_url: string | null
  email: string | null
  phone: string | null
  enrichment_status: string
  enriched_data: any
  created_at: string
  updated_at: string
}

export const fetchLeads = async (): Promise<Lead[]> => {
  const response = await api.get('/api/leads/')
  return response.data
}

export const uploadCSV = async (file: File): Promise<any> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/api/leads/upload-csv', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const enrichLeads = async (leadIds: number[], enrichmentTypes: string[]): Promise<any> => {
  const response = await api.post('/api/enrich/', {
    lead_ids: leadIds,
    enrichment_types: enrichmentTypes,
  })
  return response.data
}

export const deleteLead = async (leadId: number): Promise<void> => {
  await api.delete(`/api/leads/${leadId}`)
}

export const getEnrichmentStatus = async (leadId: number): Promise<any> => {
  const response = await api.get(`/api/enrich/status/${leadId}`)
  return response.data
}

