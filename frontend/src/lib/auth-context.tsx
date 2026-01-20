"use client"

import { createContext, useContext, useState, useEffect } from 'react'
import { authClient, Session, User } from './auth-client'

interface AuthContextType {
  session: Session | null
  user: User | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session | null>(null)
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing session on mount
    const initAuth = async () => {
      try {
        // @ts-ignore
        const currentSession = await authClient.getSession()
        setSession(currentSession)
        if (currentSession?.user) {
          setUser(currentSession.user)
        }
      } catch (error) {
        console.error('Auth initialization error:', error)
      } finally {
        setLoading(false)
      }
    }

    initAuth()

    // Set up session listener
    // @ts-ignore
    const unsubscribe = authClient.onSessionChange((newSession) => {
      // @ts-ignore
      setSession(newSession)
      // @ts-ignore
      setUser(newSession?.user || null)
    })

    return () => {
      unsubscribe()
    }
  }, [])

  const signIn = async (email: string, password: string) => {
    setLoading(true)
    try {
      const result = await authClient.signIn.email({
        email,
        password,
      })

      if (result.error) {
        throw new Error(result.error.message)
      }

      // @ts-ignore
      const newSession = await authClient.getSession()
      setSession(newSession)
      setUser(newSession?.user || null)
    } finally {
      setLoading(false)
    }
  }

  const signUp = async (email: string, password: string) => {
    setLoading(true)
    try {
      const result = await authClient.signUp.email({
        email,
        password,
        name: email.split('@')[0], // Use part of email as name since we don't catch it
      })

      if (result.error) {
        throw new Error(result.error.message)
      }

      // @ts-ignore
      const newSession = await authClient.getSession()
      setSession(newSession)
      setUser(newSession?.user || null)
    } finally {
      setLoading(false)
    }
  }

  const signOut = async () => {
    await authClient.signOut()
    setSession(null)
    setUser(null)
  }

  const value: AuthContextType = {
    session,
    user,
    loading,
    signIn,
    signUp,
    signOut,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be within AuthProvider')
  }
  return context
}
