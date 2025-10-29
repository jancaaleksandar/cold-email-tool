'use client'

import { useState } from 'react'
import LeadsTable from '@/components/LeadsTable'
import Header from '@/components/Header'
import UploadModal from '@/components/UploadModal'

export default function Home() {
  const [showUploadModal, setShowUploadModal] = useState(false)
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleUploadSuccess = () => {
    setShowUploadModal(false)
    setRefreshTrigger(prev => prev + 1)
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <Header onUploadClick={() => setShowUploadModal(true)} />
      
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Lead Management
          </h1>
          <p className="text-gray-600">
            Upload, enrich, and manage your leads in one place
          </p>
        </div>

        <LeadsTable refreshTrigger={refreshTrigger} />
      </div>

      {showUploadModal && (
        <UploadModal
          onClose={() => setShowUploadModal(false)}
          onSuccess={handleUploadSuccess}
        />
      )}
    </main>
  )
}

