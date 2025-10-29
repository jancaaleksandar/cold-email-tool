'use client'

import { Upload, Sparkles } from 'lucide-react'

interface HeaderProps {
  onUploadClick: () => void
}

export default function Header({ onUploadClick }: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-500 text-white p-2 rounded-lg">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Clay Clone</h1>
              <p className="text-xs text-gray-500">Lead Enrichment Platform</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={onUploadClick}
              className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
            >
              <Upload className="w-4 h-4" />
              <span>Upload Leads</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

