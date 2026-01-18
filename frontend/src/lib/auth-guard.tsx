"use client"

import { useRouter } from 'next/navigation'
import { useAuth } from './auth-context'
import { useEffect } from 'react'

interface AuthGuardProps {
  children: React.ReactNode
}

/**
 * AuthGuard component that protects routes from unauthenticated users.
 * Wrap this around protected pages to automatically redirect to signin page
 * if the user is not authenticated.
 */
export function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter()
  const { user, loading } = useAuth()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/signin')
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return <>{children}</>
}
